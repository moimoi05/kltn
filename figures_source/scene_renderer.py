"""Shared fonts and native draw.io/PDF/SVG scene renderer for 160-mm figures."""
from __future__ import annotations

import base64
import html
import math
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import quote
import zlib

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "image"
SRC = ROOT / "figures_source"
WIDTH = 453.5433  # 160 mm
INK = "#000000"
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
        if color.upper() != INK:
            raise ValueError("All diagram text must be black; use bold for emphasis.")
        item = {"kind": "text", "x": x, "y": y, "text": text, "size": size,
                "bold": bold, "align": align, "width": width, "color": color}
        self.items.append(item)
        for line in text.split("\n"):
            actual = text_width(line, size, bold)
            if width and actual > width + .2:
                self.text_checks.append(f"{self.name}: text exceeds width by {actual-width:.1f}: {line}")
        return item

    def cuboid(self, x, y, w, h, text="", color="m", size=10, depth=8, bold_first=True):
        """Three vector faces; x/y/w/h describe the complete visible bounds.

        Use for a 3D MRI volume, a 3D processing block, or a third-order weight
        tensor. Feature vectors remain ordinary rectangles.
        """
        if not 0 < depth < min(w, h) / 2:
            raise ValueError("Cuboid depth must fit inside both visible dimensions.")
        fill, stroke = COLORS[color]
        item = {"kind": "cuboid", "x": x, "y": y, "w": w, "h": h,
                "depth": depth, "text": text, "size": size, "bold_first": bold_first,
                "fill": fill, "top_fill": mix_color(fill, "#FFFFFF", .38),
                "side_fill": mix_color(fill, stroke, .22), "stroke": stroke,
                "id": f"n{len(self.items)+1}"}
        self.items.append(item)
        lines = text.split("\n") if text else []
        if len(lines) * size * 1.24 > h - depth - 8:
            self.text_checks.append(f"{self.name}: cuboid text exceeds front height: {text}")
        for i, line in enumerate(lines):
            if text_width(line, size, bold_first and i == 0) > w - depth - 10:
                self.text_checks.append(f"{self.name}: cuboid text exceeds front width: {line}")
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
            if kind == "cuboid":
                # A native editable stencil and label are grouped. The label
                # occupies only the front face, matching PDF/SVG exactly.
                attrs.update(vertex="1", value="", style="group;html=1;pointerEvents=0;")
                cell = ET.SubElement(root, "mxCell", attrs)
                ET.SubElement(cell, "mxGeometry", {"x": str(item["x"]), "y": str(item["y"]),
                    "width": str(item["w"]), "height": str(item["h"]), "as": "geometry"})
                body = ET.SubElement(root, "mxCell", {"id": attrs["id"]+"-body", "parent": attrs["id"],
                    "vertex": "1", "value": "", "style": base+
                    f"shape=stencil({cuboid_stencil(item)});fillColor={item['fill']};strokeColor={item['stroke']};strokeWidth=1;"})
                ET.SubElement(body, "mxGeometry", {"x": "0", "y": "0", "width": str(item["w"]),
                    "height": str(item["h"]), "as": "geometry"})
                lines = item["text"].split("\n")
                label = "<br>".join(("<b>"+html.escape(line)+"</b>") if i == 0 and item["bold_first"]
                    else html.escape(line) for i, line in enumerate(lines))
                label_cell = ET.SubElement(root, "mxCell", {"id": attrs["id"]+"-label", "parent": attrs["id"],
                    "vertex": "1", "value": label, "style": base+
                    f"text;strokeColor=none;fillColor=none;fontSize={item['size']};align=center;verticalAlign=middle;spacing=0;"})
                ET.SubElement(label_cell, "mxGeometry", {"x": "0", "y": str(item["depth"]),
                    "width": str(item["w"]-item["depth"]), "height": str(item["h"]-item["depth"]), "as": "geometry"})
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
            if kind == "cuboid":
                pdf.setStrokeColor(HexColor(item["stroke"]))
                pdf.setLineWidth(1)
                pdf.setDash([])
                for points, fill in cuboid_faces(item):
                    pdf.setFillColor(HexColor(fill))
                    path = pdf.beginPath()
                    path.moveTo(points[0][0], self.height-points[0][1])
                    for x, y in points[1:]:
                        path.lineTo(x, self.height-y)
                    path.close()
                    pdf.drawPath(path, stroke=1, fill=1)
                self._pdf_label(pdf, cuboid_front(item))
            elif kind in ("box", "circle"):
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
            if kind == "cuboid":
                for points, fill in cuboid_faces(item):
                    pts = " ".join(f"{x},{y}" for x, y in points)
                    svg.append(f'<polygon points="{pts}" fill="{fill}" stroke="{item["stroke"]}" stroke-width="1"/>')
                front = cuboid_front(item)
                lines = front["text"].split("\n")
                top = front["y"]+(front["h"]-len(lines)*front["size"]*1.24)/2+front["size"]*.15
                for i, label in enumerate(lines):
                    text(front["x"]+front["w"]/2, top+i*front["size"]*1.24, label,
                         front["size"], front["bold_first"] and i == 0, "center")
            elif kind == "box":
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
            "changes": self.corrections + ["Redrawn as native draw.io; unified vector style and physical font sizes.",
                "All labels, chart values and ticks use black text; emphasis uses font weight."],
            "rendering": "ReportLab/SVG fallback from the same scene; draw.io desktop CLI unavailable.",
            "width_mm": 160, "minimum_font_pt": min([item.get("size", 10) for item in self.items]),
            "height_pt": self.height, "text_color": INK,
            "cuboid_count": sum(item["kind"] == "cuboid" for item in self.items),
        }
        print(f"Created {self.name}: {self.width:.1f} x {self.height:.1f} pt")


