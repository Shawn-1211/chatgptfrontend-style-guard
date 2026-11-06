---
name: openaistack-frontend-style
description: >-
  OpenaiStack 前端界面风格应用技能（v2 · KnowWork 实测底座 = ChatGPT 官方设计系统）。为 HTML/CSS/TS/JS/Vue/React
  前端开发确定 OpenaiStack 统一 UI 风格——完整设计令牌（中性灰阶/alpha 边框/黑主按钮/4px 网格/14px 正文基准/
  150ms 过渡/6px 状态点/elevation 阴影）、组件模板库、页面骨架、文件图标注册表，以及 R1-R11 确定性风格审查器
  （硬编码颜色/间距档/圆角档/字号档/时长档/层级白名单/Token 引用登记逐行检出）。风格一旦确定即作为前端项目的强制视觉约束直接
  应用。当用户要求 OpenaiStack 风格、按本规范写页面或组件、生成前端界面、执行样式审查、跑 check-style、修复风格
  违规时触发。关键词：OpenaiStack、前端风格、UI风格、界面风格、样式规范、设计Token、风格审查、样式守门、
  check-style、风格测试页。
name_cn: OpenaiStack 风格的应用
description_cn: >-
  OpenaiStack 前端界面风格应用技能：为前端开发确定统一的 OpenaiStack UI 风格（v2 · KnowWork 实测底座），含完整
  设计令牌、组件模板库、页面骨架、文件图标注册表与 R1-R11 确定性审查器。一旦确定应用本风格，后续前端开发、
  样式审查均按此规范执行。
version: v2.2
---

# SKILL.md · OpenaiStack — 本项目 UI 风格规范（v2 · KnowWork 实测版）

- **适用范围**：本项目所有前端代码（HTML / CSS / TS / JS / Vue / React 通用）。
- **效力**：本文件是本项目 UI 风格的**唯一真相源（Single Source of Truth）**。任何样式取值与本文件冲突，一律视为缺陷，必须修复后才能提交。
- **字面量豁免区**：只有 Token 定义层（`references/design-tokens.md`；真实项目中的 `tokens.css` `:root`/`[data-theme]` 块、Tailwind 中央配置）允许出现 Hex / px 原始值；其余所有代码只能引用 Token 或 Tailwind 语义类名。
- **风格来源（v2）**：以 **KnowWork v0.0.2 前端实测代码**为精确底座——即 ChatGPT 官方设计系统 `@openai/apps-sdk-ui`（MIT）的令牌 + KnowWork 产品层令牌（`--kw-*`），全部数值提取自 `F:\Users\32022\Desktop\Kownwork\web\src\styles\` 与运行中的编译产物，证据见 `references/knowwork-analysis.md`。v1 的 KnowFlow 蓝色体系已废弃，仅在 KnowFlow 老产品维护时使用。

## 参考文件导航（按需加载，不要一次全读）

| 文件 | 何时读 | 内容 |
| --- | --- | --- |
| `references/knowwork-analysis.md` | 查证据 / 改 Token 时 | KnowWork 实测分析：架构、全部 Token 值、组件规则、图标风格、v1→v2 差异 |
| `references/design-tokens.md` | 新项目初始化 / 改 Token 时 | 可复制的令牌落地（React 接入 apps-sdk-ui / Tailwind v4 / 纯 HTML 三条路线） |
| `references/component-library.md` | 写组件时 | v2 组件模板：按钮/卡片/状态点/徽章/表单/表格/菜单/浮层/Tabs/分区 |
| `references/framework-adapters.md` | 确定技术栈后 | apps-sdk 直用 / Tailwind v4 自建 / Badge 变体 / 文件图标注册表 §7 |
| `references/page-templates.md` | 写页面时 | v2 页面骨架：应用外壳 / 列表 / 详情 / 登录 / 设置 |
| `scripts/check-style.py` | 提交前（必跑） | 确定性审查器 R1–R11（v2 白名单），ERROR 时退出码 1 |
| `demo/openaistack-v2-test.html` | 需要视觉参照时 | v2 金样例兼全量测试页（双击预览，含明暗主题与全部交互） |

**标准工作流**：① 开发前读本文件 + 按需读 references → ② 开发中只用 Token / 语义类名 → ③ 提交前跑 `python scripts/check-style.py`（机械项必须 0 ERROR），再按 §五 审语义项。

## 一、设计 Token（唯一真相源，KnowWork 实测）

> **单一事实源契约**：本节（§一）是所有 Token 名与值的**唯一事实源**。`references/design-tokens.md` 只是"复制即用"的落地副本（CSS 必须写值才能用，故保留值），`references/knowwork-analysis.md` 只是实测证据底稿。**三者若出现任何值冲突，一律以本文件 §一 为准**，并立即修正另两处。
> **防漂移兜底**：审查器 R11 会对"引用名是否已登记"做确定性校验（含规范文档自身）。引用名（如 `var(--gray-350)`）未登记即报 ERROR；值是否与 §一 一致，仍由提交前人工对照本文件确认。

### 1.1 中性灰阶（暗色 = 灰阶倒置；边框用 alpha 色阶）

| Token | 亮 | 暗 | 用途 |
| --- | --- | --- | --- |
| `--gray-0` / `--gray-1000` | `#ffffff` / `#0d0d0d` | `#0d0d0d` / `#ffffff` | surface / 主文字 |
| `--gray-50` | `#f9f9f9` | `#131313` | 侧栏底、页面底（surface-secondary） |
| `--gray-75` | `#f3f3f3` | `#161616` | 信息块、气泡底（surface-tertiary） |
| `--gray-100` | `#ededed` | `#181818` | 选中态/hover 底、soft 按钮 |
| `--gray-400` | `#8f8f8f` | `#414141` | 三级文字 |
| `--gray-500` | `#5d5d5d` | `#4f4f4f` | 次要文字 |
| `--gray-900` | `#181818` | `#ededed` | 主按钮实底 |
| 其余 | 25/150/200/300/600/700/800/950 档 | 倒置 | 见 knowwork-analysis.md §2.1 |

