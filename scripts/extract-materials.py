#!/usr/bin/env python3
"""Extract lecture text and embedded images locally; Python 3.10+, stdlib only."""
import argparse
import html
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def paragraph_text(blob, namespace):
    """Walk each paragraph's descendants, rather than flushing on its opening tag."""
    root = ET.fromstring(blob)
    paragraphs = []
    for paragraph in root.iter(namespace + 'p'):
        parts = []
        for node in paragraph.iter():
            if node.tag == namespace + 't':
                parts.append(node.text or '')
            elif node.tag in (namespace + 'br', namespace + 'cr'):
                parts.append('\n')
            elif node.tag == namespace + 'tab':
                parts.append('\t')
        text = ''.join(parts).strip()
        if text:
            paragraphs.append(text)
    return '\n'.join(paragraphs)


def relationships(archive, part):
    folder, name = posixpath.split(part)
    relpath = posixpath.join(folder, '_rels', name + '.rels')
    if relpath not in archive.namelist():
        return {}
    result = {}
    for rel in ET.fromstring(archive.read(relpath)):
        if rel.get('TargetMode') == 'External':
            continue
        target = rel.get('Target', '')
        resolved = posixpath.normpath(
            target.lstrip('/') if target.startswith('/') else posixpath.join(folder, target)
        )
        if resolved == '..' or resolved.startswith('../') or '\\' in resolved:
            raise ValueError('Invalid package relationship target')
        result[rel.get('Id')] = (resolved, rel.get('Type', ''))
    return result


def extract_media(archive, prefix, destination):
    mapping = {}
    for member in archive.namelist():
        if not member.startswith(prefix) or member.endswith('/'):
            continue
        # Only direct media files are copied; never extract ZIP paths to disk.
        name = member[len(prefix):]
        if '/' in name or '\\' in name or name in ('', '.', '..') or ':' in name:
            raise ValueError('Invalid media member path')
        target = destination / 'media' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(member))
        mapping[member] = 'media/' + name
    return mapping


def extract_pptx(path, destination):
    blocks, sections = [], []
    with zipfile.ZipFile(path) as archive:
        presentation = 'ppt/presentation.xml'
        rels = relationships(archive, presentation)
        root = ET.fromstring(archive.read(presentation))
        slide_list = root.find(P + 'sldIdLst')
        if slide_list is None:
            raise ValueError('Presentation contains no slide list')
        media = extract_media(archive, 'ppt/media/', destination)
        for number, slide_id in enumerate(slide_list, 1):
            part, kind = rels[slide_id.get(R + 'id')]
            if not kind.endswith('/slide'):
                raise ValueError('Slide list relationship is not a slide')
            slide_rels = relationships(archive, part)
            body = paragraph_text(archive.read(part), A)
            notes = []
            for related, relkind in slide_rels.values():
                if relkind.endswith('/notesSlide'):
                    note_root = ET.fromstring(archive.read(related))
                    # Slide number/date/header/footer placeholders aren't speaker notes.
                    for shape in note_root.iter(P + 'sp'):
                        placeholder = shape.find('.//' + P + 'ph')
                        if placeholder is not None and placeholder.get('type') in (
                            'sldImg', 'sldNum', 'dt', 'hdr', 'ftr'
                        ):
                            continue
                        text = paragraph_text(ET.tostring(shape), A)
                        if text:
                            notes.append(text)
            images = sorted({media[target] for target, relkind in slide_rels.values()
                             if relkind.endswith('/image') and target in media})
            blocks.append(f'SLIDE {number}\n{body or "[No extractable text; inspect slide.]"}')
            if notes:
                blocks.append('SPEAKER NOTES\n' + '\n'.join(notes))
            if images:
                blocks.append('EMBEDDED IMAGES\n' + '\n'.join(images))
            sections.append({'slide': number, 'part': part, 'images': images})
    return '\n\n'.join(blocks), {'sections': sections, 'media': list(media.values())}


def extract_docx(path, destination):
    with zipfile.ZipFile(path) as archive:
        body = paragraph_text(archive.read('word/document.xml'), W)
        media = extract_media(archive, 'word/media/', destination)
    return body, {'media': list(media.values())}


def extract_plain(path):
    raw = path.read_text(encoding='utf-8-sig')
    if path.suffix.lower() not in ('.vtt', '.srt'):
        return raw
    result = []
    for block in re.split(r'\n\s*\n', raw.replace('\r\n', '\n')):
        lines = block.strip().splitlines()
        if not lines or lines[0].startswith(('WEBVTT', 'NOTE', 'STYLE', 'REGION')):
            continue
        timing = next((i for i, line in enumerate(lines) if '-->' in line), None)
        if timing is None:
            continue
        # Preserve cue alignment, but omit identifiers, cue settings, and markup.
        match = re.match(r'(\S+)\s+-->\s+(\S+)', lines[timing])
        if not match:
            continue
        body = html.unescape(re.sub(r'<[^>]+>', '', '\n'.join(lines[timing + 1:])))
        result.append(f'[{match[1]} --> {match[2]}]\n{body}')
    return '\n\n'.join(result)


def extract(path, destination):
    path, destination = Path(path), Path(destination)
    ext = path.suffix.lower()
    if ext not in ('.pptx', '.docx', '.txt', '.md', '.vtt', '.srt'):
        raise ValueError('Supported: PPTX, DOCX, TXT, MD, VTT, SRT. Render/read PDFs separately.')
    if not path.is_file():
        raise ValueError('Source file does not exist')
    # A fresh destination protects source documents and earlier reviewed extractions.
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Output directory must be empty; choose a new destination')
    destination.mkdir(parents=True, exist_ok=True)
    if ext == '.pptx':
        text, manifest = extract_pptx(path, destination)
    elif ext == '.docx':
        text, manifest = extract_docx(path, destination)
    else:
        text, manifest = extract_plain(path), {}
    manifest.update(source=path.name, format=ext.lstrip('.'))
    (destination / 'extracted.txt').write_text(text + '\n', encoding='utf-8')
    (destination / 'manifest.json').write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8'
    )
    return destination / 'extracted.txt'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('-o', '--outdir', type=Path, required=True,
                        help='empty destination for extracted.txt, manifest.json, and media/')
    args = parser.parse_args()
    try:
        output = extract(args.file, args.outdir)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as error:
        parser.exit(1, f'Extraction failed: {error}\n')
    print(output)


if __name__ == '__main__':
    main()
