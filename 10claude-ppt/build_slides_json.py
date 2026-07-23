"""
Build slides.json for VDMOS TID Defense PPT (74 slides).
Generates structured slides.json for agent-slides render command.
"""
import json
import os

BASE = r"E:\仿真数据处理\答辩\PPT制作交付包"
OUT = r"E:\仿真数据处理\答辩\PPT制作交付包\10claude-ppt\slides.json"

# ─── layout constants ─────────────────────────────────────────────────────────
W, H = 10.0, 5.625          # slide dimensions
TL, TT, TW, TH = 0.3, 0.12, 9.4, 0.88   # title
CL, CT, CW, CH = 0.4, 1.15, 9.2, 4.1    # full content
LL, LT, LW, LH = 0.4, 1.15, 4.5, 4.0   # left half
RL, RT, RW, RH = 5.05, 1.15, 4.65, 4.0 # right half
FL, FT, FW, FH = 0.4, 5.22, 9.2, 0.35  # footer

# ─── colors ───────────────────────────────────────────────────────────────────
BLUE   = "4472C4"   # primary / S-group
ORANGE = "ED7D31"   # accent / T-group
DARK   = "1F3864"   # dark title background alternative
GRAY   = "595959"   # subtitle / body
LGRAY  = "A6A6A6"   # light text
RED    = "C00000"   # warning/limit
GREEN  = "375623"   # positive finding
WHITE  = "FFFFFF"
BLACK  = "000000"

# ─── op helpers ───────────────────────────────────────────────────────────────
def add_slide(idx, layout=0):
    return {"op": "add_slide", "layout_index": layout}

def title(idx, text, *, size=24, color=BLUE, bold=True):
    return {"op": "add_text", "slide_index": idx, "text": text,
            "left": TL, "top": TT, "width": TW, "height": TH,
            "font_size": size, "bold": bold, "color": color, "wrap": True}

def body(idx, text, *, l=CL, t=CT, w=CW, h=CH,
         size=15, color=DARK, bold=False):
    return {"op": "add_text", "slide_index": idx, "text": text,
            "left": l, "top": t, "width": w, "height": h,
            "font_size": size, "bold": bold, "color": color, "wrap": True}

def label(idx, text, *, l, t, w, h, size=13, color=GRAY, bold=False):
    return {"op": "add_text", "slide_index": idx, "text": text,
            "left": l, "top": t, "width": w, "height": h,
            "font_size": size, "bold": bold, "color": color, "wrap": True}

def img(idx, rel_path, *, l, t, w=None, h=None):
    path = os.path.join(BASE, rel_path) if not os.path.isabs(rel_path) else rel_path
    op = {"op": "add_image", "slide_index": idx, "path": path, "left": l, "top": t}
    if w: op["width"] = w
    if h: op["height"] = h
    return op

def notes(idx, text):
    return {"op": "set_speaker_notes", "slide_index": idx, "text": text}

def divider_line(idx):
    """Horizontal rule under the title."""
    return {"op": "add_line_shape", "slide_index": idx,
            "x1": TL, "y1": TT+TH+0.03, "x2": TL+TW, "y2": TT+TH+0.03,
            "color": BLUE, "width_pt": 1.5}

def img_left(idx, rel, *, w=4.5, h=3.9):
    return img(idx, rel, l=LL, t=LT, w=w, h=h)

def img_right(idx, rel, *, w=4.6, h=3.9):
    return img(idx, rel, l=RL, t=RT, w=w, h=h)

def text_left(idx, text, *, size=15, color=DARK):
    return body(idx, text, l=LL, t=LT, w=LW, h=LH, size=size, color=color)

def text_right(idx, text, *, size=15, color=DARK):
    return body(idx, text, l=RL, t=RT, w=RW, h=RH, size=size, color=color)

