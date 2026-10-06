"""Native draw.io first, then PDF/SVG from the same 160-mm scene.
ReportLab is the fallback when draw.io desktop CLI is absent.
Charts read the separately audited results_data.json only.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "image"
SRC = ROOT / "figures_source"
WIDTH = 453.5433  # 160 mm
INK = "#263B4D"
LINE = "#5C6B79"
COLORS = {
    "m": ("#E7F0FA", "#567DA3"),
    "r": ("#EAF3E9", "#638560"),
    "c": ("#FBF0E3", "#A27D51"),
    "pair": ("#FAE9ED", "#A87984"),
    "fusion": ("#EEEAF6", "#86759D"),
    "time": ("#E8F3F8", "#6590A5"),
    "out": ("#EEF0F2", "#77838F"),
    "white": ("#FFFFFF", "#A2ADB7"),
}
PROVENANCE: dict[str, dict] = {}
def register_fonts():
    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    candidates = [(windows / "arial.ttf", windows / "arialbd.ttf")]
    packaged_fonts = ROOT.parent / "thesis_revision_work" / "python_packages" / "matplotlib" / "mpl-data" / "fonts" / "ttf"
    candidates.append((packaged_fonts / "DejaVuSans.ttf", packaged_fonts / "DejaVuSans-Bold.ttf"))
    try:
        import matplotlib
        fontdir = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
        candidates.append((fontdir / "DejaVuSans.ttf", fontdir / "DejaVuSans-Bold.ttf"))
    except ImportError:
        pass
    found = [(regular, bold) for regular, bold in candidates if regular.exists() and bold.exists()]
    for regular, bold in found:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("ThesisSans", str(regular)))
            pdfmetrics.registerFont(TTFont("ThesisSansBold", str(bold)))
            fallback = next(((a, b) for a, b in found if "DejaVu" in a.name), (regular, bold))
            pdfmetrics.registerFont(TTFont("ThesisSymbols", str(fallback[0])))
            pdfmetrics.registerFont(TTFont("ThesisSymbolsBold", str(fallback[1])))
            return
    raise RuntimeError("Arial or DejaVu Sans font files are required for Vietnamese labels.")


def font_runs(text, bold=False):
    base = "ThesisSansBold" if bold else "ThesisSans"
    fallback = "ThesisSymbolsBold" if bold else "ThesisSymbols"
    supported = pdfmetrics.getFont(base).face.charToGlyph
    runs = []
    for char in text:
        font = base if ord(char) in supported else fallback
        if ord(char) not in pdfmetrics.getFont(font).face.charToGlyph:
            raise ValueError(f"Missing font glyph: {char!r} U+{ord(char):04X}")
        if runs and runs[-1][0] == font:
            runs[-1] = (font, runs[-1][1] + char)
        else:
            runs.append((font, char))
    return runs


def text_width(text, size, bold=False):
    return sum(pdfmetrics.stringWidth(chunk, font, size) for font, chunk in font_runs(text, bold))


class Scene:
    def __init__(self, name, height, sources=(), corrections=()):
        self.name, self.width, self.height = name, WIDTH, height
        self.items = []
        self.sources = list(sources)
        self.corrections = list(corrections)
        self.text_checks = []

    def text(self, x, y, text, size=10, bold=False, align="left", width=None, color=INK):
        item = {"kind": "text", "x": x, "y": y, "text": text, "size": size,
                "bold": bold, "align": align, "width": width, "color": color}
        self.items.append(item)
        for line in text.split("\n"):
            actual = text_width(line, size, bold)
            if width and actual > width + .2:
                self.text_checks.append(f"{self.name}: text exceeds width by {actual-width:.1f}: {line}")
        return item

    def box(self, x, y, w, h, text, color="out", size=10, bold_first=True, dashed=False):
        fill, stroke = COLORS[color]
        item = {"kind": "box", "x": x, "y": y, "w": w, "h": h, "text": text,
                "fill": fill, "stroke": stroke, "size": size, "bold_first": bold_first,
                "dashed": dashed, "id": f"n{len(self.items)+1}"}
        self.items.append(item)
        lines = text.split("\n") if text else []
        if len(lines) * size * 1.24 > h - 8:
            self.text_checks.append(f"{self.name}: text exceeds box height: {text}")
        for i, line in enumerate(lines):
            actual = text_width(line, size, bold_first and i == 0)
            if actual > w - 10:
                self.text_checks.append(f"{self.name}: box text exceeds by {actual-w+10:.1f}: {line}")
        return item

    def circle(self, x, y, r, text="", color="fusion", size=12):
        fill, stroke = COLORS[color]
        item = {"kind": "circle", "x": x, "y": y, "r": r, "text": text,
                "fill": fill, "stroke": stroke, "size": size, "id": f"n{len(self.items)+1}"}
        self.items.append(item)
        return item

    def bar(self, x, y, w, h, color="fusion"):
        item = self.box(x, y, w, h, "", color, 9.5)
        item["radius"] = 0
        return item

    def path(self, points, arrow=True, color=LINE, dashed=False, start_arrow=False, width=1.1):
        item = {"kind": "path", "points": points, "arrow": arrow,
                "color": color, "dashed": dashed, "start_arrow": start_arrow, "width": width}
        self.items.append(item)
        return item

    def line(self, x1, y1, x2, y2, **kwargs):
        return self.path([(x1, y1), (x2, y2)], **kwargs)

    def save_drawio(self):
        mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "Codex",
                                      "version": "native-xml"})
        diagram = ET.SubElement(mxfile, "diagram", {"id": self.name, "name": self.name})
        model = ET.SubElement(diagram, "mxGraphModel", {
            "grid": "0", "page": "1", "pageScale": "1", "pageWidth": str(self.width),
            "pageHeight": str(self.height), "background": "#FFFFFF", "math": "0"})
        root = ET.SubElement(model, "root")
        ET.SubElement(root, "mxCell", {"id": "0"})
        ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
        for index, item in enumerate(self.items):
            kind = item["kind"]
            attrs = {"id": item.get("id", f"i{index}"), "parent": "1"}
            base = f"html=1;fontFamily=Arial;fontColor={INK};whiteSpace=wrap;"
            if kind == "path":
                attrs.update(edge="1", value="", style=(
                    base + "edgeStyle=none;rounded=0;" +
                    f"endArrow={'block' if item['arrow'] else 'none'};endFill=1;endSize=5;" +
                    f"startArrow={'block' if item['start_arrow'] else 'none'};startFill=1;startSize=5;" +
                    f"strokeColor={item['color']};strokeWidth={item['width']};" +
                    ("dashed=1;dashPattern=4 3;" if item["dashed"] else "")))
                cell = ET.SubElement(root, "mxCell", attrs)
                geom = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
                for point, role in [(item["points"][0], "sourcePoint"), (item["points"][-1], "targetPoint")]:
                    ET.SubElement(geom, "mxPoint", {"x": str(point[0]), "y": str(point[1]), "as": role})
                if len(item["points"]) > 2:
                    arr = ET.SubElement(geom, "Array", {"as": "points"})
                    for point in item["points"][1:-1]:
                        ET.SubElement(arr, "mxPoint", {"x": str(point[0]), "y": str(point[1])})
                continue
            if kind == "box":
                lines = item["text"].split("\n")
                label = "<br>".join(("<b>" + html.escape(line) + "</b>") if i == 0 and item["bold_first"]
                                     else html.escape(line) for i, line in enumerate(lines))
                attrs.update(vertex="1", value=label, style=(base +
                    f"rounded={0 if item.get('radius') == 0 else 1};arcSize=8;fillColor={item['fill']};strokeColor={item['stroke']};" +
                    f"strokeWidth=1;fontSize={item['size']};spacing=5;" +
                    ("dashed=1;" if item["dashed"] else "")))
                x, y, w, h = item["x"], item["y"], item["w"], item["h"]
            elif kind == "circle":
                attrs.update(vertex="1", value=html.escape(item["text"]), style=(base +
                    f"ellipse;fillColor={item['fill']};strokeColor={item['stroke']};" +
                    f"strokeWidth=1;fontSize={item['size']};"))
                x, y = item["x"] - item["r"], item["y"] - item["r"]
                w = h = item["r"] * 2
            else:
                attrs.update(vertex="1", value=html.escape(item["text"]).replace("\n", "<br>"), style=(base +
                    f"text;strokeColor=none;fillColor=none;fontSize={item['size']};" +
                    f"fontStyle={1 if item['bold'] else 0};align={item['align']};verticalAlign=top;spacing=0;"))
                w = item["width"] or max(text_width(line, item["size"], item["bold"])
                    for line in item["text"].split("\n")) + 2
                x = item["x"] - (w / 2 if item["align"] == "center" else w if item["align"] == "right" else 0)
                y, h = item["y"], len(item["text"].split("\n")) * item["size"] * 1.24
            cell = ET.SubElement(root, "mxCell", attrs)
            ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w),
                                                "height": str(h), "as": "geometry"})
        ET.indent(mxfile, space="  ")
        ET.ElementTree(mxfile).write(SRC / f"{self.name}.drawio", encoding="utf-8", xml_declaration=True)

    def save_pdf(self):
        pdf = canvas.Canvas(str(OUT / f"{self.name}.pdf"), pagesize=(self.width, self.height))
        pdf.setTitle(self.name.replace("-", " "))
        pdf.setAuthor("Nguyen Phuong Nam")
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        for item in self.items:
            kind = item["kind"]
            if kind in ("box", "circle"):
                pdf.setFillColor(HexColor(item["fill"]))
                pdf.setStrokeColor(HexColor(item["stroke"]))
                pdf.setLineWidth(1)
                pdf.setDash([4, 3] if item.get("dashed") else [])
                if kind == "box":
                    pdf.roundRect(item["x"], self.height-item["y"]-item["h"], item["w"], item["h"], item.get("radius", 4), fill=1)
                    self._pdf_label(pdf, item)
                else:
                    pdf.circle(item["x"], self.height-item["y"], item["r"], fill=1)
                    self._pdf_text(pdf, item["x"], item["y"]-item["size"]*.5,
                                   item["text"], item["size"], False, "center", INK)
            elif kind == "text":
                self._pdf_text(pdf, item["x"], item["y"], item["text"], item["size"],
                               item["bold"], item["align"], item["color"])
            else:
                pdf.setStrokeColor(HexColor(item["color"]))
                pdf.setLineWidth(item["width"])
                pdf.setDash([4, 3] if item["dashed"] else [])
                path = pdf.beginPath()
                path.moveTo(item["points"][0][0], self.height-item["points"][0][1])
                for x, y in item["points"][1:]:
                    path.lineTo(x, self.height-y)
                pdf.drawPath(path)
                if item["arrow"]:
                    self._pdf_arrow(pdf, item["points"][-2], item["points"][-1], item["color"])
                if item["start_arrow"]:
                    self._pdf_arrow(pdf, item["points"][1], item["points"][0], item["color"])
        pdf.showPage()
        pdf.save()

    def _pdf_text(self, pdf, x, y, text, size, bold, align, color):
        pdf.setFillColor(HexColor(color))
        for i, line in enumerate(text.split("\n")):
            line_width = text_width(line, size, bold)
            left = x-line_width/2 if align == "center" else x-line_width if align == "right" else x
            for font, chunk in font_runs(line, bold):
                pdf.setFont(font, size)
                pdf.drawString(left, self.height-y-size*.84-i*size*1.24, chunk)
                left += pdfmetrics.stringWidth(chunk, font, size)

    def _pdf_label(self, pdf, item):
        lines = item["text"].split("\n")
        top = item["y"] + (item["h"]-len(lines)*item["size"]*1.24)/2 + item["size"]*.15
        for i, line in enumerate(lines):
            self._pdf_text(pdf, item["x"]+item["w"]/2, top+i*item["size"]*1.24,
                           line, item["size"], item["bold_first"] and i == 0, "center", INK)

    def _pdf_arrow(self, pdf, previous, tip, color):
        points = arrow_points(previous, tip)
        pdf.setFillColor(HexColor(color))
        path = pdf.beginPath()
        path.moveTo(points[0][0], self.height-points[0][1])
        for x, y in points[1:]:
            path.lineTo(x, self.height-y)
        path.close()
        pdf.drawPath(path, stroke=0, fill=1)

    def save_svg(self):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="160mm" height="{self.height/2.8346457:.3f}mm" viewBox="0 0 {self.width} {self.height}">',
               '<rect width="100%" height="100%" fill="white"/>']
        def text(x, y, label, size, bold=False, align="left", color=INK):
            anchor = "middle" if align == "center" else "end" if align == "right" else "start"
            for i, line in enumerate(label.split("\n")):
                svg.append(f'<text x="{x}" y="{y+size*.84+i*size*1.24}" font-family="Arial, DejaVu Sans, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{color}">{html.escape(line)}</text>')
        for item in self.items:
            kind = item["kind"]
            dash = ' stroke-dasharray="4 3"' if item.get("dashed") else ""
            if kind == "box":
                svg.append(f'<rect x="{item["x"]}" y="{item["y"]}" width="{item["w"]}" height="{item["h"]}" rx="{item.get("radius", 4)}" fill="{item["fill"]}" stroke="{item["stroke"]}" stroke-width="1"{dash}/>')
                lines = item["text"].split("\n")
                top = item["y"]+(item["h"]-len(lines)*item["size"]*1.24)/2+item["size"]*.15
                for i, label in enumerate(lines):
                    text(item["x"]+item["w"]/2, top+i*item["size"]*1.24, label,
                         item["size"], item["bold_first"] and i == 0, "center")
            elif kind == "circle":
                svg.append(f'<circle cx="{item["x"]}" cy="{item["y"]}" r="{item["r"]}" fill="{item["fill"]}" stroke="{item["stroke"]}" stroke-width="1"/>')
                text(item["x"], item["y"]-item["size"]*.5, item["text"], item["size"], align="center")
            elif kind == "text":
                text(item["x"], item["y"], item["text"], item["size"], item["bold"], item["align"], item["color"])
            else:
                pts = " ".join(f"{x},{y}" for x, y in item["points"])
                svg.append(f'<polyline points="{pts}" fill="none" stroke="{item["color"]}" stroke-width="{item["width"]}" stroke-linejoin="round"{dash}/>')
                for previous, tip, enabled in [(item["points"][-2], item["points"][-1], item["arrow"]),
                                               (item["points"][1], item["points"][0], item["start_arrow"])]:
                    if enabled:
                        pts = " ".join(f"{x},{y}" for x, y in arrow_points(previous, tip))
                        svg.append(f'<polygon points="{pts}" fill="{item["color"]}"/>')
        svg.append("</svg>")
        (OUT / f"{self.name}.svg").write_text("\n".join(svg), encoding="utf-8")

    def save(self):
        if self.text_checks:
            raise ValueError("\n".join(self.text_checks))
        self.save_drawio()  # Native editable source is deliberately authored first.
        self.save_pdf()
        self.save_svg()
        PROVENANCE[self.name] = {
            "outputs": [f"image/{self.name}.pdf", f"image/{self.name}.svg"],
            "editable_source": f"figures_source/{self.name}.drawio",
            "based_on": self.sources,
            "changes": self.corrections + ["Redrawn as native draw.io; unified vector style and physical font sizes."],
            "rendering": "ReportLab/SVG fallback from the same scene; draw.io desktop CLI unavailable.",
            "width_mm": 160, "minimum_font_pt": min([item.get("size", 10) for item in self.items]),
        }
        print(f"Created {self.name}: {self.width:.1f} x {self.height:.1f} pt")


def arrow_points(previous, tip):
    dx, dy = tip[0]-previous[0], tip[1]-previous[1]
    norm = math.hypot(dx, dy) or 1
    dx, dy = dx/norm, dy/norm
    return [tip, (tip[0]-5*dx+2.5*dy, tip[1]-5*dy-2.5*dx),
            (tip[0]-5*dx-2.5*dy, tip[1]-5*dy+2.5*dx)]


def timeline():
    s = Scene("mci-progression-timeline", 314,
        ["D:/KLTN/metadata/scripts/pipeline_common.py", "D:/KLTN/metadata/scripts/05_create_survival_labels.py",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Separate third-MRI prediction origin p from the 18-month eligibility landmark L.",
         "Show conditional eligibility through L and score-defined post-L outcomes; retain ±90-day clinical matching limitation."])
    s.text(18, 9, "Chọn 3 MRI trong cửa sổ 18 tháng: baseline ≤ s₁ < s₂ < s₃ ≤ L", 10, bold=True)
    for x, label in [(70, "Visit 1\ns₁"), (160, "Visit 2\ns₂"), (250, "Visit 3\ns₃ = p")]:
        s.box(x-39, 40, 78, 43, label, "time", 10)
        s.text(x, 91, "MRI + R + C", 9.5, align="center")
        s.line(x, 108, x, 130)
    s.line(18, 135, 437, 135)
    s.line(25, 128, 25, 143, arrow=False)
    s.text(18, 149, "Baseline", 9.5)
    s.line(250, 130, 250, 143, arrow=False, width=1.5)
    s.text(250, 149, "Dự đoán tại p", 9.5, bold=True, align="center")
    s.line(332, 112, 332, 178, arrow=False, dashed=True)
    s.text(327, 183, "L = baseline + 18 tháng", 9.5, align="right")
    s.box(352, 40, 87, 45, "Tiến triển*\nSau L", "out", 10)
    s.box(352, 207, 87, 45, "Kiểm duyệt\nSau L", "out", 10)
    s.path([(340, 135), (346, 135), (346, 62), (352, 62)])
    s.path([(340, 135), (346, 135), (346, 230), (352, 230)])
    s.path([(25, 218), (25, 226), (332, 226), (332, 218)], arrow=False, color=COLORS["time"][1])
    s.text(178, 234, "Điều kiện: không tiến triển sớm đến hết L", 9.5, align="center")
    s.text(18, 260, "Thời gian mô hình = (ngày outcome − p) / 365.25; p có thể trùng L.", 9.5)
    s.text(18, 277, "* Endpoint theo MMSE < 24 hoặc CDR-global ≥ 1 sau L.", 9.5)
    s.text(18, 294, "Clinical ghép gần nhất ±90 ngày; có thể quan sát sau ngày MRI.", 9.5)
    s.save()


def taxonomy():
    s = Scene("fusion-taxonomy", 303,
        ["D:/KLTN/pileline.drawio", "D:/KLTN/pairwise_tensor_fusion_pipeline_v2.svg"],
        ["Separate simple feature combination, explicit pair interaction, and adaptive routing."])
    s.box(13, 119, 96, 52, "Multimodal\nM · R · C", "white")
    rows = [(13, "Concatenation", "Ghép các đặc trưng", "out"),
            (69, "Element-wise", "Tương tác theo phần tử", "out"),
            (125, "Bilinear / outer product", "Tương tác bậc hai đầy đủ", "pair"),
            (181, "Low-rank CP", "Factorize tensor trọng số", "pair"),
            (237, "Gated residual", "Điều tiết đóng góp từng route", "fusion")]
    for y, title, detail, color in rows:
        s.box(146, y, 291, 45, title+"\n"+detail, color)
        s.path([(109, 145), (127, 145), (127, y+22.5), (146, y+22.5)])
    s.text(13, 288, "Thesis kết hợp CP cho pairwise interaction và gated residual cho routing.", 9.5)
    s.save()


def cohort():
    s = Scene("cohort-construction", 383,
        ["D:/KLTN/metadata/reports/cohort_flow.md", "D:/KLTN/metadata/reports/final_cohort_qc.md",
         "D:/KLTN/metadata/reports/training_manifest_summary.md"],
        ["Use the audited final cohort waterfall and exact RID-wise split; do not conflate L with p."])
    stages = [("899", "Đối tượng ADNI có MRI liên kết", "white"),
              ("843", "MCI tại baseline", "white"),
              ("631", "Không tiến triển sớm đến hết L", "time"),
              ("536", "Có theo dõi hợp lệ sau L", "time"),
              ("359", "Có ≥3 thời điểm MRI; chọn đúng 3", "fusion")]
    for i, (count, label, color) in enumerate(stages):
        y = 12+i*52
        s.box(18, y, 418, 38, f"{count} đối tượng   |   {label}", color, 10)
        if i < len(stages)-1:
            s.line(227, y+38, 227, y+52)
    s.text(227, 273, "1 077 MRI = 359 đối tượng × 3 visits", 10, bold=True, align="center")
    s.box(18, 296, 201, 37, "106 events\nMMSE / CDR sau L", "out", 10)
    s.box(235, 296, 201, 37, "253 censored\nTheo dõi cuối sau L", "out", 10)
    s.text(227, 345, "RID-wise split: train 251  |  validation 54  |  test 54", 10, bold=True, align="center")
    s.text(227, 365, "Fit scaler, PCA và imputation trên train; áp dụng nguyên vẹn cho val/test.", 9.5, align="center")
    s.save()


def preprocessing():
    s = Scene("modality-preprocessing", 300,
        ["D:/KLTN/ARCHITECTURE_AUDIT_20260919.md", "D:/KLTN/phase_05b_pairwise_medicalnet_source.zip",
         "D:/KLTN/pileline.drawio"],
        ["Correct radiomics to 16 PCA inputs and clinical to nine values plus nine observedness masks.",
         "Use exact encoder dimensions and ±90-day matching rather than prospective-only availability."])
    s.text(15, 8, "INPUT", 10, bold=True)
    s.text(109, 8, "PREPROCESSING", 10, bold=True)
    s.text(261, 8, "ENCODER", 10, bold=True)
    rows = [(40, "T1 MRI", "RAS; SynthStrip\nRigid registration\n144³, 1.5 mm; z-score", "MedicalNet\nResNet18\n512 → 128", "M\n128", "m"),
            (123, "Radiomics\n107 features", "Loại 3 hằng số\nTrain scaling + PCA\n16 thành phần", "MLP\n16 → 128 → 64", "R\n64", "r"),
            (206, "Clinical\n9 values\n9 masks", "Nearest valid ±90 d\nTrain median + scaling\nMask: 1 = observed", "MLP\n18 → 64 → 64", "C\n64", "c")]
    for y, label, prep, encoder, output, color in rows:
        s.box(15, y, 76, 62, label, color)
        s.box(109, y, 135, 62, prep, color, 9.5, bold_first=False)
        s.box(262, y, 112, 62, encoder, color, 9.5)
        s.box(391, y+9, 47, 44, output, color, 10)
        for a, b in [(91, 109), (244, 262), (374, 391)]:
            s.line(a, y+31, b, y+31)
    s.text(15, 285, "Cùng encoder dùng cho cả 3 visits; chỉ train quyết định tham số tiền xử lý.", 9.5)
    s.save()


def evolution():
    s = Scene("architecture-evolution", 398,
        ["D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Preserve chronological development; CP follows the full outer-product model and RC pruning follows ablation."])
    stages = [("MRI Only", "Đặc trưng không gian", "m"),
              ("Longitudinal MRI", "Khai thác chuỗi 3 visits", "time"),
              ("Multimodal Concatenation", "Thêm thông tin R và C", "out"),
              ("Dynamic Pairwise Fusion", "MR, MC, RC; gated residual", "fusion"),
              ("CP-Factorized Pairwise Fusion", "Giảm tham số tensor trọng số", "pair"),
              ("Fusion Ablation", "Kiểm tra cơ chế và từng pair", "out"),
              ("RC-Free Pairwise Fusion", "Giữ 3 modalities; chỉ MR và MC", "fusion")]
    for i, (title, desc, color) in enumerate(stages):
        y = 9+i*55
        s.circle(30, y+23, 13, str(i+1), "white", 10)
        s.box(57, y, 378, 45, title+"\n"+desc, color, 10)
        if i < len(stages)-1:
            s.line(246, y+45, 246, y+55)
    s.save()


def full_graph():
    s = Scene("full-pairwise-graph", 337,
        ["D:/KLTN/pileline.drawio", "D:/KLTN/phase_05b_pairwise_medicalnet_source.zip"],
        ["Show all three pair blocks and six distinct directed residual contributions without crossing edges."])
    s.text(227, 7, "Full reference: 3 pair blocks, 6 directed routes", 10.5, bold=True, align="center")
    s.box(188, 36, 78, 42, "M\n128", "m")
    s.box(55, 106, 90, 42, "MR\nM × R", "pair")
    s.box(309, 106, 90, 42, "MC\nM × C", "pair")
    s.box(61, 203, 78, 42, "R\n64", "r")
    s.box(315, 203, 78, 42, "C\n64", "c")
    s.box(182, 270, 90, 42, "RC\nR × C", "pair")
    s.line(145, 112, 188, 65)
    s.line(309, 112, 266, 65)
    s.line(100, 148, 100, 203)
    s.line(354, 148, 354, 203)
    s.line(182, 277, 139, 238)
    s.line(272, 277, 315, 238)
    s.text(115, 65, "(MR → M)", 9.5, align="center")
    s.text(340, 65, "(MC → M)", 9.5, align="center")
    s.text(87, 168, "(MR → R)", 9.5, align="right")
    s.text(367, 168, "(MC → C)", 9.5)
    s.text(121, 279, "(RC → R)", 9.5, align="right")
    s.text(335, 279, "(RC → C)", 9.5)
    s.text(227, 170, "M/R/C là identity paths.\nMỗi arrow là đóng góp\nprojected × gate × λ.", 9.5, align="center")
    s.text(227, 322, "Pair features được xây dựng từ low projections của hai modality tương ứng.", 9.5, align="center")
    s.save()


def outer_cp():
    s = Scene("outer-vs-cp", 326,
        ["D:/KLTN/phase_05b_pairwise_medicalnet_source.zip",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["CP factorizes the first bilinear interaction weight tensor, retaining bias and identical post-MLP.",
         "Display controlled MR/MC/RC dimensions and ranks rather than suggesting patient-data decomposition."])
    s.text(112, 7, "FULL OUTER PRODUCT", 10, bold=True, align="center")
    s.text(342, 7, "CP-FACTORIZED WEIGHTS", 10, bold=True, align="center")
    s.line(227, 30, 227, 257, arrow=False, dashed=True, color="#B4BEC7")
    s.box(14, 37, 57, 34, "x\ndₓ", "m")
    s.box(150, 37, 57, 34, "y\ndᵧ", "r")
    s.box(56, 99, 112, 37, "x ⊗ y\ndₓ × dᵧ", "pair")
    s.path([(42, 71), (42, 118), (56, 118)])
    s.path([(178, 71), (178, 118), (168, 118)])
    s.box(31, 157, 161, 36, "Flatten + Linear\ndₓdᵧ → H", "pair")
    s.line(112, 136, 112, 157)
    s.box(32, 214, 159, 42, "Post-MLP (giữ nguyên)\nGELU · dropout · Linear · LN", "fusion", 9.5)
    s.line(112, 193, 112, 214)
    s.box(245, 37, 70, 34, "x → Aᵀx\nQ", "m")
    s.box(370, 37, 70, 34, "y → Bᵀy\nQ", "r")
    s.box(294, 99, 98, 37, "q = u ⊙ v\nQ", "pair")
    s.path([(280, 71), (280, 118), (294, 118)])
    s.path([(405, 71), (405, 118), (392, 118)])
    s.box(263, 157, 161, 36, "h = Oq + b\nQ → H", "pair")
    s.line(343, 136, 343, 157)
    s.box(264, 214, 159, 42, "Post-MLP (giữ nguyên)\nGELU · dropout · Linear · LN", "fusion", 9.5)
    s.line(343, 193, 343, 214)
    s.text(227, 272, "W ∈ ℝ^(H × dₓ × dᵧ) ≈ Σ o_q ⊗ a_q ⊗ b_q", 10, align="center")
    s.text(227, 291, "MR: 32 × 32, Q=8   |   MC: 32 × 16, Q=8   |   RC: 32 × 16, Q=4", 9.5, align="center")
    s.text(227, 309, "Thay tensor trọng số W; không phân rã MRI hay dữ liệu bệnh nhân.", 9.5, bold=True, align="center")
    s.save()


def gated_route():
    s = Scene("gated-residual-route", 406,
        ["D:/KLTN/residual gate MRI.drawio.png", "D:/KLTN/residual gate Radiomics.drawio.png",
         "D:/KLTN/residual gated clinical.drawio.png", "D:/KLTN/phase_05b_pairwise_medicalnet_source.zip"],
        ["Restore the explicit identity residual; distinguish directed projection, visit-specific scalar gate, and global unconstrained route scale.",
         "Gate input uses LN(original modality) and projected pair; λ initialized 0.1 without softplus."])
    s.box(16, 12, 128, 42, "Original modality\nU_d (identity)", "m")
    s.box(287, 12, 151, 42, "Pair feature\nE_p", "pair")
    s.box(287, 77, 151, 42, "Directed projection\nLinear + LN → Ê_(p→d)", "pair", 9.5)
    s.line(362, 54, 362, 77)
    s.box(16, 77, 128, 42, "Gate context\nLN(U_d)", "fusion")
    s.line(80, 54, 80, 77)
    s.box(178, 145, 260, 52, "Dynamic scalar gate g_(p→d)\nconcat[LN(U_d), Ê_(p→d)] → MLP → sigmoid\nRiêng từng đối tượng, visit và route", "fusion", 9.5)
    s.path([(144, 98), (162, 98), (162, 164), (178, 164)])
    s.path([(362, 119), (362, 145)])
    s.circle(362, 238, 14, "×", "fusion", 13)
    s.line(362, 197, 362, 224)
    s.path([(438, 98), (447, 98), (447, 238), (376, 238)])
    s.box(178, 216, 135, 44, "Global route scale λ\nLearnable; init 0.1", "fusion", 9.5)
    s.line(313, 238, 348, 238)
    s.text(434, 273, "λ × g × Ê", 10, bold=True, align="right")
    s.circle(227, 300, 14, "+", "fusion", 14)
    s.path([(16, 33), (7, 33), (7, 300), (213, 300)])
    s.path([(362, 252), (362, 300), (241, 300)])
    s.box(168, 332, 118, 38, "LayerNorm", "fusion")
    s.line(227, 314, 227, 332)
    s.box(313, 332, 125, 38, "Updated modality\nZ_d", "m", 9.5)
    s.line(286, 351, 313, 351)
    s.text(16, 387, "λ không bị ràng buộc dấu; U_d không qua thêm identity projection.", 9.5)
    s.save()


def rc_routes():
    s = Scene("rc-free-routing", 372,
        ["D:/KLTN/week12/Sơ đồ luồng residual A6 theo M, R, C.png",
         "D:/KLTN/week12/Bao_cao_tuan_12/image/week12/a6_residual_flow.png",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Correct the original diagram by drawing the identity path separately from gated interaction paths.",
         "Remove active RC→R and RC→C routes while retaining all three modality encoders."])
    rows = [(14, "M", "(MR → M)", "(MC → M)", "M_out\n128", "m"),
            (149, "R", "(MR → R)", None, "R_out\n64", "r"),
            (249, "C", "(MC → C)", None, "C_out\n64", "c")]
    for y, original, pair1, pair2, output, color in rows:
        s.box(16, y, 141, 31, original+"  (identity)", color)
        s.box(16, y+45, 141, 31, pair1+"  |  λ × g × Ê", "pair", 9.5)
        inputs = [y+15.5, y+60.5]
        if pair2:
            s.box(16, y+90, 141, 31, pair2+"  |  λ × g × Ê", "pair", 9.5)
            inputs.append(y+105.5)
        join = y+60.5 if pair2 else y+38
        s.circle(211, join, 14, "+", "fusion", 14)
        for i, py in enumerate(inputs):
            if abs(py-join) < 1:
                s.line(157, py, 197, join)
            else:
                dest = join-14 if py < join else join+14
                s.path([(157, py), (211, py), (211, dest)])
        s.box(250, join-17, 95, 34, "LayerNorm", "fusion", 9.5)
        s.line(225, join, 250, join)
        s.box(368, join-22, 69, 44, output, color)
        s.line(345, join, 368, join)
    s.box(16, 342, 421, 24, "RC pair đã bỏ; M, R, C và các identity paths vẫn được giữ.", "white", 9.5, bold_first=False, dashed=True)
    s.save()


def final_pipeline():
    s = Scene("final-pipeline", 515,
        ["D:/KLTN/pileline.drawio", "D:/KLTN/Untitled Diagram.drawio",
         "D:/KLTN/week12/Sơ đồ luồng residual A6 theo M, R, C.png",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Rebuild the main architecture with three retained modalities, MR/MC rank8 only, four gated routes and explicit identity paths.",
         "Display output128/64/64 → concat256 → readout128 → shared three-visit T-LSTM/attention/raw Cox log-risk."])
    s.text(16, 8, "1   XỬ LÝ TỪNG VISIT   (cùng trọng số cho 3 visits)", 10, bold=True)
    rows = [(35, "MRI", "MedicalNet\nResNet18", "M\n128", "m"),
            (99, "Radiomics\nPCA 16", "MLP\n16 → 128 → 64", "R\n64", "r"),
            (163, "Clinical\n9 + 9 masks", "MLP\n18 → 64 → 64", "C\n64", "c")]
    for y, inp, enc, feature, color in rows:
        s.box(16, y, 92, 46, inp, color)
        s.box(129, y, 120, 46, enc, color, 9.5)
        s.box(271, y, 64, 46, feature, color)
        s.line(108, y+23, 129, y+23)
        s.line(249, y+23, 271, y+23)
    s.box(361, 35, 77, 174, "M · R · C\n\nPer-visit\nfusion\n\nMR / MC\nCP rank 8\n\nNo RC", "fusion", 9.5)
    for y in (58, 122, 186):
        s.line(335, y, 361, y)
    s.text(16, 223, "2   CP PAIRWISE + DYNAMIC GATED RESIDUAL ROUTING", 10, bold=True)
    s.box(16, 246, 134, 52, "M_out 128\nM + (MR→M) + (MC→M)\nLayerNorm", "m", 9.5)
    s.box(160, 246, 134, 52, "R_out 64\nR + (MR→R)\nLayerNorm", "r", 9.5)
    s.box(304, 246, 134, 52, "C_out 64\nC + (MC→C)\nLayerNorm", "c", 9.5)
    s.path([(400, 209), (446, 209), (446, 234), (227, 234), (227, 246)])
    s.path([(227, 234), (83, 234), (83, 246)])
    s.path([(227, 234), (371, 234), (371, 246)])
    s.text(249, 318, "Mỗi route = λ × g × Ê", 9.5)
    s.box(99, 335, 118, 38, "Concatenate\n256", "fusion")
    s.box(243, 335, 128, 38, "Shared readout\n256 → 128", "fusion")
    s.line(217, 354, 243, 354)
    s.path([(83, 298), (83, 311), (158, 311), (158, 335)])
    s.path([(227, 298), (227, 311), (158, 311)], arrow=False)
    s.path([(371, 298), (371, 311), (227, 311)], arrow=False)
    s.text(129, 388, "3   LONGITUDINAL SURVIVAL", 10, bold=True)
    s.box(16, 410, 92, 52, "3 visit vectors\n128 mỗi visit\nΔt theo MRI", "time", 9.5)
    s.box(129, 410, 92, 52, "T-LSTM\nHidden 128", "time")
    s.box(242, 410, 91, 52, "Temporal\nattention\nΣ α_t h_t", "time", 9.5)
    s.box(354, 410, 84, 52, "Cox head\n128 → 64 → 1\nLog-risk η", "out", 9.5)
    s.path([(307, 373), (307, 380), (62, 380), (62, 410)])
    for a, b in [(108, 129), (221, 242), (333, 354)]:
        s.line(a, 436, b, 436)
    s.text(227, 477, "Huấn luyện bằng Cox partial likelihood (Breslow ties).", 9.5, align="center")
    s.text(227, 493, "Output là raw log-risk; không áp dụng sigmoid ở survival head.", 9.5, align="center")
    s.save()


def temporal():
    s = Scene("temporal-model", 301,
        ["D:/KLTN/phase_05b_pairwise_medicalnet_source.zip"],
        ["Use consecutive MRI time gaps, shared T-LSTM128, scalar additive attention and raw log-risk head."])
    for i, x in enumerate((27, 180, 333)):
        s.box(x, 12, 92, 38, f"Visit {i+1}\nx_{i+1} ∈ ℝ¹²⁸", "time")
        s.box(x, 86, 92, 42, f"T-LSTM\nh_{i+1} ∈ ℝ¹²⁸", "time")
        s.line(x+46, 50, x+46, 86)
        s.box(x, 163, 92, 38, f"Attention\nα_{i+1}", "time")
        s.line(x+46, 128, x+46, 163)
        if i < 2:
            s.line(x+92, 107, x+153, 107)
    s.text(150, 66, "Δt₂", 9.5, align="center")
    s.text(303, 66, "Δt₃", 9.5, align="center")
    s.box(105, 233, 141, 38, "z = Σ α_t h_t\nSoftmax theo visits", "time", 9.5)
    s.box(273, 233, 151, 38, "Cox head\nRaw log-risk η", "out")
    s.line(246, 252, 273, 252)
    s.path([(73, 201), (73, 219), (175, 219), (175, 233)])
    s.path([(226, 201), (226, 219), (175, 219)], arrow=False)
    s.path([(379, 201), (379, 219), (226, 219)], arrow=False)
    s.text(227, 285, "Δt₁ = 0; Δt₂, Δt₃ là khoảng cách giữa MRI liên tiếp (năm).", 9.5, align="center")
    s.save()


def topology():
    s = Scene("mri-hub-topology", 181,
        ["D:/KLTN/week12/Sơ đồ luồng residual A6 theo M, R, C.png",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Interpret MRI as the interaction hub while preserving radiomics and clinical; omit any active R-C edge."])
    s.box(16, 48, 113, 59, "Radiomics\nR", "r", 11)
    s.box(170, 48, 113, 59, "MRI\nM", "m", 11)
    s.box(324, 48, 113, 59, "Clinical\nC", "c", 11)
    s.line(129, 77, 170, 77, start_arrow=True)
    s.line(283, 77, 324, 77, start_arrow=True)
    s.text(150, 27, "MR", 10, bold=True, align="center")
    s.text(303, 27, "MC", 10, bold=True, align="center")
    s.text(227, 131, "Giữ đủ 3 modalities; không có direct radiomics-clinical pair.", 10, bold=True, align="center")
    s.text(227, 153, "Topology phản ánh lựa chọn mô hình qua validation và ablation.", 9.5, align="center")
    s.save()


def chart_sources(data, keys):
    return ["figures_source/results_data.json"] + [data["sources"][key] for key in keys]
def performance_chart(data):
    s = Scene("performance-evolution", 474, chart_sources(data, ["phase_evolution", "mri_initialization",
        "longitudinal_crossformer", "concat_official", "pairwise_official", "standardized_benchmark"]),
        ["Separate four protocol groups, including a separate concat Cox-batch8 panel; no connecting trend lines.",
         "Plot validation single-seed milestones only; flag incomplete attention provenance with a hollow marker."])
    titles = ["1  MRI Only: cùng protocol, khác initialization", "2  Longitudinal MRI: Cox batch 6",
              "3  Multimodal Concat.: Cox batch 8", "4  Pairwise family: Cox batch 6"]
    for panel, group in enumerate(data["evolution"]["groups"]):
        top = 9 + panel*106
        s.text(16, top, titles[panel], 10, bold=True)
        upper, lower = top+26, top+74
        def yy(value):
            return lower-(value-.70)/.18*(lower-upper)
        for tick in (.70, .80, .88):
            y = yy(tick)
            s.line(50, y, 438, y, arrow=False, color="#CFD5DB", width=.6)
            s.text(42, y-4, f"{tick:.2f}", 9.5, align="right")
        s.line(50, upper-1, 50, lower, arrow=False, width=.8)
        rows = group["rows"]
        span = 364/len(rows)
        for i, row in enumerate(rows):
            x, y = 61+span*(i+.5), yy(row["value"])
            color = "white" if row.get("marker") == "hollow" else ("fusion" if panel == 3 else "time")
            dot = s.circle(x, y, 3.7, color=color)
            if color != "white":
                dot["fill"] = dot["stroke"]
            plate = s.bar(x-20, y-18, 40, 13, "white")
            plate["stroke"] = "#FFFFFF"
            s.text(x, y-17, f"{row['value']:.4f}", 9.5, align="center")
            s.text(x, lower+7, row["label"], 9.5, align="center", width=span-3)
    s.text(16, 444, "Y: validation C-index. Tất cả điểm: seed 20260727; không nối các protocol.", 9.5)
    s.text(16, 461, "* Attention: best-observed; artifact hoàn tất còn hạn chế, ký hiệu rỗng.", 9.5)
    s.save()


def parameter_chart(data):
    p = data["parameters"]
    s = Scene("cp-parameter-reduction", 364, chart_sources(data, ["cp_architecture", "standardized_benchmark"]),
        ["Contrast the first bilinear-layer scope with total-model scope; use zero-origin linear axes.",
         "Do not present parameter counts as measured runtime, memory or FLOPs savings."])
    s.text(16, 9, "a  Ba first bilinear layers (MR, MC, RC; gồm bias)", 10, bold=True)
    core = p["first_bilinear_layers"]
    for y, label, count, color in [(44, "Full outer-product", core["full"], "pair"),
                                    (91, "CP-factorized", core["cp"], "fusion")]:
        s.text(16, y+8, label, 10)
        w = count/250000*270
        s.bar(155, y, w, 26, color)
        s.text(155+w+6, y+8, f"{count:,}", 9.5)
    for tick in (0, 100000, 200000):
        x = 155+tick/250000*270
        s.line(x, 124, x, 130, arrow=False)
        s.text(x, 134, f"{tick//1000}k", 9.5, align="center")
    s.line(155, 127, 425, 127, arrow=False, width=.8)
    s.text(16, 155, f"Giảm {core['reduction_percent']:.3f}% trong tensor trọng số tương tác đầu tiên.", 10, bold=True)
    s.text(16, 187, "b  Toàn bộ mô hình: backbone MRI chiếm phần lớn tham số", 10, bold=True)
    for row, y, color in zip(p["total_models"][:2], (222, 268), ("pair", "fusion")):
        s.text(16, y+8, "Full Pairwise" if y == 222 else "CP Pairwise", 10)
        w = row["value"]/40000000*270
        s.bar(155, y, w, 26, color)
        s.text(155+w+5, y+8, f"{row['value']/1000000:.3f} M", 9.5)
    s.line(155, 307, 425, 307, arrow=False, width=.8)
    for tick in (0, 10000000, 20000000, 30000000, 40000000):
        x = 155+tick/40000000*270
        s.line(x, 304, x, 310, arrow=False)
        s.text(x, 314, f"{tick//1000000}M", 9.5, align="center")
    s.text(16, 342, f"Giảm {p['total_full_to_cp_reduction_percent']:.3f}% tổng tham số; post-MLP giữ nguyên.", 10, bold=True)
    s.save()


def ablation_chart(data):
    ablation = data["ablations"]
    s = Scene("ablation-deltas", 346, chart_sources(data, ["ablation"]),
        ["Show six observed single-seed validation deltas against the same full-CP reference.",
         "Distinguish the fixed-lambda full-CP ablation from the later RC-free fixed-lambda sensitivity model."])
    s.text(16, 8, "Δ validation C-index so với Full CP Pairwise", 10.5, bold=True)
    zero = 218
    scale = 9500
    for tick in (-.01, 0, .01, .02):
        x = zero+tick*scale
        s.line(x, 32, x, 282, arrow=False, color="#D0D7DD", width=.7)
        s.text(x, 287, f"{tick:+.2f}" if tick else "0", 9.5, align="center")
    for i, row in enumerate(ablation["rows"]):
        if not math.isclose(row["value"]-ablation["baseline"], row["delta"], abs_tol=1e-12):
            raise ValueError("Audited ablation delta is inconsistent")
        y, endpoint = 42+i*40, zero+row["delta"]*scale
        s.text(16, y+7, row["label"], 10, bold=row["label"] == "Remove RC")
        s.bar(min(zero, endpoint), y, abs(endpoint-zero), 24,
              "fusion" if row["delta"] >= 0 else "out")
        s.text(endpoint+(6 if row["delta"] >= 0 else -6), y+7, f"{row['delta']:+.4f}", 9.5,
               bold=row["label"] == "Remove RC", align="left" if row["delta"] >= 0 else "right")
    s.line(zero, 32, zero, 282, arrow=False, width=1.15)
    s.text(16, 314, f"Reference = {ablation['baseline']:.6f}; seed {ablation['seed']}; cùng cohort/split.", 9.5)
    s.text(16, 331, "Δ từ một seed là bằng chứng khám phá; không phải kiểm định ý nghĩa thống kê.", 9.5)
    s.save()


def benchmark_chart(data):
    s = Scene("standardized-benchmark", 370, chart_sources(data, ["standardized_benchmark", "standardized_audit"]),
        ["Plot three-seed mean ± sample SD (ddof1), alongside individual seed values; SD is not a confidence interval.",
         "Use standardized validation only, leaving the deterministic post-selection classical baseline separate."])
    s.text(16, 9, "54 validation subjects  |  480 comparable pairs", 10, bold=True)
    s.text(439, 30, "Mean ± SD", 9.5, bold=True, align="right")
    xx = lambda value: 158+(value-.60)/.30*184
    for tick in (.60, .70, .80, .90):
        x = xx(tick)
        s.line(x, 53, x, 289, arrow=False, color="#D1D7DD", width=.7)
        s.text(x, 294, f"{tick:.2f}", 9.5, align="center")
    for i, row in enumerate(data["benchmark"]):
        y = 72+i*48
        s.text(16, y-4, row["label"].replace("–", "-"), 9.5, bold=row["label"] == "RC-Free Pairwise")
        s.line(xx(row["mean"]-row["sd"]), y, xx(row["mean"]+row["sd"]), y, arrow=False, width=1.5)
        for end in (row["mean"]-row["sd"], row["mean"]+row["sd"]):
            s.line(xx(end), y-5, xx(end), y+5, arrow=False)
        for j, value in enumerate(row["values"]):
            s.circle(xx(value), y+10, 2.5, color="white")
        dot = s.circle(xx(row["mean"]), y, 4, color="fusion")
        dot["fill"] = dot["stroke"]
        s.text(439, y-4, f"{row['mean']:.4f} ± {row['sd']:.4f}", 9.5, align="right")
    s.text(250, 314, "Validation C-index", 10, align="center")
    dot = s.circle(19, 344, 3.5, color="fusion")
    dot["fill"] = dot["stroke"]
    s.text(28, 339, "Mean ± sample SD", 9.5)
    s.circle(177, 344, 2.5, color="white")
    s.text(186, 339, "Seeds 20260727 / 28 / 29", 9.5)
    s.text(16, 357, "SD là độ biến thiên giữa 3 seeds; không phải confidence interval.", 9.5)
    s.save()


def charts(data):
    for draw in (performance_chart, parameter_chart, ablation_chart, benchmark_chart):
        draw(data)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--charts-only", action="store_true")
    args = parser.parse_args()
    register_fonts()
    OUT.mkdir(exist_ok=True)
    SRC.mkdir(exist_ok=True)
    if not args.charts_only:
        for draw in (timeline, taxonomy, cohort, preprocessing, evolution, full_graph,
                     outer_cp, gated_route, rc_routes, final_pipeline, temporal, topology):
            draw()
    data_file = SRC / "results_data.json"
    if data_file.exists():
        charts(json.loads(data_file.read_text(encoding="utf-8-sig")))
    previous = {}
    provenance_file = SRC / "figure_provenance.json"
    if provenance_file.exists():
        previous = json.loads(provenance_file.read_text(encoding="utf-8")).get("figures", {})
    provenance_file.write_text(json.dumps({"figures": {**previous, **PROVENANCE},
        "authoring": "Native draw.io XML is saved before vector exports. PDF/SVG rendering uses the same scene.",
        "style": {"width_mm": 160, "font": "Arial / DejaVu Sans", "colors": COLORS}},
        ensure_ascii=False, indent=2), encoding="utf-8")
if __name__ == "__main__":
    main()
