"""Check source consistency and the latest compiled PDF/log; no model/data access."""
from pathlib import Path
import argparse
import collections
import json
import re


def source_checks(root):
    files = [root / 'main.tex'] + sorted((root / 'chapters').glob('*.tex')) + sorted((root / 'FrontMatter').glob('*.tex'))
    texts = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8') for p in files}
    joined = '\n'.join(texts.values())
    bib = (root / 'references.bib').read_text(encoding='utf-8')
    bib_keys = re.findall(r'@\w+\s*\{\s*([^,\s]+)', bib)
    citations = set()
    for group in re.findall(r'\\(?:nocite|cite|citet|citep|citealt|citeauthor|citeyear)(?:\[[^\]]*\])*\{([^}]+)\}', joined):
        citations.update(k.strip() for k in group.split(','))
    labels = re.findall(r'\\label\{([^}]+)\}', joined)
    refs = set(re.findall(r'\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}', joined))
    duplicates = sorted(k for k, n in collections.Counter(labels).items() if n > 1)
    figures = {}
    missing_graphics = []
    for name, text in texts.items():
        if name.startswith('chapters'):
            figures[name] = len(re.findall(r'\\begin\{figure\}', text))
        for graphic in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', text):
            candidates = [root / graphic, root / 'image' / graphic]
            if not any(p.is_file() for p in candidates):
                missing_graphics.append(graphic)
    narrative = '\n'.join(t for name, t in texts.items() if name.startswith('chapters'))
    return {
        'chapter_count': len(figures), 'figures_per_chapter': figures,
        'figure_count': sum(figures.values()), 'citation_keys_used': len(citations),
        'missing_citations': sorted(citations - set(bib_keys)),
        'unused_bibliography_keys': sorted(set(bib_keys) - citations),
        'non_paper_bibliography_entries': re.findall(r'@(?!article\b|inproceedings\b)\w+\s*\{\s*([^,\s]+)', bib, re.I),
        'internal_project_citations': sorted(k for k in citations if k.startswith('nam2026')),
        'duplicate_bibliography_keys': sorted(k for k, n in collections.Counter(bib_keys).items() if n > 1),
        'duplicate_labels': duplicates, 'undefined_source_references': sorted(refs - set(labels)),
        'missing_graphics': sorted(set(missing_graphics)),
        'todo_fixme': bool(re.search(r'\b(?:TODO|FIXME)\b', joined, re.I)),
        'old_experiment_final_name': bool(re.search(r'\bA6(?:_NO_RC)?\b', narrative)),
        'resizebox_used': '\\resizebox' in joined,
    }


def build_checks(root, pdf_path):
    from pypdf import PdfReader
    log_path = root / 'main.log'
    log = log_path.read_text(encoding='utf-8', errors='replace') if log_path.exists() else ''
    reader = PdfReader(pdf_path)
    title = 'Longitudinal Learning with Tensor Fusion for Predicting Progression of Alzheimer’s Disease'
    expected_chapters = [re.search(r'\\chapter\{([^}]+)\}', p.read_text(encoding='utf-8')).group(1)
                         for p in sorted((root / 'chapters').glob('*.tex'))]
    chapter_pages = {}
    def walk(items):
        for item in items:
            if isinstance(item, list):
                walk(item)
            else:
                try:
                    name = str(item.title)
                    index = reader.get_destination_page_number(item) + 1
                    if name in expected_chapters or re.match(r'^[1-5]\s', name):
                        chapter_pages[name] = index
                except (AttributeError, ValueError, KeyError):
                    pass
    walk(reader.outline)
    bibliography_page = None
    for item in reader.outline:
        if not isinstance(item, list) and 'TÀI LIỆU' in str(getattr(item, 'title', '')):
            bibliography_page = reader.get_destination_page_number(item) + 1
    first_chapter = min(chapter_pages.values()) if chapter_pages else None
    main_count = bibliography_page - first_chapter if first_chapter and bibliography_page else None
    bbl = (root / 'main.bbl').read_text(encoding='utf-8', errors='replace') if (root / 'main.bbl').exists() else ''
    bibitems = re.findall(r'\\bibitem(?:\[[\s\S]*?\])?\s*\{([^}]+)\}', bbl)
    return {
        'pdf': pdf_path.name, 'total_pdf_pages': len(reader.pages),
        'main_content_pages': main_count, 'chapter_pdf_pages': chapter_pages,
        'bibliography_pdf_page': bibliography_page,
        'compiled_reference_count': len(bibitems),
        'baseline_is_reference_one': bool(bibitems and bibitems[0] == 'aghajanian2025longitudinal'),
        'pdf_title': str(reader.metadata.title), 'official_title_matches_metadata': str(reader.metadata.title) == title,
        'overfull_boxes': re.findall(r'Overfull \\[hv]box[^\n]*', log),
        'underfull_boxes': re.findall(r'Underfull \\[hv]box[^\n]*', log),
        'undefined_build_reference_or_citation': bool(re.search(r'(?:Reference|Citation)[^\n]{0,300}undefined|There were undefined', re.sub(r'\s+', ' ', log))),
        'bibtex_errors': bool(re.search(r"I couldn't open|I found no database|error message", (root / 'main.blg').read_text(encoding='utf-8', errors='replace'))) if (root / 'main.blg').exists() else True,
        'latex_errors': re.findall(r'^!.*$', log, re.M),
        'missing_glyph_warning': bool(re.search(r'Missing character|not contain the glyph', log)),
        'float_too_large': bool(re.search(r'Float too large|Too many unprocessed floats', log)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--visual-record', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    report = {'source': source_checks(root)}
    from qa_performance_tables import check as check_performance_tables
    report['performance_tables'] = check_performance_tables(root)
    from qa_figure_style import check as check_figure_style
    report['figure_style'] = check_figure_style(root)
    pdf = args.pdf or root / 'main.pdf'
    if pdf.exists():
        report['build'] = build_checks(root, pdf)
    if args.visual_record and args.visual_record.exists():
        report['visual_review'] = json.loads(args.visual_record.read_text(encoding='utf-8'))
    s = report['source']
    failure_keys = ['missing_citations', 'unused_bibliography_keys', 'non_paper_bibliography_entries',
                    'internal_project_citations', 'duplicate_bibliography_keys', 'duplicate_labels',
                    'undefined_source_references', 'missing_graphics', 'todo_fixme', 'old_experiment_final_name', 'resizebox_used']
    errors = [key for key in failure_keys if s[key]]
    if not report['figure_style']['pass']:
        errors.append('figure_text_color_or_3d_representation')
    if s['chapter_count'] != 5 or any(n < 1 for n in s['figures_per_chapter'].values()):
        errors.append('chapter_figure_requirement')
    if 'build' in report:
        b = report['build']
        for key in ['overfull_boxes', 'undefined_build_reference_or_citation', 'bibtex_errors', 'latex_errors', 'missing_glyph_warning', 'float_too_large']:
            if b[key]:
                errors.append(key)
        if b['total_pdf_pages'] > 70 or not b['official_title_matches_metadata']:
            errors.append('page_limit_or_title')
        if not b['baseline_is_reference_one'] or b['compiled_reference_count'] != s['citation_keys_used']:
            errors.append('baseline_order_or_reference_count')
    report['automated_check_pass'] = not errors
    report['failed_checks'] = errors
    (root / 'qa_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
