"""Audit manuscript tables against the user-provided common-seed report.

This verifies transcription, derived differences, coverage and emphasis. It does
not verify remote checkpoint execution or recompute patient-level predictions.
"""
from pathlib import Path
import json
import re


def plain(cell):
    return cell.removeprefix(r'\bestresult{').removesuffix('}') if cell.startswith(r'\bestresult{') else cell


def value(cell):
    text = plain(cell).replace('{,}', '.').replace(',', '.')
    matches = re.findall(r'[+-]?\d+(?:\.\d+)?', text)
    assert len(matches) == 1, cell
    return float(matches[0])


def table_rows(source, label):
    table = source.split(r'\label{' + label + '}', 1)[1].split(r'\end{table}', 1)[0]
    return [[c.strip() for c in line.removesuffix(r'\\').strip().split('&')]
            for line in table.splitlines() if '&' in line and not line.startswith(r'\textbf')]


def check_row(cells, records, by_key, offset, kind):
    name = plain(cells[0])
    if name == 'RC-Free -- Bỏ RC':
        name = 'RC-Free Pairwise Fusion'
    record = records[name]
    got = [value(cells[offset]), value(cells[offset + 1])]
    expected = [record['validation'], record['test']]
    if offset == 2:
        assert value(cells[1]) == record['epoch'], name
    if kind == 'gains':
        baseline = by_key['paper_adaptation']
        expected = expected + [record['validation'] - baseline['validation'], record['test'] - baseline['test']]
        got = got + [value(cells[3]), value(cells[4])]
    if kind == 'ablation':
        expected = expected + [record['validation'] - by_key['cp_pairwise']['validation'], record['test'] - record['validation']]
        got = got + [value(cells[3]), value(cells[4])]
    assert all(abs(a - b) <= 0.0000005 for a, b in zip(got, expected)), (name, got, expected)
    return record['key']


def check_tables(source, records, by_key):
    covered = set()
    checked = []
    for label, offset, kind in [('tab:mri-milestones', 2, 'scores'),
                                ('tab:fusion-common-seed', 2, 'scores'),
                                ('tab:baseline-gains', 1, 'gains'),
                                ('tab:ablation', 1, 'ablation')]:
        rows = table_rows(source, label)
        covered = covered | {check_row(cells, records, by_key, offset, kind) for cells in rows}
        for index in (offset, offset + 1):
            highest = max(value(row[index]) for row in rows)
            for cells in rows:
                assert cells[index].startswith(r'\bestresult{') == (value(cells[index]) == highest), (label, cells[0], index)
        checked = checked + [{'table': label, 'rows': len(rows), 'numbers_and_maximum_emphasis_match': True}]
    assert covered == set(by_key), sorted(set(by_key) - covered)
    return checked, covered


def check(root):
    data = json.loads((root / 'provenance/common_seed_evaluation_20261008.json').read_text(encoding='utf-8'))
    records = {r['name']: r for r in data['records']}
    by_key = {r['key']: r for r in data['records']}
    source = (root / 'chapters/chapter4.tex').read_text(encoding='utf-8')
    assert len(records) == 22 and data['seed'] == 20260727
    checked, covered = check_tables(source, records, by_key)
    # The fixed-lambda follow-up is also named in prose with its selected epoch.
    fixed = by_key['rcfree_fixed']
    assert 'epoch 12' in source and f"{fixed['validation']:.6f}".replace('.', ',') in source
    assert f"{fixed['test']:.6f}".replace('.', ',') in source
    files = sorted((root / 'chapters').glob('*.tex')) + sorted((root / 'FrontMatter').glob('*.tex'))
    narrative = '\n'.join(p.read_text(encoding='utf-8') for p in files)
    assert not re.search(r'\b(?:P\d{2}(?:[-_][A-Z0-9]+)?|A[1-6])\b', narrative), 'Visible phase/variant codes found'
    assert not re.search(r'classical|cổ điển|Cox elastic-net|Random Survival Forest|0[,.]860707|0[,.]856549', narrative, re.I)
    assert 'test hậu nghiệm' in source and 'chưa đủ bằng chứng kết luận RC-Free ổn định nhất' in source
    return {'seed': data['seed'], 'distinct_models_checked': len(covered), 'tables': checked,
            'no_visible_phase_codes': True, 'posthoc_test_scope_preserved': True,
            'verification_scope': 'Transcription/arithmetic only; remote execution not independently reproduced', 'pass': True}


if __name__ == '__main__':
    print(json.dumps(check(Path(__file__).resolve().parent.parent), ensure_ascii=False, indent=2))
