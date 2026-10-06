# Compile instructions

Official title: **Longitudinal Learning with Tensor Fusion for Predicting Progression of Alzheimer’s Disease**.

The source uses XeTeX, `fontspec`, numeric `natbib`, and BibTeX with `unsrtnat`. Biber is not required. All figures are supplied as vector PDF and can be included without running a diagram editor or Python. Build from the directory containing `main.tex`.

## Windows

With Tectonic on PATH:

```powershell
./build.ps1
```

For a portable executable:

```powershell
./build.ps1 -TectonicPath 'C:\path\to\tectonic.exe'
```

Tectonic fetches required TeX resources on its first build. It automatically runs BibTeX and repeats TeX until references stabilize. On Windows, `build.ps1` creates a local `.build/fontconfig.conf` for the Windows Fonts directory if no fontconfig file is already configured. Its warnings about absolute system-font paths describe portability; fonts are embedded in the finished PDF.

## XeLaTeX / Overleaf / Linux / macOS

Select **XeLaTeX**, not pdfLaTeX. Use a current TeX Live or MiKTeX with the packages referenced in `main.tex`.

```bash
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Alternatively, run `bash build.sh` or `latexmk -xelatex main.tex`.

The manuscript uses Times New Roman when available, with Tinos and TeX Gyre Termes fallbacks. Sans-serif text uses Arial or TeX Gyre Heros; monospace text uses Consolas or Latin Modern Mono. Fonts are not redistributed in this package. Line/page breaks can change slightly with a fallback font; recheck the page limit after changing fonts or text.

## Output and figure source

`main.pdf` is the compiler output. The build scripts also copy it to `Nguyen_Phuong_Nam_Thesis_RCFree_Revised.pdf`.

To redraw the diagrams/charts, install Python packages `reportlab`, `matplotlib`, `Pillow` and run:

```bash
python figures_source/generate_figures.py
```

The generator reads `figures_source/results_data.json`, writes editable `.drawio` scene files and vector PDF/SVG exports, and preserves the unified style through `figures_source/scene_renderer.py`. Figure text is black; colors apply to fills/strokes. The shared renderer supplies 3D cuboids for volumetric MRI and CP weight tensors, including native editable drawio stencils. The `.drawio` source is editable in diagrams.net. Automatic exports in this revision use the shared Python scene renderer because draw.io Desktop was unavailable; changing a `.drawio` manually does not automatically update its paired Python scene.

For the optional automated QA script, install `pypdf` and `PyMuPDF`, then run `python scripts/qa_thesis.py` after a successful build. The checks include pure black figure text in PDF/SVG/drawio and 3D volume/weight-tensor representations. Recheck the LaTeX log, all pages and all figure labels after editing. Numerical chart changes must remain linked to an actual experimental report, not manually invented values. Figure rendering/source syntax is also checked in `QUALITY_CHECK.md`; a fresh visual review is required after content or font changes.