**边框 alpha 体系**（禁止固定灰 hex）：`--border-subtle` = 黑 5%（暗：白 6%）；`--border` = 黑 10%（暗：白 12%）；`--border-strong` = 黑 15%（暗：白 20%）；`--border-focus` = 黑 50%（暗：白 50%，输入框焦点）；`--scrollbar` = 黑 30%（暗：白 30%，滚动条）。

### 1.2 表面与文字

| Token | 亮 | 暗 |
| --- | --- | --- |
| `--surface` | `#ffffff` | `#212121` |
| `--surface-secondary`（侧栏/页面底） | `#f9f9f9` | `#181818` |
| `--surface-tertiary`（信息块） | `#f3f3f3` | `#131313` |
| `--surface-elevated`（浮层） | `#ffffff` | `#303030` |
| `--text` | `#0d0d0d` | `#ffffff` |
| `--text-secondary` | `#5d5d5d` | `#afafaf` |
| `--text-tertiary` | `#8f8f8f` | `#8f8f8f` |
| `--on-accent`（彩色实底上的文字） | `#ffffff` | `#ffffff` |

### 1.3 语义色（ChatGPT 色板）

| 语义 | 实底（→hover） | 文字色 | 状态点 |
| --- | --- | --- | --- |
| **主按钮** | `#181818`（→`#303030`）；暗色 `#f3f3f3` 白按钮 | 白/黑 | — |
| 次按钮 | `#ededed`（→`#dfdfdf`） | `--text` | — |
| 链接 link | — | `#2b7de9` | — |
| 信息 info | `#0285ff`（→`#0169cc`） | `#0169cc` / 暗 `#66b5ff` | `#0285ff` |
| 成功 success | `#00a240` | `#00692a` / 暗 `#04b84c` | `#00a240` |
| 危险 danger | `#e02e2a`（→`#ba2623`） | `#911e1b` / 暗 `#e02e2a` | `#e02e2a` |
| 警告 warning | `#e25507` | `#923b0f` | `#fb6a22` |
| 提示 caution | `#ba8e00` | `#916f00` | 黄 |
| 发现 discovery | `#924ff7`（→`#8046d9`） | `#532d8d` / 暗 `#be95fa` | — |

