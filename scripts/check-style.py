#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenaiStack 风格确定性审查器（scripts/check-style.py）

对照 SKILL.md §一 Token 白名单与 §四 禁止清单做确定性扫描。
只查"可机械判定"的项；语义项（卡片嵌套、状态可见性、留白质量等）扫描结束后
会打印待人工/模型确认清单。

规则编号（与 SKILL.md v2 §五 自查清单一一对应；白名单 = KnowWork 实测）：
  R1 硬编码颜色   #hex / rgb() / hsl() / oklch() 等（Token 定义层豁免）
                 · 仅识别 3/6/8 位 Hex（4 位 #RGBA 不支持，请统一用 6 位写法）
                 · 纯数字且不在颜色上下文的 #123 降级为 INFO（避免"任务 #1234"误报）
  R2 间距网格     4px 基准 + 登记档 2/3/4/6/8/10/12/14/16/20/24/28/32/40/48/56/64（或 0/auto）
  R3 圆角登记档   2/4/6/8/10/12/16/20/24；rounded-full 仅限头像/状态点/toast（INFO 确认）
  R4 任意像素值   禁止 [..px] 任意值语法
  R5 字号分级     UI 档 12/13/14(基准)/15/16/18/20；标题档 24/32/36/48/60/72
  R6 装饰渐变     禁止蓝紫渐变与一切装饰性渐变（Tailwind 类与 CSS 函数）
  R7 阴影体系     仅 elevation 档 shadow-100/200/300/400（浮层）+ hairline；卡片无阴影
  R8 背景图       background url() 需人工确认非大尺寸装饰图（INFO）
  R9 时长档       过渡与动画默认 150ms；登记档 150/160/180/200/220/350ms，其余禁止
  R9 时长档       过渡与动画默认 150ms；登记档 150/160/180/200/220/350ms，其余禁止
  R10 层级白名单   z-index 仅允许 1000(遮罩)/1001(对话框·抽屉)/1100(菜单·气泡)/2000(轻提示)/auto
  R11 引用登记     var(--xxx) 引用的 Token 名必须已登记（gray-<档> 或登记名）；
                   对规范文档（SKILL.md/README/references）自身同样执行，防止文档里引用未定义名字（如 gray-350）

用法：
    python scripts/check-style.py                 # 扫描当前目录
    python scripts/check-style.py src assets     # 指定目录 / 文件（显式文件不受目录排除限制）
    python scripts/check-style.py --ext md,txt   # 追加扫描扩展名

豁免：
  - SKILL.md 整文件豁免（规范本体，示例含反例）——但 R11 引用校验仍执行
  - tailwind.config.* 豁免颜色规则（Token 中央配置）
  - :root / .dark 块内豁免颜色与阴影字面量（Token 定义层）

