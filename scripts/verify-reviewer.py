#!/usr/bin/env python3
"""Build fresh Typst previews and record visual inspection without trusting stale files."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, report):
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')


def inputs(root, final_pdf):
    result = {}
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if any(part in {'verification', '.git', '__pycache__', '.venv', 'node_modules'} for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError('Reviewer inputs must not contain symbolic links')
        if not path.is_file() or path == final_pdf or path.name in {'_progress.md', '_study-progress.md'}:
            continue
        if path.name.startswith('.env') or path.name == 'credentials.json' or path.suffix in {'.key', '.pem'}:
            continue
        result[relative.as_posix()] = digest(path)
    return result


def build(source, ppi=120, compiler='typst'):
    source = Path(source).resolve()
    if not source.is_file() or source.suffix != '.typ':
        raise ValueError('Provide an existing .typ source')
    root = source.parent
    output = source.with_suffix('.pdf')
    run = root/'verification'/('run-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
    run.mkdir(parents=True)
    report_path = run/'verification.json'
    report = {'source': str(source), 'input_root': str(root), 'final_pdf': str(output),
              'created_utc': datetime.now(timezone.utc).isoformat(), 'ppi': ppi,
              'status': 'build-failed', 'pages': []}
    try:
        before = inputs(root, output)
        for target in [str(run/'reviewer.pdf'), str(run/'page-{p}.png')]:
            command = [compiler, 'compile', '--root', str(root), str(source), target]
            if target.endswith('.png'):
                command += ['--ppi', str(ppi)]
            subprocess.run(command, cwd=root, check=True, capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
        pages = sorted(run.glob('page-*.png'), key=lambda path: int(path.stem.split('-')[-1]))
        if not pages or not (run/'reviewer.pdf').is_file():
            raise ValueError('Compiler produced no PDF/pages')
        if inputs(root, output) != before:
            raise ValueError('Inputs changed during build; rebuild from a stable source')
        shutil.copy2(run/'reviewer.pdf', output)
        report.update(status='visual-check-pending', input_hashes=before,
                      pdf_sha256=digest(output), run_pdf_sha256=digest(run/'reviewer.pdf'),
                      pages=[{'page': int(path.stem.split('-')[-1]), 'file': path.name,
                              'sha256': digest(path), 'inspected': False} for path in pages])
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        report['error'] = error.stderr if isinstance(error, subprocess.CalledProcessError) else str(error)
    save(report_path, report)
    return report_path, report


def inspect(report_path, pages, notes):
    report_path = Path(report_path).resolve()
    report = json.loads(report_path.read_text(encoding='utf-8'))
    if report['status'] not in ('visual-check-pending', 'verified'):
        raise ValueError('Cannot inspect a failed build')
    root = Path(report['input_root'])
    final = Path(report['final_pdf'])
    if inputs(root, final) != report['input_hashes']:
        raise ValueError('Source/materials/template changed; rebuild before inspection')
    if digest(final) != report['pdf_sha256'] or digest(report_path.parent/'reviewer.pdf') != report['run_pdf_sha256']:
        raise ValueError('PDF changed; rebuild before inspection')
    available = {row['page'] for row in report['pages']}
    if not pages or not set(pages).issubset(available):
        raise ValueError('Inspection page numbers are not in this render run')
    for row in report['pages']:
        image = report_path.parent/row['file']
        if image.parent != report_path.parent or digest(image) != row['sha256']:
            raise ValueError('Preview changed; rebuild before inspection')
    for row in report['pages']:
        if row['page'] in pages:
            row.update(inspected=True, inspection_notes=notes,
                       inspected_utc=datetime.now(timezone.utc).isoformat())
    report['status'] = 'verified' if all(row['inspected'] for row in report['pages']) else 'visual-check-pending'
    save(report_path, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    builder = commands.add_parser('build')
    builder.add_argument('source', type=Path)
    builder.add_argument('--ppi', type=int, default=120)
    recorder = commands.add_parser('inspect')
    recorder.add_argument('report', type=Path)
    recorder.add_argument('--pages', required=True, help='comma-separated pages actually viewed')
    recorder.add_argument('--notes', required=True, help='findings from the actual visual check')
    args = parser.parse_args()
    try:
        if args.command == 'build':
            if args.ppi < 72:
                raise ValueError('Use at least 72 ppi; default 120')
            path, report = build(args.source, args.ppi)
            print(path)
            if report['status'] == 'build-failed':
                parser.exit(1, 'Build failed; see the report.\n')
        else:
            if not args.notes.strip():
                raise ValueError('Inspection notes must not be empty')
            report = inspect(args.report, [int(page) for page in args.pages.split(',')], args.notes)
            print(report['status'])
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'Verification failed: {error}\n')


if __name__ == '__main__':
    main()