### 1.4 圆角（全阶梯登记）

`2 / 4 / 6 / 8 / 10 / 12 / 16 / 20 / 24 px + full`

映射：**小控件/徽章 4、控件/输入框 8、卡片/表格容器 12、弹窗/大卡片/登录卡 16、气泡 20、对话输入区 24**；头像、状态圆点、toast = `full`。除此之外禁止任何圆角值。

### 1.5 间距（4px 基准网格 + 半档）

Tailwind 标准 4px 刻度（p-1=4px、p-2=8px…），**允许半档** `×1.5`（p-1.5=6、p-2.5=10、p-3.5=14）用于组件内微间距，**允许 2/3px** 用于按钮内图标 gap。登记档：`2/3/4/6/8/10/12/14/16/20/24/28/32/40/48/56/64`（或 0/auto）。5、7、9、11、13、15、17 等未登记值禁止。

### 1.6 字号（UI 档 + 标题档）

| 层 | 登记值 |
| --- | --- |
| UI（`--kw-font-*`） | **12 / 13 / 14（默认正文基准）/ 15（对话正文）/ 16 / 20（页面标题）** |
| 组件库 text 档 | 8 / 10 / 12 / 14 / 16 / 18 |
| 标题 heading 档（semibold） | 16 / 18 / 20 / 24 / 32 / 36 / 48 / 60 / 72 |

字体栈：`ui-sans-serif, -apple-system, system-ui, "Segoe UI", "Noto Sans", "Helvetica", "Arial", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`；等宽 `ui-monospace, "SF Mono", Menlo, Consolas, monospace`。数字一律 `font-variant-numeric: tabular-nums`。行高与字号配对（实测）：12/18、14/20、16/24、18/29；标题档自带行高。

### 1.7 阴影（elevation + 发丝描边，卡片无阴影）

| Token | 值（亮） |
| --- | --- |
| `--shadow-100/200/300` | `0 1px 2px -1px` / `0 2px 4px -1px` / `0 4px 8px -2px` + 黑 8%/8%/10%（暗色 20%/20%/36%） |
| `--shadow-400`（对话框/抽屉） | `0 8px 16px -2px` + 黑 12%（暗 30%） |
| `--shadow-hairline` | `0 0 0 1px 边框色`（浮层必配） |
| 浮层组合 | `shadow-300 + hairline`；输入框 `0 4px 16px 黑 6%` |
| `--backdrop`（浮层遮罩） | 黑 30%（暗色主题：黑 50%） |

### 1.8 过渡

**150ms**（`cubic-bezier(.4,0,.2,1)`）为默认；登记动画档：侧栏宽度 160ms、toast 180ms、对话框 200ms、抽屉 220ms。

### 1.9 控件尺寸档

高度 `22/24/26/28/32(默认)/36/40/44/48`；图标 `14/16(默认)/18/20/22/24`；按钮内 gap `3/4/6`；侧栏宽 **260px**（折叠 60px）；对话正文最大宽 **760px**；断点（实测）380 / 576 / 768 / 1024 / 1280 / 1536px。

## 二、布局与交互原则（v2 实测规则）