def section_header(idx, section_title, subtitle=""):
    ops = [
        {"op": "add_text", "slide_index": idx, "text": section_title,
         "left": 0.5, "top": 1.8, "width": 9.0, "height": 1.2,
         "font_size": 32, "bold": True, "color": WHITE, "wrap": True},
    ]
    if subtitle:
        ops.append({"op": "add_text", "slide_index": idx, "text": subtitle,
                    "left": 0.5, "top": 3.0, "width": 9.0, "height": 0.7,
                    "font_size": 18, "bold": False, "color": "D9D9D9", "wrap": True})
    return ops

def two_col_headers(idx, left_h, right_h, *, size=16, color=BLUE):
    return [
        label(idx, left_h,  l=LL, t=LT,      w=LW, h=0.35, size=size, color=color, bold=True),
        label(idx, right_h, l=RL, t=RT,      w=RW, h=0.35, size=size, color=color, bold=True),
    ]

def conclusion_box(idx, text, *, l=CL, t=4.6, w=CW, h=0.55,
                    bg=ORANGE, fg=WHITE, size=14):
    return [
        {"op": "add_text", "slide_index": idx, "text": text,
         "left": l, "top": t, "width": w, "height": h,
         "font_size": size, "bold": True, "color": fg, "wrap": True,
         "background_color": bg}
    ]

def footer_note(idx, text, size=10):
    return label(idx, text, l=FL, t=FT, w=FW, h=FH, size=size, color=LGRAY)

# ─── image path shortcuts ──────────────────────────────────────────────────────
def p03(f): return os.path.join(BASE, "03_实验结果", f)
def p03e(f): return os.path.join(BASE, "03_实验结果", "可编辑图表", f)
def p04s(f): return os.path.join(BASE, "04_T器件仿真", "simulation", f)
def p04c(f): return os.path.join(BASE, "04_T器件仿真", "comparison", f)
def p04r(f): return os.path.join(BASE, "04_T器件仿真", f)
def p05f(f): return os.path.join(BASE, "05_S器件仿真", "七剂量转移", "figures", f)
def p05e(f): return os.path.join(BASE, "05_S器件仿真", "低压电场", "figures", f)
def p02(f): return os.path.join(BASE, "02_背景与结构", f)
def p06(f): return os.path.join(BASE, "06_AI辅助流程", f)
OLD = "S_T_VDMOS_TID_完整成果展示版_讲稿版_"
def pold(n): return p03(f"{OLD}{n}.png")

