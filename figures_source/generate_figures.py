"""Thesis figure declarations; charts use the separately audited results_data.json.

Shared fonts and vector rendering live in scene_renderer.py. Native draw.io is
saved first; PDF/SVG use the same scene when the desktop CLI is unavailable.
"""
from __future__ import annotations

import argparse
import json
import math

if __package__:
    from .scene_renderer import (
        COLORS, INK, LINE, OUT, PROVENANCE, ROOT, SRC, WIDTH, Scene,
        arrow_points, cuboid_faces, cuboid_front, cuboid_stencil,
        font_runs, mix_color, register_fonts, text_width,
    )
else:
    from scene_renderer import (
        COLORS, INK, LINE, OUT, PROVENANCE, ROOT, SRC, WIDTH, Scene,
        arrow_points, cuboid_faces, cuboid_front, cuboid_stencil,
        font_runs, mix_color, register_fonts, text_width,
    )

def timeline():
    s = Scene("mci-progression-timeline", 264,
        ["D:/KLTN/metadata/scripts/pipeline_common.py", "D:/KLTN/metadata/scripts/05_create_survival_labels.py",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Separate third-MRI prediction origin p from the 18-month eligibility landmark L.",
         "Show conditional eligibility through L and score-defined post-L outcomes; retain ±90-day clinical matching limitation.",
         "Draw the three volumetric MRI observations as 3D cuboids; tabular R/C remain labels."])
    s.text(18, 9, "Chọn 3 MRI trong cửa sổ 18 tháng: baseline ≤ s₁ < s₂ < s₃ ≤ L", 10, bold=True)
    for x, label in [(70, "T1 MRI\nVisit 1: s₁"), (160, "T1 MRI\nVisit 2: s₂"), (250, "T1 MRI\nVisit 3: p")]:
        s.cuboid(x-39, 40, 78, 43, label, "m", 9.5, depth=7)
        s.text(x, 91, "+ R + C", 9.5, align="center")
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
    s.save()