1. **侧边栏**：260px（折叠 60px），padding 12px 8px；菜单项 padding 8px 12px、圆角 8、字号 14；**选中态 = 浅灰底 `#ededed`、文字不变色，与 hover 同款，禁止彩色实底选中态**。
2. **左下角固定区 = 用户菜单**：border-top 分隔 + 头像（28px 圆形）+ 姓名/邮箱两行；点开含 个人设置 / 回答语言 / 管理后台（仅管理员）/ 退出登录。**不设独立"系统设置"侧栏菜单项**。
3. **整页永不滚动**（外壳 `overflow: clip`），只有内容层滚动；滚动条色 `--scrollbar`。
4. **内容卡片化**：卡片圆角 12、1px alpha 边框、**无阴影**；企业级分区（权限/审批/配置）用 border-subtle + `surface-tertiary` 浅灰底，禁止卡片嵌套。
5. **状态可见性**：Agent/任务状态用 **6px 语义色圆点 + 文字**（绿 #00a240 / 红 #e02e2a / 橙 #fb6a22 / 蓝 #0285ff / 灰 #8f8f8f），圆点居中、文字按基线；实底徽章（Badge）圆角 4、semibold、12/14px，仅用于计数/标签类。
6. **表格**：表头 12px 次文字色 + border 底边；行 padding 10px 12px、行分隔 border-subtle、hover 黑 5% 底；数字 tabular-nums。
7. **Tabs = 下划线式**（active 2px 黑下划线 + 文字变主色），非胶囊；危险操作用红色文字（菜单内 danger 文字色），需二次确认。
8. **图标**：操作图标用 ChatGPT 官方 Icon 同款（细线 outline、圆角端点、单色 currentColor）；默认 **16px**，侧栏折叠态 20px；菜单图标与文字同色。**文件类型图标走注册表**（`references/framework-adapters.md` §7）：彩色圆角方块（4px 圆角）+ 白色类别形 + 旁侧扩展名文字；类别形 ≤5 类（文档/表格/演示/图纸/压缩），颜色只取登记语义色——同类别格式同色、靠扩展名文字区分（个别格式可按惯例覆盖类别色，如 PDF 惯例红，覆盖色同样只取登记色）；新增格式只加注册表行，未注册格式自动兜底（中性灰 + 通用形），永不缺图。
9. **浮层**：菜单/弹层圆角 12、surface-elevated、`shadow-300 + hairline`；对话框圆角 16、shadow-400、宽度 250–450px、内边距 20px；toast = 黑底白字胶囊（radius-full）。**层级（实测登记）**：遮罩 1000、对话框与抽屉 1001、菜单/气泡/悬停提示 1100、轻提示 2000——登记档之外的 z-index 禁止。
10. **动效原则**：动效是状态反馈，不是装饰——只用于进入 / 退出 / hover / 开关与加载指示；进入用 `--ease-enter`、退出用 `--ease-exit`、位移用 `--ease-move`、常规用 `--ease`；禁止装饰性循环动画（骨架呼吸与“生成中”三点指示除外）；用户开启“减少动态”（`prefers-reduced-motion: reduce`）时禁用全部过渡与动画。
11. **键盘焦点与表单态**：自定义可点元素全局 `:focus-visible` = `outline: 2px solid var(--link)` + 2px offset；输入框焦点 = `--border-focus`（黑/白 50% alpha）边框；错误态 = `--danger` 边框 + 红字提示；禁用态 = surface-tertiary 底 + tertiary 字 + 默认指针。禁止移除一切焦点指示。

## 三、技术栈约束

1. **组件优先级**：React 项目直接使用 `@openai/apps-sdk-ui`（MIT，KnowWork 同款，含 Button/Menu/Avatar/Badge/Icon 全套）；其次 radix-ui；未覆盖才自建，自建组件只用本文件 Token。
2. **样式只写 Tailwind v4 语义 Token 类名**或 var() 引用；映射见 `references/design-tokens.md`。
3. **禁止直接写 Hex 值或任意像素值**；字面量只允许存在于 Token 定义层。
4. **新增 Token 的唯一合法路径**：① 先登记到本文件 §一 → ② 同步 `references/design-tokens.md` 落地 → ③ 再在组件中使用。
5. **明暗主题**：用 `[data-theme='light'/'dark']` 属性切换 Token 值（**不是** `.dark` class），组件代码不感知主题。