# ─── plan slides list ─────────────────────────────────────────────────────────
PLAN_SLIDES = [
    # Part 1: Background & Methods  (1-10)
    {"slide_number": 1,  "archetype_id": "title_slide",    "action_title": "Trench 与 SGT VDMOS 总剂量辐照效应对比及 TCAD 建模验证", "story_role": "cover"},
    {"slide_number": 2,  "archetype_id": "content_bullets", "action_title": "高辐射环境会持续改变功率 MOS 器件的关键电学参数",  "story_role": "context"},
    {"slide_number": 3,  "archetype_id": "two_column",      "action_title": "TCAD 将长周期辐照实验转化为可迭代、可解释的模型研究", "story_role": "context"},
    {"slide_number": 4,  "archetype_id": "content_bullets", "action_title": "已有研究建立了 TID 机制框架，但结构对比与统一验证仍需具体样品证据", "story_role": "context"},
    {"slide_number": 5,  "archetype_id": "table",           "action_title": "三篇 TID 文献分别支撑机制、结构比较与 TCAD 分析",  "story_role": "context"},
    {"slide_number": 6,  "archetype_id": "content_bullets", "action_title": "研究闭环从真实测量延伸到两类器件的可追溯 TCAD 验证", "story_role": "context"},
    {"slide_number": 7,  "archetype_id": "content_bullets", "action_title": "六只器件在七个剂量点进行同器件纵向跟踪",           "story_role": "context"},
    {"slide_number": 8,  "archetype_id": "two_column",      "action_title": "Trench 与 SGT 通过不同沟槽电极和氧化层布局控制沟道与漂移区电场", "story_role": "context"},
    {"slide_number": 9,  "archetype_id": "process_flow",    "action_title": "统一算法从原始曲线重新提取 Vth、gm、SS 与输出指标", "story_role": "context"},
    {"slide_number": 10, "archetype_id": "content_bullets", "action_title": "六只器件的七剂量曲线共同显示阈值负移与开启能力下降", "story_role": "key_finding"},
    # Part 2: Transfer characteristics  (11-25)
    {"slide_number": 11, "archetype_id": "content_bullets", "action_title": "S1：七剂量转移曲线显示稳定负移与开启区斜率下降",  "story_role": "evidence"},
    {"slide_number": 12, "archetype_id": "content_bullets", "action_title": "S2：阈值负移幅度与 S1 接近，组内一致性较好",       "story_role": "evidence"},
    {"slide_number": 13, "archetype_id": "content_bullets", "action_title": "S3：跨导下降略大，但阈值负移仍与 S 组高度一致",    "story_role": "evidence"},
    {"slide_number": 14, "archetype_id": "content_bullets", "action_title": "T1：阈值负移超过 10 V，亚阈区明显展开",            "story_role": "evidence"},
    {"slide_number": 15, "archetype_id": "content_bullets", "action_title": "T2：跨导下降最大，阈值与 SS 仍保持 T 组共同趋势",  "story_role": "evidence"},
    {"slide_number": 16, "archetype_id": "content_bullets", "action_title": "T3：三只 T 器件均进入约 1.6–1.7 V/dec 的高 SS 区间", "story_role": "evidence"},
    {"slide_number": 17, "archetype_id": "content_bullets", "action_title": "60 krad 时两组 gm 均下降约 60%，但 Vth 与 SS 的退化幅度不同", "story_role": "key_finding"},
    {"slide_number": 18, "archetype_id": "two_column",      "action_title": "S 组转移曲线随剂量稳定负移，三只器件保持高度一致", "story_role": "evidence"},
    {"slide_number": 19, "archetype_id": "table",           "action_title": "S 组七剂量指标给出连续、可复核的退化轨迹",         "story_role": "evidence"},
    {"slide_number": 20, "archetype_id": "two_column",      "action_title": "T 组阈值负移接近 10 V，亚阈区在中高剂量快速恶化", "story_role": "evidence"},
    {"slide_number": 21, "archetype_id": "table",           "action_title": "T 组七剂量指标显示 Vth 与 SS 的退化快于输出漏电变化", "story_role": "evidence"},
    {"slide_number": 22, "archetype_id": "content_bullets", "action_title": "两组 gm 均下降约 60%，说明开启能力衰减是共同退化维度", "story_role": "key_finding"},
    {"slide_number": 23, "archetype_id": "content_bullets", "action_title": "T 组 SS 增量约为 S 组的 10.8 倍，亚阈区差异最显著", "story_role": "key_finding"},
    {"slide_number": 24, "archetype_id": "two_column",      "action_title": "SGT 组阈值负移更小，Trench 组在 20 krad 后平均 Vth 已转为负值", "story_role": "key_finding"},
    {"slide_number": 25, "archetype_id": "two_column",      "action_title": "本批结果提示 SGT 的电极与氧化层布局提高了转移特性的 TID 稳定性", "story_role": "key_finding"},
    # Part 3: Output & rescan  (26-40)
    {"slide_number": 26, "archetype_id": "content_bullets", "action_title": "输出曲线需同时区分低压漏电、高压代理指标与仪器限流", "story_role": "context"},
    {"slide_number": 27, "archetype_id": "content_bullets", "action_title": "六只器件的输出响应呈现明显组间差异与非单调细节",  "story_role": "evidence"},
    {"slide_number": 28, "archetype_id": "content_bullets", "action_title": "S1：60 krad 的 30 V 漏电增幅为 1749%，高压代理降至 36 V", "story_role": "evidence"},
    {"slide_number": 29, "archetype_id": "content_bullets", "action_title": "S2：三只 S 器件中 30 V 漏电相对增幅最大",          "story_role": "evidence"},
    {"slide_number": 30, "archetype_id": "content_bullets", "action_title": "S3：相对增幅较低，但高压代理同样降至约 35 V",       "story_role": "evidence"},
    {"slide_number": 31, "archetype_id": "content_bullets", "action_title": "T1：低压漏电仅小幅增加，高压代理保持在 108 V",     "story_role": "evidence"},
    {"slide_number": 32, "archetype_id": "content_bullets", "action_title": "T2：30 V 漏电增幅为 58.9%，高压代理为 109 V",      "story_role": "evidence"},
    {"slide_number": 33, "archetype_id": "content_bullets", "action_title": "T3：三只 T 器件的 60 krad 输出指标集中在同一区间",  "story_role": "evidence"},
    {"slide_number": 34, "archetype_id": "content_bullets", "action_title": "S 组首扫尖峰在复扫中消失，表现出明显的扫描后恢复", "story_role": "key_finding"},
    {"slide_number": 35, "archetype_id": "two_column",      "action_title": "S/T 输出指标给出相反的高压代理变化方向",           "story_role": "key_finding"},
    {"slide_number": 36, "archetype_id": "content_bullets", "action_title": "13 条 S 组复扫的 30 V 漏电全部降低 70.65%–96.19%", "story_role": "evidence"},
    {"slide_number": 37, "archetype_id": "two_column",      "action_title": "S3 60 krad 案例显示恢复并非单点变化，而覆盖较宽电压范围", "story_role": "evidence"},
    {"slide_number": 38, "archetype_id": "process_flow",    "action_title": "高场扫描可能通过陷阱电荷释放与重分布形成表观恢复", "story_role": "insight"},
    {"slide_number": 39, "archetype_id": "two_column",      "action_title": "SGT 与 Trench 的输出响应方向相反，说明结构敏感区并不相同", "story_role": "key_finding"},
    {"slide_number": 40, "archetype_id": "content_bullets", "action_title": "SGT 的厚氧化层与屏蔽电极可能增强辐照电荷对漂移区电场的影响", "story_role": "insight"},
    # Part 4: T-device TCAD  (41-53)
    {"slide_number": 41, "archetype_id": "content_bullets", "action_title": "T 器件结构、网格和基础参数固定，剂量只改变陷阱参数", "story_role": "method"},
    {"slide_number": 42, "archetype_id": "two_column",      "action_title": "低参数 Not/Nit 剂量函数把七个剂量点映射到同一模型", "story_role": "method"},
    {"slide_number": 43, "archetype_id": "two_column",      "action_title": "Not 主导阈值静电位移，Nit 用于约束亚阈区与栅控退化", "story_role": "method"},
    {"slide_number": 44, "archetype_id": "two_column",      "action_title": "T 组七剂量转移仿真复现阈值负移主趋势",             "story_role": "evidence"},
    {"slide_number": 45, "archetype_id": "big_number",      "action_title": "T 模型对 ΔVth 与 gm 达到稳定的范围内定量一致性",   "story_role": "key_finding"},
    {"slide_number": 46, "archetype_id": "two_column",      "action_title": "SS 残差揭示均匀陷阱模型无法同时解释全部退化",       "story_role": "limitation"},
    {"slide_number": 47, "archetype_id": "content_bullets", "action_title": "无雪崩预击穿输出只能用于 30 V 内的限定趋势比较",    "story_role": "limitation"},
    {"slide_number": 48, "archetype_id": "content_bullets", "action_title": "原始实验与 SDevice 曲线叠加保留离散、缺段和异常",   "story_role": "evidence"},
    {"slide_number": 49, "archetype_id": "content_bullets", "action_title": "高压求解在约 30 V 后显著变慢，失败尝试本身构成模型边界", "story_role": "limitation"},
    {"slide_number": 50, "archetype_id": "content_bullets", "action_title": "IIC 是条件化高场判据，不能替代实验 V@1µA 或标准 BV", "story_role": "limitation"},
    {"slide_number": 51, "archetype_id": "two_column",      "action_title": "终态电场图支持空间形态比较，但不能单独证明 BV 不变", "story_role": "limitation"},
    {"slide_number": 52, "archetype_id": "two_column",      "action_title": "T 输出实验约 100 V 的高压代理与仿真高场形态只形成定性对应", "story_role": "key_finding"},
    {"slide_number": 53, "archetype_id": "two_column",      "action_title": "T 仿真结论同时包含拟合成果、模型残差和数值边界",    "story_role": "key_finding"},
    # Part 5: S-device TCAD  (54-59)
    {"slide_number": 54, "archetype_id": "two_column",      "action_title": "S 型七剂量转移曲线已完成实验-仿真同图比较",         "story_role": "evidence"},
    {"slide_number": 55, "archetype_id": "two_column",      "action_title": "S 模型能描述 gm 下降，但高剂量 Vth 负移仍明显不足", "story_role": "limitation"},
    {"slide_number": 56, "archetype_id": "content_bullets", "action_title": "严格 SS 算法下仅 20 krad 仿真曲线具备有效比较窗口", "story_role": "limitation"},
    {"slide_number": 57, "archetype_id": "two_column",      "action_title": "S 型低漏压终点的局部电场峰值仅发生约 0.18% 变化",   "story_role": "evidence"},
    {"slide_number": 58, "archetype_id": "process_flow",    "action_title": "S 模型下一步应同时修正基线、剂量映射和亚阈区扫描",  "story_role": "insight"},
    {"slide_number": 59, "archetype_id": "two_column",      "action_title": "S 型仿真已形成真实图像链，模型验证仍处于迭代阶段",  "story_role": "key_finding"},
    # Part 6: AI & Conclusions  (60-74)
    {"slide_number": 60, "archetype_id": "four_column",     "action_title": "本研究形成器件对比、恢复现象、双模型与 AI 流程四类创新", "story_role": "key_finding"},
    {"slide_number": 61, "archetype_id": "two_column",      "action_title": "TCAD 的主要瓶颈不是写出 deck，而是反复收敛、比较和证据筛选", "story_role": "context"},
    {"slide_number": 62, "archetype_id": "process_flow",    "action_title": "AI 协作采用「探索—审批—执行—监控—复核」的受监督状态机", "story_role": "method"},
    {"slide_number": 63, "archetype_id": "content_bullets", "action_title": "单核原子租约让多任务并发保持可控且失败关闭",         "story_role": "method"},
    {"slide_number": 64, "archetype_id": "content_bullets", "action_title": "异步监控只报告状态，不自动重试或修改参数",           "story_role": "method"},
    {"slide_number": 65, "archetype_id": "table",           "action_title": "AI 与研究者职责分离，避免自动化越过物理与证据边界", "story_role": "method"},
    {"slide_number": 66, "archetype_id": "content_bullets", "action_title": "失败、部分结果和异常点均保留为可追溯证据",           "story_role": "method"},
    {"slide_number": 67, "archetype_id": "big_number",      "action_title": "自动化流程已管理 22,627 个原始点和多轮仿真证据",    "story_role": "evidence"},
    {"slide_number": 68, "archetype_id": "three_column",    "action_title": "真实虚拟机工程与 AI 操作记录展示了持续迭代过程",    "story_role": "evidence"},
    {"slide_number": 69, "archetype_id": "process_flow",    "action_title": "四项创新共同把实验现象推进到可解释、可追溯的模型成果", "story_role": "insight"},
    {"slide_number": 70, "archetype_id": "matrix_2x2",      "action_title": "实验确认两种器件均发生强烈转移退化，但输出响应方向不同", "story_role": "key_finding"},
    {"slide_number": 71, "archetype_id": "two_column",      "action_title": "T 模型实现定量标定，S 模型完成阶段性验证与问题定位", "story_role": "key_finding"},
    {"slide_number": 72, "archetype_id": "content_bullets", "action_title": "关键证据边界集中保留，避免成果展示产生误解",         "story_role": "limitation"},
    {"slide_number": 73, "archetype_id": "process_flow",    "action_title": "下一步工作将围绕 S 模型、高压验证与恢复机制展开",  "story_role": "next_steps"},
    {"slide_number": 74, "archetype_id": "end_slide",       "action_title": "谢谢各位老师，请批评指正",                          "story_role": "close"},
]