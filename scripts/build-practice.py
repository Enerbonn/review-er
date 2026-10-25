#!/usr/bin/env python3
"""Validate one MCQ bank and render matching Typst practice views (stdlib only)."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import random
import re
import shutil


def required(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{field} must be a nonempty string')
    return value


def normalized(value):
    return re.sub(r'\s+', ' ', value).strip().casefold()


def prepare(bank, count=None, seed=None):
    bank = copy.deepcopy(bank)
    if not isinstance(bank, dict):
        raise ValueError('Bank must be an object')
    required(bank.get('title'), 'title')
    items = bank.get('items')
    if not isinstance(items, list) or not items:
        raise ValueError('items must be a nonempty list')
    if count is not None and (type(count) is not int or count < 1 or len(items) != count):
        raise ValueError('Bank does not match requested item count')
    ids, stems = set(), set()
    rng = random.Random(seed)
    for item in items:
        if not isinstance(item, dict):
            raise ValueError('Each item must be an object')
        ident = required(item.get('id'), 'item id')
        stem = normalized(required(item.get('stem'), 'stem'))
        required(item.get('topic'), 'topic')
        required(item.get('source'), 'source')
        required(item.get('rationale'), 'rationale')
        if ident in ids or stem in stems:
            raise ValueError('Duplicate item id or question stem')
        ids.add(ident)
        stems.add(stem)
        options = item.get('options')
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError('Each MCQ needs exactly four options')
        if any(not isinstance(option, dict) for option in options):
            raise ValueError('Each option must be an object')
        option_ids = [required(option.get('id'), 'option id') for option in options]
        texts = [normalized(required(option.get('text'), 'option text')) for option in options]
        if len(set(option_ids)) != 4 or len(set(texts)) != 4:
            raise ValueError('Options must have distinct ids and text')
        correct = required(item.get('correct'), 'correct option id')
        if correct not in option_ids:
            raise ValueError('Correct option must exist')
        distractors = item.get('distractors')
        if not isinstance(distractors, dict) or set(distractors) != set(option_ids) - {correct}:
            raise ValueError('Every distractor needs an explanation, and only distractors')
        for reason in distractors.values():
            required(reason, 'distractor explanation')
        if seed is not None:
            rng.shuffle(options)
        item['answer_letter'] = 'ABCD'[next(i for i, option in enumerate(options) if option['id'] == correct)]
    blueprint = bank.get('blueprint')
    if not isinstance(blueprint, dict) or not blueprint or any(type(n) is not int or n < 1 for n in blueprint.values()):
        raise ValueError('blueprint needs positive item counts by topic')
    if dict(Counter(item['topic'] for item in items)) != blueprint:
        raise ValueError('Topic coverage does not match blueprint')
    return bank


def literal(value):
    # Strings become literal text, never executable Typst markup from the bank.
    return '#text(' + json.dumps(value, ensure_ascii=False) + ')'


def question(item, number):
    lines = [f'#heading(level: 2, numbering: none)[Question {number}]', literal(item['stem']), '#parbreak()']
    for label, option in zip('ABCD', item['options']):
        lines += [literal(label + '. ' + option['text']), '#linebreak()']
    return '\n'.join(lines)


def answer(item, number):
    correct_text = next(o['text'] for o in item['options'] if o['id'] == item['correct'])
    lines = [literal(f"{number}. Answer: {item['answer_letter']} — {correct_text}"),
             '#parbreak()', literal(item['rationale'])]
    for label, option in zip('ABCD', item['options']):
        if option['id'] != item['correct']:
            lines += ['#parbreak()', literal(label + '. ' + item['distractors'][option['id']])]
    return '\n'.join(lines)


def render(bank, view, profile):
    max_height = '205mm' if profile == 'tablet' else '245mm'
    suffix = 'Answer reviewer' if view == 'reviewer' else 'Mock exam'
    title = json.dumps(bank['title'] + ' — ' + suffix, ensure_ascii=False)
    lines = ['#import "template/academic.typ": *',
             f'#show: reviewer.with(title: {title}, style: "visual", profile: "{profile}")',
             '#show heading.where(level: 2): it => block(sticky: true, above: 8pt, below: 6pt)[#text(size: 11.5pt, weight: "bold", fill: maroon)[#it.body]]',
             literal('Practice material; not an official or validated exam.')]
    if view == 'exam':
        lines += ['= Questions']
        for n, item in enumerate(bank['items'], 1):
            lines += [f'#practice-item(max-height: {max_height})[', question(item, n), '#note-lines(count: 1)', ']']
        lines += ['#pagebreak()', '= Answers and rationales']
        lines += [literal('Key: ' + '   '.join(f"{n}: {item['answer_letter']}" for n, item in enumerate(bank['items'], 1)))]
        for n, item in enumerate(bank['items'], 1):
            lines += [f'#practice-item(max-height: {max_height})[', answer(item, n), ']']
    else:
        lines += [literal('Answers are visible. Use the matching mock exam first for an unseen attempt.')]
        for n, item in enumerate(bank['items'], 1):
            length = len(item['stem']) + sum(len(o['text']) for o in item['options']) + len(item['rationale']) + sum(map(len, item['distractors'].values()))
            stacked = 'true' if length > 750 else 'false'
            lines += ['#practice-pair([', question(item, n), '], [', answer(item, n),
                      f'], stacked: {stacked}, label: "Question {n}", max-height: {max_height})']
    return '\n\n'.join(lines) + '\n'


def build(bank_path, output, view='both', count=None, profile='paper', seed=None):
    if view not in {'both', 'reviewer', 'exam'} or profile not in {'paper', 'tablet'}:
        raise ValueError('Unsupported view or profile')
    bank_path, output = Path(bank_path).resolve(), Path(output).resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('Use an empty output directory; existing work is preserved')
    bank = prepare(json.loads(bank_path.read_text(encoding='utf-8-sig')), count, seed)
    output.mkdir(parents=True, exist_ok=True)
    normalized_bank = json.dumps(bank, ensure_ascii=False, indent=2) + '\n'
    (output / 'practice-bank.json').write_text(normalized_bank, encoding='utf-8')
    views = ['reviewer', 'exam'] if view == 'both' else [view]
    for selected in views:
        folder = output / selected
        folder.mkdir()
        shutil.copytree(Path(__file__).resolve().parents[1] / 'assets/template', folder / 'template')
        (folder / 'reviewer.typ').write_text(render(bank, selected, profile), encoding='utf-8')
    record = {'count': len(bank['items']), 'blueprint': bank['blueprint'], 'seed': seed,
              'views': views, 'profile': profile, 'matching_questions': view == 'both',
              'source_bank_sha256': hashlib.sha256(bank_path.read_bytes()).hexdigest(),
              'final_bank_sha256': hashlib.sha256(normalized_bank.encode()).hexdigest(),
              'status': 'written; compile and visual checks pending'}
    (output / 'practice-manifest.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bank', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    parser.add_argument('--view', choices=['reviewer', 'exam', 'both'], default='both')
    parser.add_argument('--count', type=int)
    parser.add_argument('--profile', choices=['paper', 'tablet'], default='paper')
    parser.add_argument('--seed', type=int)
    args = parser.parse_args()
    try:
        record = build(args.bank, args.output, args.view, args.count, args.profile, args.seed)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'Practice build failed: {error}\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
