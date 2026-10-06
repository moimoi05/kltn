"""Check rendered figure text and editable 3D diagrams against thesis styling."""
from pathlib import Path
import xml.etree.ElementTree as ET


def check(root: Path):
    import pymupdf
    color_errors, native_errors, svg_errors = [], [], []
    files = sorted((root / 'image').glob('*.pdf'))
    for path in files:
        with pymupdf.open(path) as doc:
            for page in doc:
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines', []):
                        for span in line['spans']:
                            if span['text'].strip() and span['color'] != 0:
                                color_errors.append({'figure': path.stem, 'text': span['text'], 'rgb': span['color']})
        for cell in ET.parse(root / 'figures_source' / (path.stem + '.drawio')).iter('mxCell'):
            if cell.get('vertex') == '1' and cell.get('value', '').strip():
                styles = dict(item.split('=', 1) for item in cell.get('style', '').split(';') if '=' in item)
                if styles.get('fontColor', '').lower() not in {'#000000', '#000', 'black'}:
                    native_errors.append({'figure': path.stem, 'cell': cell.get('id')})
        for node in ET.parse(path.with_suffix('.svg')).iter():
            if node.tag.rsplit('}', 1)[-1] == 'text' and ''.join(node.itertext()).strip():
                if node.get('fill', '').lower() not in {'#000000', '#000', 'black'}:
                    svg_errors.append({'figure': path.stem, 'text': ''.join(node.itertext())})
    volume_figures = ['modality-preprocessing', 'final-pipeline', 'outer-vs-cp']
    missing_3d = []
    for name in volume_figures:
        styles = [cell.get('style', '') for cell in ET.parse(root / 'figures_source' / (name + '.drawio')).iter('mxCell')]
        if not any('shape=cube' in style or 'shape=stencil(' in style for style in styles):
            missing_3d.append(name)
    report = {'figure_pdfs_checked': len(files), 'colored_pdf_text': color_errors,
              'colored_drawio_text': native_errors, 'colored_svg_text': svg_errors,
              'three_dimensional_figures_checked': volume_figures, 'missing_3d_representation': missing_3d}
    report['pass'] = len(files) == 16 and not any((color_errors, native_errors, svg_errors, missing_3d))
    return report


if __name__ == '__main__':
    import json
    report = check(Path(__file__).resolve().parents[1])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['pass'] else 1)