def mix_color(first, second, fraction):
    channels = [round(int(first[i:i+2], 16)*(1-fraction)+int(second[i:i+2], 16)*fraction)
                for i in (1, 3, 5)]
    return "#"+"".join(f"{value:02X}" for value in channels)


def cuboid_faces(item):
    x, y, w, h, d = (item[key] for key in ("x", "y", "w", "h", "depth"))
    return [([(x, y+d), (x+d, y), (x+w, y), (x+w-d, y+d)], item["top_fill"]),
            ([(x+w-d, y+d), (x+w, y), (x+w, y+h-d), (x+w-d, y+h)], item["side_fill"]),
            ([(x, y+d), (x+w-d, y+d), (x+w-d, y+h), (x, y+h)], item["fill"])]


def cuboid_front(item):
    return {**item, "y": item["y"]+item["depth"],
            "w": item["w"]-item["depth"], "h": item["h"]-item["depth"]}


def cuboid_stencil(item):
    """Embed a draw.io custom shape using its documented URL/deflate/base64 codec."""
    shape = ET.Element("shape", {"name": "ThesisCuboid", "w": str(item["w"]),
        "h": str(item["h"]), "aspect": "variable", "strokewidth": "inherit"})
    ET.SubElement(shape, "background")
    foreground = ET.SubElement(shape, "foreground")
    for points, fill in cuboid_faces({**item, "x": 0, "y": 0}):
        ET.SubElement(foreground, "fillcolor", {"color": fill})
        path = ET.SubElement(foreground, "path")
        ET.SubElement(path, "move", {"x": str(points[0][0]), "y": str(points[0][1])})
        for x, y in points[1:]:
            ET.SubElement(path, "line", {"x": str(x), "y": str(y)})
        ET.SubElement(path, "close")
        ET.SubElement(foreground, "fillstroke")
    xml = ET.tostring(shape, encoding="unicode")
    encoded = quote(xml, safe="~()*!.'-_").encode("utf-8")
    compressor = zlib.compressobj(wbits=-15)
    payload = compressor.compress(encoded)+compressor.flush()
    return base64.b64encode(payload).decode("ascii")


def arrow_points(previous, tip):
    dx, dy = tip[0]-previous[0], tip[1]-previous[1]
    norm = math.hypot(dx, dy) or 1
    dx, dy = dx/norm, dy/norm
    return [tip, (tip[0]-5*dx+2.5*dy, tip[1]-5*dy-2.5*dx),
            (tip[0]-5*dx-2.5*dy, tip[1]-5*dy+2.5*dx)]
