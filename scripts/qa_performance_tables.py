"""Check the published benchmark table against frozen research evidence."""
from pathlib import Path
import json
import math
import re
import statistics


def normalized(name):
    return re.sub(r'\s+', ' ', name.replace('–', '-').replace('--', '-')
                  .replace('$\\lambda$', 'λ')).strip()


def check(root):
    data = json.loads((root / 'figures_source/results_data.json').read_text(encoding='utf-8'))
    records = data['benchmark']
    means = {normalized(r['label']): statistics.fmean(r['values']) for r in records}
    maximum = max(means.values())
    winners = {name for name, mean in means.items() if math.isclose(mean, maximum, abs_tol=1e-12)}
    chapter = (root / 'chapters/chapter4.tex').read_text(encoding='utf-8')
    table = chapter.split('\\label{tab:standard-bench}', 1)[1].split('\\end{table}', 1)[0]
    checked = []
    for line in table.splitlines():
        if '&' not in line:
            continue
        cells = [s.strip() for s in line.removesuffix('\\\\').strip().split('&')]
        bold = [c.startswith('\\bestresult{') and c.endswith('}') for c in cells]
        plain = [c[len('\\bestresult{'):-1] if flag else c for c, flag in zip(cells, bold)]
        name = normalized(plain[0])
        if name not in means:
            continue
        record = next(r for r in records if normalized(r['label']) == name)
        numbers = [float(n) for cell in plain[1:] for n in
                   re.findall(r'\d+\.\d+', cell.replace('{,}', '.').replace(',', '.'))]
        expected = record['values'] + [means[name], statistics.stdev(record['values'])]
        assert len(numbers) == len(expected) == 5, name
        assert all(abs(a - b) <= 0.0000005 for a, b in zip(numbers, expected)), name
        assert math.isclose(record['mean'], means[name], abs_tol=1e-12), name
        assert math.isclose(record['sd'], expected[-1], abs_tol=1e-12), name
        assert all(bold) if name in winners else not any(bold), name
        checked.append(name)
    assert len(checked) == len(records) == len(set(checked)), checked
    return {'benchmark_rows_checked': len(checked), 'highest_mean': maximum,
            'rows_bolded_by_mean_including_ties': sorted(winners),
            'values_mean_sample_sd_match_frozen_evidence': True}


if __name__ == '__main__':
    print(json.dumps(check(Path(__file__).resolve().parent.parent), ensure_ascii=False, indent=2))