## 四、禁止清单（红线）

1. 禁止硬编码颜色：`#hex`、`rgb()`、`hsl()`（Token 定义层除外）。
2. 禁止 4px 网格外间距与未登记档位：`5/7/9/11/13/15/17/18px` 等一律不允许（18px 若用于 gap 请先登记用途）。
3. 禁止登记圆角档以外的圆角；`full` 仅限头像、状态圆点、toast。
4. **禁止彩色实底选中态**（侧栏 active 用灰底）；禁止蓝紫渐变、厚重阴影（只用 elevation 体系）、卡片嵌套。
5. 禁止未登记字体栈或字号；正文基准 14px（非 16px）。
6. 禁止大尺寸装饰性背景图。
7. 时长只允许登记档：150 / 160 / 180 / 200 / 220 / 350ms；其余禁止。
8. 禁止登记外 z-index 层级（只允许 1000 / 1001 / 1100 / 2000 / auto）。

## 五、提交前自查（脚本 + 模型两段式）

**第一步（机械项）**：`python scripts/check-style.py <改动目录>`，必须 **0 ERROR**（R1 颜色 / R2 间距档 / R3 圆角档 / R4 任意像素值 / R5 字号档 / R6 装饰渐变 / R7 阴影变量 / R8 背景图 / R9 时长档 / R10 层级白名单 / R11 Token 引用登记）。

**第二步（语义项）**：

- [ ] 侧栏选中态是灰底、无彩色强调；
- [ ] 左下角是用户菜单形态（设置在菜单内，非独立菜单项）；
- [ ] 运行状态是 6px 语义色圆点 + 文字；
- [ ] 卡片无阴影（alpha 边框分层）；浮层带 hairline；
- [ ] 图标为细线 outline 风格、16px 默认；
- [ ] 正文基准 14px；数字 tabular-nums；
- [ ] 无卡片嵌套；企业级分区用浅灰底信息块；
- [ ] 键盘焦点可见（focus-visible 描边 / 输入框 50% 焦点边框）；z-index 全部在登记档；
- [ ] 循环动画仅限加载态（骨架呼吸 / 生成中三点），prefers-reduced-motion 下动效已禁用；
- [ ] 新增 Token 已先登记 §一。

> 审查修复完成后，必须列出全部修复项，并确认代码完全符合 OpenaiStack v2 规范。

## 六、版本记录

- **v2.2（2026-11-05，守门补强）**：新增 **R11 Token 引用登记校验**——`var(--xxx)` 引用名必须已登记（灰度档 / 登记 Token 名），**对规范文档自身同样生效**，文档里引用未定义名字（如 `var(--gray-350)`）即拦截；确立**单一事实源契约**：Token 名与值唯一以 §一 为准，references/design-tokens.md 仅落地副本、knowwork-analysis.md 仅证据底稿，冲突一律以 §一 为准并同步修正。
- **v2.1（2026-11-05，审计补缺）**：新增登记：四条缓动曲线、慢速档 350ms、`--border-focus`/`--scrollbar`/`--backdrop`/`--on-accent`/discovery 紫、行高配对、断点与布局尺寸、z-index 层级档；新增规则：键盘焦点与表单态（§二.11）、R10 层级白名单、R9 扩展至 animation；component-library 与 page-templates 重写为 v2。
- **v2（2026-11-05）**：按 KnowWork v0.0.2 前端实测全面重写（ChatGPT 官方设计系统底座：灰阶 + alpha 边框 + 黑主按钮 + 灰底选中态 + 4px 网格 + 150ms + 状态点 + 用户菜单左下角）。证据：`references/knowwork-analysis.md`。
- **v1（2026-11-05，已废弃）**：以 KnowFlow《UI 改造指南》为底座（蓝 #3b82f6 / slate / 8px-only / 200ms / 实底徽章 / 蓝底选中态）。仅维护 KnowFlow 老产品时参考。
