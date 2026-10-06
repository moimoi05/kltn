#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if command -v tectonic >/dev/null 2>&1; then
    tectonic --keep-logs --keep-intermediates main.tex
else
    xelatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    xelatex -interaction=nonstopmode -halt-on-error main.tex
    xelatex -interaction=nonstopmode -halt-on-error main.tex
fi
cp main.pdf Nguyen_Phuong_Nam_Thesis_RCFree_Revised.pdf