def taxonomy():
    s = Scene("fusion-taxonomy", 294,
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
    s.save()


def cohort():
    s = Scene("cohort-construction", 367,
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
    s.save()


def preprocessing():
    s = Scene("modality-preprocessing", 280,
        ["D:/KLTN/ARCHITECTURE_AUDIT_20260919.md", "D:/KLTN/phase_05b_pairwise_medicalnet_source.zip",
         "D:/KLTN/pileline.drawio"],
        ["Correct radiomics to 16 PCA inputs and clinical to nine values plus nine observedness masks.",
         "Use exact encoder dimensions and ±90-day matching rather than prospective-only availability.",
         "MRI volume and its spatial preprocessing/3D encoder use cuboids; final 128-D embedding is a vector."])
    s.text(15, 8, "INPUT", 10, bold=True)
    s.text(109, 8, "PREPROCESSING", 10, bold=True)
    s.text(261, 8, "ENCODER", 10, bold=True)
    rows = [(40, "T1 MRI\n3D volume", "RAS; SynthStrip\nRigid registration\n144³, 1.5 mm; z-score", "MedicalNet\n3D ResNet18\nGAP 512 → 128", "M\n128", "m"),
            (123, "Radiomics\n107 features", "Loại 3 hằng số\nTrain scaling + PCA\n16 thành phần", "MLP\n16 → 128 → 64", "R\n64", "r"),
            (206, "Clinical\n9 values\n9 masks", "Nearest valid ±90 d\nTrain median + scaling\nMask: 1 = observed", "MLP\n18 → 64 → 64", "C\n64", "c")]
    for y, label, prep, encoder, output, color in rows:
        draw = s.cuboid if color == "m" else s.box
        draw(15, y, 76, 62, label, color)
        draw(109, y, 135, 62, prep, color, 9.5, bold_first=False)
        draw(262, y, 112, 62, encoder, color, 9.5)
        s.box(391, y+9, 47, 44, output, color, 10)
        for a, b in [(91, 109), (244, 262), (374, 391)]:
            s.line(a, y+31, b, y+31)
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
    s = Scene("full-pairwise-graph", 324,
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
    s.save()


def outer_cp():
    s = Scene("outer-vs-cp", 304,
        ["D:/KLTN/phase_05b_pairwise_medicalnet_source.zip",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["CP factorizes the first bilinear interaction weight tensor, retaining bias and identical post-MLP.",
         "Display controlled MR/MC/RC dimensions and ranks rather than suggesting patient-data decomposition.",
         "Show the third-order weight tensor as a sum of 3D rank-one tensors, with explicit factor matrices A/B/O."])
    s.text(227, 7, "PHÂN RÃ CP CỦA TENSOR TRỌNG SỐ W", 10.5, bold=True, align="center")
    s.text(227, 19, "Mỗi W_q = o_q ⊗ a_q ⊗ b_q là một tensor hạng 1", 9.5, align="center")
    for x, w, label, color in [(20, 67, "W", "pair"), (132, 70, "W₁", "fusion"),
                                (243, 70, "W₂", "fusion"), (371, 66, "W_Q", "fusion")]:
        s.cuboid(x, 31, w, 55, label, color, 12, depth=10)
    s.text(107, 48, "≈", 15, align="center")
    s.text(222, 48, "+", 15, align="center")
    s.text(328, 48, "+", 14, align="center")
    s.text(344, 48, "…", 14, align="center")
    s.text(359, 48, "+", 12, align="center")
    s.text(53, 94, "H × dₓ × dᵧ", 9.5, align="center")
    s.text(167, 94, "o₁ ⊗ a₁ ⊗ b₁", 9.5, align="center")
    s.text(278, 94, "o₂ ⊗ a₂ ⊗ b₂", 9.5, align="center")
    s.text(404, 94, "o_Q ⊗ a_Q ⊗ b_Q", 9.5, align="center")
    s.box(15, 115, 131, 29, "A: dₓ × Q", "m", 10)
    s.box(161, 115, 131, 29, "B: dᵧ × Q", "r", 10)
    s.box(307, 115, 131, 29, "O: H × Q", "fusion", 10)
    s.text(112, 158, "FULL OUTER PRODUCT", 10, bold=True, align="center")
    s.text(342, 158, "CP-FACTORIZED WEIGHTS", 10, bold=True, align="center")
    s.line(227, 157, 227, 285, arrow=False, dashed=True, color="#B4BEC7")
    s.box(15, 177, 83, 28, "x: dₓ", "m", 10)
    s.box(132, 177, 83, 28, "y: dᵧ", "r", 10)
    s.path([(56, 205), (56, 212), (112, 212), (112, 219)])
    s.path([(174, 205), (174, 212), (112, 212)], arrow=False)
    s.box(15, 219, 200, 33, "x ⊗ y → Flatten + Linear\ndₓdᵧ → H (gồm bias b)", "pair", 9.5)
    s.box(15, 259, 200, 33, "Post-MLP (giữ nguyên)\nGELU · dropout · Linear · LN", "fusion", 9.5)
    s.line(112, 252, 112, 259)
    s.box(244, 177, 91, 28, "u = Aᵀx: Q", "m", 9.5)
    s.box(347, 177, 91, 28, "v = Bᵀy: Q", "r", 9.5)
    s.path([(289, 205), (289, 212), (342, 212), (342, 219)])
    s.path([(393, 205), (393, 212), (342, 212)], arrow=False)
    s.box(244, 219, 194, 33, "h = O(u ⊙ v) + b\nQ → H", "pair", 9.5)
    s.box(244, 259, 194, 33, "Post-MLP (giữ nguyên)\nGELU · dropout · Linear · LN", "fusion", 9.5)
    s.line(342, 252, 342, 259)
    s.save()


def gated_route():
    s = Scene("gated-residual-route", 382,
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
    s.save()


def rc_routes():
    s = Scene("rc-free-routing", 337,
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
    s.save()


def final_pipeline():
    s = Scene("final-pipeline", 474,
        ["D:/KLTN/pileline.drawio", "D:/KLTN/Untitled Diagram.drawio",
         "D:/KLTN/week12/Sơ đồ luồng residual A6 theo M, R, C.png",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Rebuild the main architecture with three retained modalities, MR/MC rank8 only, four gated routes and explicit identity paths.",
         "Display output128/64/64 → concat256 → readout128 → shared three-visit T-LSTM/attention/raw Cox log-risk.",
         "Use 3D cuboids for the MRI volume and 3D encoder, retaining 2D vector branches for M/R/C and temporal embeddings."])
    s.text(16, 8, "1   XỬ LÝ TỪNG VISIT   (cùng trọng số cho 3 visits)", 10, bold=True)
    rows = [(35, "T1 MRI 3D\n1 × 144³", "MedicalNet\n3D ResNet18", "M\n128", "m"),
            (99, "Radiomics\nPCA 16", "MLP\n16 → 128 → 64", "R\n64", "r"),
            (163, "Clinical\n9 + 9 masks", "MLP\n18 → 64 → 64", "C\n64", "c")]
    for y, inp, enc, feature, color in rows:
        draw = s.cuboid if color == "m" else s.box
        draw(16, y, 92, 46, inp, color, 9.5)
        draw(129, y, 120, 46, enc, color, 9.5)
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
    s.save()


def temporal():
    s = Scene("temporal-model", 283,
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
    s.save()


def topology():
    s = Scene("mri-hub-topology", 95,
        ["D:/KLTN/week12/Sơ đồ luồng residual A6 theo M, R, C.png",
         "D:/KLTN/week12/thesis_phase_evolution_bundle_20261005_final.zip"],
        ["Interpret MRI as the interaction hub while preserving radiomics and clinical; omit any active R-C edge.",
         "Lower MR/MC toward the arrows: top-to-arrow gap 17 pt instead of 50 pt; trim the empty margins."])
    s.box(16, 18, 113, 59, "Radiomics\nR", "r", 11)
    s.box(170, 18, 113, 59, "MRI\nM", "m", 11)
    s.box(324, 18, 113, 59, "Clinical\nC", "c", 11)
    s.line(129, 47, 170, 47, start_arrow=True)
    s.line(283, 47, 324, 47, start_arrow=True)
    s.text(150, 30, "MR", 10, bold=True, align="center")
    s.text(303, 30, "MC", 10, bold=True, align="center")
    s.save()


def chart_sources(data, keys):
    return ["figures_source/results_data.json"] + [data["sources"][key] for key in keys]
def performance_chart(data):
    s = Scene("performance-evolution", 458, chart_sources(data, ["phase_evolution", "mri_initialization",
        "longitudinal_crossformer", "concat_official", "pairwise_official", "standardized_benchmark"]),
        ["Separate four protocol groups, including a separate concat Cox-batch8 panel; no connecting trend lines.",
         "Plot validation single-seed milestones only; flag incomplete attention provenance with a hollow marker."])
    titles = ["1  MRI Only: cùng protocol, khác initialization", "2  Longitudinal MRI: Cox batch 6",
              "3  Multimodal Concat.: Cox batch 8", "4  Pairwise family: Cox batch 6"]
    s.text(16, 7, "Validation C-index", 9.5)
    for panel, group in enumerate(data["evolution"]["groups"]):
        top = 25 + panel*106
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
    s.save()


def parameter_chart(data):
    p = data["parameters"]
    s = Scene("cp-parameter-reduction", 313, chart_sources(data, ["cp_architecture", "standardized_benchmark"]),
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
    s.text(16, 162, "b  Toàn bộ mô hình: backbone MRI chiếm phần lớn tham số", 10, bold=True)
    for row, y, color in zip(p["total_models"][:2], (197, 243), ("pair", "fusion")):
        s.text(16, y+8, "Full Pairwise" if y == 197 else "CP Pairwise", 10)
        w = row["value"]/40000000*270
        s.bar(155, y, w, 26, color)
        s.text(155+w+5, y+8, f"{row['value']/1000000:.3f} M", 9.5)
    s.line(155, 282, 425, 282, arrow=False, width=.8)
    for tick in (0, 10000000, 20000000, 30000000, 40000000):
        x = 155+tick/40000000*270
        s.line(x, 279, x, 285, arrow=False)
        s.text(x, 289, f"{tick//1000000}M", 9.5, align="center")
    s.save()


def ablation_chart(data):
    ablation = data["ablations"]
    s = Scene("ablation-deltas", 310, chart_sources(data, ["ablation"]),
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
    s.save()


def benchmark_chart(data):
    s = Scene("standardized-benchmark", 337, chart_sources(data, ["standardized_benchmark", "standardized_audit"]),
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
    dot = s.circle(19, 35, 3.5, color="fusion")
    dot["fill"] = dot["stroke"]
    s.text(28, 30, "Mean ± sample SD", 9.5)
    s.circle(177, 35, 2.5, color="white")
    s.text(186, 30, "Seeds 20260727 / 28 / 29", 9.5)
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
        "style": {"width_mm": 160, "font": "Arial / DejaVu Sans", "text_color": INK,
                  "colors": COLORS, "volume_primitive": "Three-face native editable cuboid stencil",
                  "annotation_policy": "Explanatory footer notes are in LaTeX captions; axes, marker legends and internal labels remain in drawings."}},
        ensure_ascii=False, indent=2), encoding="utf-8")
if __name__ == "__main__":
    main()