退出码：存在 ERROR = 1（可直接接入 pre-commit / CI）；仅 INFO 或干净 = 0。
"""

import argparse
import re
import sys
from fnmatch import fnmatch
from pathlib import Path

# ---------------- 配置 ----------------
EXTENSIONS = {".html", ".css", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".md"}
EXCLUDE_DIRS = {".git", "node_modules", "dist", "build", "out", ".next", ".nuxt", ".temp", "coverage"}
FULL_EXEMPT_NAMES = {"SKILL.md", "design-tokens.md", "knowwork-analysis.md", "README.md", "README_EN.md"}  # 文档展示层：规范本体、Token 登记落地、实测证据、双语项目说明（含调色板与规则原文展示，不作代码扫描）
# R11（Token 引用登记校验）不随 FULL_EXEMPT 整文件豁免：规范文档自身也要守——但它允许引用在文档里登记过的 Token（语义色/灰阶/圆角等展示表格）。
# 因此 R11 对 FULL_EXEMPT 文档同样执行"引用是否可解析到已登记名"的轻量校验，仅对"引用了从未定义的名字"报 ERROR。
# R11_EXEMPT：纯文档/教学/证据层。SKILL.md 与 README* 常用 var(--xxx)、var(--gray-350) 做"反例教学"（示例违规写法），
# knowwork-analysis.md 只转述上游源码 token 原文——这三类都不属于"真实落地引用"，R11 对其豁免，避免误伤教学反例。
# R11 强制对象 = 真实代码文件（demo / 组件 / 页面模板 / 业务代码）+ Token 落地副本 design-tokens.md（:root/[data-theme] 落地值），
# 后者正是上次 gray-350 类漂移的发生地，必须受检。
R11_EXEMPT_NAMES = {"SKILL.md", "README.md", "README_EN.md", "knowwork-analysis.md"}
COLOR_EXEMPT_NAMES_PREFIX = ("tailwind.config",)  # Tailwind 中央配置：Token 落地层
# ---- R11 已登记 Token 名（单一事实源 = SKILL.md §一 / design-tokens.md 落地） ----
# 灰度档：SKILL.md §1.1 登记档（0/25/50/75/100/150/200/300/400/500/600/700/800/900/950/1000）
GRAY_TIERS = {0, 25, 50, 75, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 950, 1000}
# 除 gray-* 外的已登记 Token 名（取自 SKILL.md §一 与 design-tokens.md 落地）
REGISTERED_TOKENS = {
    # 表面 / 文字 / 边框
    "surface", "surface-secondary", "surface-tertiary", "surface-elevated",
    "text", "text-secondary", "text-tertiary", "on-accent", "backdrop",
    "border", "border-subtle", "border-strong", "border-focus", "scrollbar",
    # 语义色
    "primary", "primary-hover", "soft", "soft-hover", "link",
    "info", "info-hover", "info-text", "success", "success-text",
    "danger", "danger-hover", "danger-text", "warning", "warning-text",
    "discovery", "discovery-hover", "discovery-text", "status-neutral",
    # 圆角
    "radius-2xs", "radius-xs", "radius-sm", "radius-md", "radius-lg",
    "radius-xl", "radius-2xl", "radius-3xl", "radius-4xl", "radius-full",
    # 阴影
    "shadow-100", "shadow-200", "shadow-300", "shadow-400", "shadow-hairline",
    "kw-shadow-input", "kw-shadow-floating",
    # 过渡 / 动效
    "duration", "ease", "ease-enter", "ease-exit", "ease-move",
    # 字号 / 字体
    "font-xs", "font-sm", "font-base", "font-chat", "font-md", "font-title",
    "font-sans", "font-mono",
    "kw-font-xs", "kw-font-sm", "kw-font-base", "kw-font-chat", "kw-font-md", "kw-font-title",
    # 布局 / 尺寸
    "sidebar-width", "chat-max-width", "icon-size",
    "control-size-sm", "control-size-md", "control-size-lg",
    "kw-sidebar-width",
    # 产品自有
    "kw-link", "kw-radius-control", "kw-radius-card", "kw-radius-card-lg", "kw-radius-bubble",
}
SPACING_PX = {0, 2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64}
RADIUS_PX = {2, 4, 6, 8, 10, 12, 16, 20, 24}
FONT_PX = {8, 10, 12, 13, 14, 15, 16, 18, 20, 24, 32, 36, 48, 60, 72}
FONT_CLASSES_OK = {"xs", "sm", "base", "lg", "xl", "2xl"}
DURATION_MS = {150, 160, 180, 200, 220, 350}
Z_INDEX_OK = {1000, 1001, 1100, 2000}  # 实测层级档：遮罩/对话框·抽屉/菜单·气泡/轻提示

# ---------------- 正则 ----------------
RE_HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
RE_FUNC_COLOR = re.compile(r"\b(?:rgba?|hsla?|oklch|oklab|lab|lch)\s*\(")
RE_HEX_HAS_LETTER = re.compile(r"[a-fA-F]")
# 颜色上下文：# 前最近的非空白字符属于以下之一（或行首），视为颜色取值位置
COLOR_CTX_CHARS = ':=(,"\'[{';

RE_SPACING_CLASS = re.compile(
    r"(?<!\w)(?:gap-x|gap-y|space-x|space-y|px|py|pt|pr|pb|pl|mx|my|mt|mr|mb|ml|gap|p|m)"
    r"-(\d+(?:\.\d+)?)(?![\w.])"
)
RE_SPACING_DECL = re.compile(
    r"(?<![\w-])(?:row-gap|column-gap|margin|padding|gap)"
    r"(?:-(?:top|right|bottom|left|x|y|inline|block|inline-start|inline-end|block-start|block-end))?"
    r"\s*:\s*([^;{}]+)"
)
RE_PX = re.compile(r"(\d+(?:\.\d+)?)px")

RE_RADIUS_CLASS = re.compile(
    r"(?<![\w-])rounded(?:-(?:[tblr][tblr]?-)?(?P<val>none|2xs|xs|sm|md|lg|xl|2xl|3xl|4xl|full))?(?![\w-])"
)
RE_RADIUS_DECL = re.compile(r"(?<![\w-])border-radius\s*:\s*([^;{}]+)")
RE_ARBITRARY_PX = re.compile(r"\[[^\]\n]*?\d+(?:\.\d+)?px[^\]\n]*?\]")

RE_FONT_CLASS = re.compile(r"(?<![\w-])text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)(?![\w.-])")
RE_FONT_DECL = re.compile(r"(?<![\w-])font-size\s*:\s*([^;{}]+)")

RE_GRADIENT = re.compile(
    r"(?<![\w-])(?:bg-gradient-to-|bg-linear-|bg-conic-|bg-radial-|"
    r"repeating-linear-gradient\s*\(|repeating-radial-gradient\s*\(|"
    r"linear-gradient\s*\(|conic-gradient\s*\(|radial-gradient\s*\()"
)
RE_SHADOW_CLASS = re.compile(r"(?<![\w-])shadow-([a-z0-9]+)(?![\w-])")
RE_SHADOW_BARE = re.compile(r"(?<![\w-])shadow(?![\w-])")
RE_SHADOW_DECL = re.compile(r"(?<![\w-])box-shadow\s*:\s*([^;{}]+)")
RE_TRANSITION_MS = re.compile(r"(?<![\w-])(?:transition|animation)(?:-duration)?\s*:\s*[^;{}]*?(\d+)ms")
RE_ZINDEX_DECL = re.compile(r"(?<![\w-])z-index\s*:\s*(-?\d+|auto)\b")
RE_ZINDEX_CLASS = re.compile(r"(?<![\w-])z-(\[|[0-9]+)")
RE_BG_URL = re.compile(r"(?<![\w-])background(?:-image)?\s*:\s*[^;{}]*?\burl\s*\(")
# R11：捕获 var(--xxx) 引用；xxx 需能解析到已登记 Token 名（gray-<档> 或 REGISTERED_TOKENS）
RE_VAR_REF = re.compile(r"var\(--([a-zA-Z0-9][a-zA-Z0-9-]*)\)")

RE_TOKEN_BLOCK_OPEN = re.compile(r"^\s*(?::root|\.dark|\[data-theme[^\]]*\])\s*\{")

MANUAL_REVIEW = [
    "侧边栏选中态是否为浅灰底（v2 禁止彩色实底选中态）",
    "左下角是否为用户菜单形态（设置在菜单内，非独立菜单项）",
    "运行状态是否为 6px 语义色圆点 + 文字（绿/红/橙/蓝/灰）",
    "卡片是否无阴影（alpha 边框分层）；浮层是否为 shadow + hairline 组合",
    "图标是否细线 outline 风格（ChatGPT Icon 同款），默认 16px",
    "正文基准是否 14px；数字是否 tabular-nums；无卡片嵌套",
    "键盘焦点是否可见（focus-visible 描边 / 输入框 50% 焦点边框）",
]


def iter_lines_with_token_state(text):
    """逐行产出 (行号, 行文本, 是否处于 :root/.dark Token 块内)。"""
    in_block = False
    depth = 0
    for i, line in enumerate(text.splitlines(), 1):
        if in_block:
            yield i, line, True
            depth += line.count("{") - line.count("}")
            if depth <= 0:
                in_block = False
        elif RE_TOKEN_BLOCK_OPEN.match(line):
            in_block = True
            depth = line.count("{") - line.count("}")
            yield i, line, True
            if depth <= 0:
                in_block = False
        else:
            yield i, line, False


def fmt_px(v):
    return f"{v:g}px"


def prev_nonspace(line, pos):
    """pos 前最近的非空白字符；行首返回空字符串。"""
    i = pos - 1
    while i >= 0 and line[i].isspace():
        i -= 1
    return line[i] if i >= 0 else ""


def is_color_context(line, pos):
    return prev_nonspace(line, pos) in ("",) or prev_nonspace(line, pos) in COLOR_CTX_CHARS


def check_token_refs(rel, ln, line):
    """R11：var(--xxx) 引用的 Token 名必须已登记。对规范文档（SKILL/README/references）自身也执行，
    防止引用从未定义的名字（如 var(--gray-350)）。"""
    out = []
    for m in RE_VAR_REF.finditer(line):
        name = m.group(1)
        if name.startswith("gray-"):
            try:
                tier = int(name[5:])
            except ValueError:
                tier = None
            if tier not in GRAY_TIERS:
                out.append((ln, "ERROR", "R11-Token引用未登记",
                            f"var(--{name})：未登记灰度档，允许 0/25/50/75/100/150/200/300/400/500/600/700/800/900/950/1000"))
        elif name not in REGISTERED_TOKENS:
            out.append((ln, "ERROR", "R11-Token引用未登记",
                        f"var(--{name})：未登记 Token，请先在 SKILL.md §一 登记并同步 design-tokens.md"))
    return out


def check_line(rel, ln, line, in_token, color_exempt, check_r11=True):
    out = []
    if not line.strip():
        return out

    # R11 引用的 Token 名必须已登记（含规范文档自身，不随 FULL_EXEMPT 豁免）
    if check_r11:
        out.extend(check_token_refs(rel, ln, line))

    # R1 硬编码颜色（Token 定义层与 tailwind.config 豁免）
    if not in_token and not color_exempt:
        for m in RE_HEX.finditer(line):
            tok = m.group(0)
            in_ctx = is_color_context(line, m.start())
            if in_ctx or RE_HEX_HAS_LETTER.search(tok):
                out.append((ln, "ERROR", "R1-硬编码颜色",
                            f"{tok} → 替换为 SKILL.md §一 语义类名/Token"))
            else:
                out.append((ln, "INFO", "R1-硬编码颜色",
                            f"{tok} 疑似任务编号等非颜色文本，请人工确认"))
        m = RE_FUNC_COLOR.search(line)
        if m:
            out.append((ln, "ERROR", "R1-硬编码颜色",
                        f"{m.group(0).rstrip('(').strip()}() → 替换为 SKILL.md §一 语义类名/Token"))

    # R2 Tailwind 间距类（n × 4px）
    for m in RE_SPACING_CLASS.finditer(line):
        v = float(m.group(1))
        px = v * 4
        if v != 0 and px not in SPACING_PX:
            out.append((ln, "ERROR", "R2-间距网格",
                        f"{m.group(0)} = {fmt_px(px)}，不在 4px 网格登记档（允许 2/3/4/6/8/10/12/14/16/20/24/28/32/40/48/56/64）"))
    # R2 内联样式间距
    for m in RE_SPACING_DECL.finditer(line):
        val = m.group(1)
        prop = line[m.start():m.end()].split(":")[0].strip()
        if "calc(" in val:
            out.append((ln, "INFO", "R2-间距网格",
                        f"{prop}: {val.strip()} 含 calc()，请人工确认取值在 8px 档位"))
            continue
        for pm in RE_PX.finditer(val):
            if float(pm.group(1)) not in SPACING_PX:
                out.append((ln, "ERROR", "R2-间距网格",
                            f"{prop}: {pm.group(0)}，不在 4px 网格登记档（或 0/auto）"))

    # R3 圆角类
    for m in RE_RADIUS_CLASS.finditer(line):
        val = m.group("val")
        if val is None:
            out.append((ln, "ERROR", "R3-圆角白名单",
                        "'rounded' 默认圆角未登记，请写 rounded-sm/md/lg"))
        elif val == "full":
            out.append((ln, "INFO", "R3-圆角白名单",
                        "rounded-full：请确认仅用于头像/状态圆点等圆形形状"))
        elif val == "none":
            out.append((ln, "ERROR", "R3-圆角白名单",
                        "rounded-none 未登记（如需直角请先在 SKILL.md 登记 Token）"))
        elif val not in ("2xs", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl"):
            out.append((ln, "ERROR", "R3-圆角白名单",
                        f"rounded-{val} 超出登记圆角档 2/4/6/8/10/12/16/20/24"))
    # R3 内联圆角
    for m in RE_RADIUS_DECL.finditer(line):
        val = m.group(1)
        if "9999px" in val or "50%" in val:
            out.append((ln, "INFO", "R3-圆角白名单",
                        f"border-radius: {val.strip()}：请确认为圆形形状"))
            continue
        for pm in RE_PX.finditer(val):
            if float(pm.group(1)) not in RADIUS_PX:
                out.append((ln, "ERROR", "R3-圆角白名单",
                            f"border-radius: {pm.group(0)}，只允许登记档 2/4/6/8/10/12/16/20/24"))

    # R4 任意像素值语法
    for m in RE_ARBITRARY_PX.finditer(line):
        out.append((ln, "ERROR", "R4-任意像素值",
                    f"{m.group(0)}：禁止任意值语法，请使用标准刻度或先登记 Token"))

    # R5 字号
    for m in RE_FONT_CLASS.finditer(line):
        if m.group(1) not in FONT_CLASSES_OK:
            out.append((ln, "ERROR", "R5-字号分级",
                        f"text-{m.group(1)} 超出登记档（UI 允许 xs/sm/base/lg/xl/2xl，标题用登记 px 值）"))
    for m in RE_FONT_DECL.finditer(line):
        for pm in RE_PX.finditer(m.group(1)):
            if float(pm.group(1)) not in FONT_PX:
                out.append((ln, "ERROR", "R5-字号分级",
                            f"font-size: {pm.group(0)}，只允许 UI 档 12/13/14/15/16/18/20 或标题档 24/32/36/48/60/72"))

    # R6 装饰渐变
    if RE_GRADIENT.search(line):
        out.append((ln, "ERROR", "R6-装饰渐变",
                    "禁止蓝紫渐变与装饰性渐变（含 bg-gradient/bg-linear 与 CSS gradient 函数）"))

    # R7 阴影（v2：elevation 100–400 体系，卡片无阴影）
    for m in RE_SHADOW_CLASS.finditer(line):
        if m.group(1) not in ("100", "200", "300", "400", "none"):
            out.append((ln, "ERROR", "R7-阴影体系",
                        f"shadow-{m.group(1)} 未登记；只允许 shadow-100/200/300/400（浮层）或 shadow-none"))
    if RE_SHADOW_BARE.search(line):
        out.append((ln, "ERROR", "R7-阴影体系",
                    "裸 'shadow' 类未登记，请写 shadow-100/200/300/400 或移除"))
    for m in RE_SHADOW_DECL.finditer(line):
        if in_token:
            continue
        val = m.group(1).strip()
        if "var(--shadow" not in val and "var(--kw-shadow" not in val and val != "none":
            out.append((ln, "ERROR", "R7-阴影体系",
                        f"box-shadow: {val}，只允许 var(--shadow-100/200/300/400)、var(--shadow-hairline)、var(--kw-shadow-*)（仅浮层）或 none"))

    # R8 背景图
    if RE_BG_URL.search(line):
        out.append((ln, "INFO", "R8-背景图",
                    "background 使用 url()：请人工确认非大尺寸装饰性背景图"))

    # R9 时长档（v2：过渡与动画默认 150ms；登记档 150/160/180/200/220/350ms）
    for m in re.finditer(r"(?<![\w-])duration-(\d+)(?![\w-])", line):
        if int(m.group(1)) not in DURATION_MS:
            out.append((ln, "ERROR", "R9-时长档",
                        f"duration-{m.group(1)} 未登记；时长档仅 150/160/180/200/220/350ms"))
    for m in RE_TRANSITION_MS.finditer(line):
        if int(m.group(1)) not in DURATION_MS:
            out.append((ln, "ERROR", "R9-时长档",
                        f"transition/animation {m.group(1)}ms 未登记；时长档仅 150/160/180/200/220/350ms"))

    # R10 层级白名单（v2 实测层级档）
    for m in RE_ZINDEX_DECL.finditer(line):
        val = m.group(1)
        if val != "auto" and int(val) not in Z_INDEX_OK:
            out.append((ln, "ERROR", "R10-层级白名单",
                        f"z-index: {val} 未登记；层级档仅 1000(遮罩)/1001(对话框·抽屉)/1100(菜单·气泡)/2000(轻提示)"))
    for m in RE_ZINDEX_CLASS.finditer(line):
        tok = m.group(1)
        if tok == "[":
            out.append((ln, "ERROR", "R10-层级白名单",
                        "z-[..] 任意值语法禁止；层级档仅 1000/1001/1100/2000"))
        elif int(tok) not in Z_INDEX_OK:
            out.append((ln, "ERROR", "R10-层级白名单",
                        f"z-{tok} 未登记；层级档仅 1000/1001/1100/2000"))
    return out


def check_file(path: Path, rel: str):
    findings = []
    full_exempt = path.name in FULL_EXEMPT_NAMES
    color_exempt = path.name.startswith(COLOR_EXEMPT_NAMES_PREFIX)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [(0, "ERROR", "IO", f"无法读取文件: {exc}")]
    if full_exempt:
        # 规范文档整文件豁免 R1–R10（展示调色板/反例），但仍执行 R11（Token 引用登记校验）——
        # 这样文档自身若引用了从未登记的名字（如 var(--gray-350)）同样会被拦截。
        # 例外：实测证据文档（R11_EXEMPT_NAMES）只转述上游源码 token 原文，R11 亦豁免。
        if path.name in R11_EXEMPT_NAMES:
            return findings
        for ln, line, in_token in iter_lines_with_token_state(text):
            findings.extend(check_token_refs(rel, ln, line))
        return findings
    for ln, line, in_token in iter_lines_with_token_state(text):
        findings.extend(check_line(rel, ln, line, in_token, color_exempt))
    return findings


def collect_files(args_paths, extra_exts):
    exts = set(EXTENSIONS) | {("." + e.lstrip(".")) for e in extra_exts}
    files = []
    for p in args_paths:
        path = Path(p)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for f in sorted(path.rglob("*")):
                if not f.is_file():
                    continue
                if f.suffix.lower() not in exts:
                    continue
                if any(part in EXCLUDE_DIRS for part in f.parts):
                    continue
                files.append(f)
        else:
            print(f"[warn] 路径不存在，已跳过: {p}")
    return files


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="OpenaiStack 风格确定性审查器")
    parser.add_argument("paths", nargs="*", default=["."], help="要扫描的目录/文件，默认当前目录")
    parser.add_argument("--ext", default="", help="追加扫描扩展名，逗号分隔，如 md,txt")
    args = parser.parse_args()

    extra = [e.strip() for e in args.ext.split(",") if e.strip()] if args.ext else []
    root = Path(".")
    files = collect_files(args.paths, extra)

    all_findings = []
    scanned = 0
    for f in files:
        scanned += 1
        rel = f.relative_to(root).as_posix() if f.is_relative_to(root) else f.as_posix()
        all_findings.extend((rel, *item) for item in check_file(f, rel))

    errors = [x for x in all_findings if x[2] == "ERROR"]
    infos = [x for x in all_findings if x[2] == "INFO"]

    print(f"OpenaiStack check-style · 扫描 {scanned} 个文件")
    print("-" * 72)
    for rel, ln, sev, rule, msg in all_findings:
        print(f"{rel}:{ln}  [{sev}] [{rule}] {msg}")
    if not all_findings:
        print("（无机械项违规）")
    print("-" * 72)
    print(f"结果: {len(errors)} ERROR / {len(infos)} INFO")

    if infos or errors:
        print()
        print("需人工/模型审查（脚本无法判定）：")
        for i, item in enumerate(MANUAL_REVIEW, 1):
            print(f"  {i}. {item}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
