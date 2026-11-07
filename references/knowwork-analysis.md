# KnowWork 前端实测分析（references/knowwork-analysis.md）

> **定位**：本文件是 OpenaiStack v2 Token 登记表的证据底稿。所有数值均为 2026-11-05 从本机运行的 KnowWork v0.0.2 前端源码与编译产物中实测提取，非推测。
> **证据来源**：`F:\Users\32022\Desktop\Kownwork\web\`（完整源码）+ 运行中的网关 `http://localhost:8081`（编译 CSS 173KB）。

## 0. 核心结论（为什么原设计"感觉有问题"）

| 产品 | 设计系统 | 主色 | 选中态 | 灰阶 | 网格 | 过渡 |
| --- | --- | --- | --- | --- | --- | --- |
| KnowFlow（改造指南版） | Ant Design + 自建 Less Token | 蓝 #3b82f6 | 浅蓝底+深蓝字 | slate 冷灰 | 8px | 200ms |
| **KnowWork（实测）** | **ChatGPT 官方设计系统 `@openai/apps-sdk-ui`（MIT）+ Tailwind v4** | **黑 #181818（暗色主题下白）** | **灰底 #ededed，无彩色** | **纯中性灰 #0d0d0d→#fff + alpha 边框** | **4px 基准（允许 6/10/14 半档与 2/3 微间距）** | **150ms** |

> OpenaiStack v1 以 KnowFlow 的《UI 改造指南》（`KnowFlow/docs/UI_REDESIGN_GUIDE.md`，蓝 #3b82f6、slate、8px 网格）为底座；而正在运行的 KnowWork 采用 ChatGPT 设计系统——两者是不同世代的两套语言。v2 按 KnowWork 实测值重写登记表。

## 1. 架构（web/src/styles 的分层）

```
index.css   = @import 'tailwindcss' + @import '@openai/apps-sdk-ui/css'（ChatGPT 令牌与重置）
tokens.css  = KnowWork 自有令牌：全部别名指向组件库令牌，仅补链接色/字号档/布局尺寸
ui.css      = 自建组件样式（声明纪律："颜色、圆角、阴影只用组件库的令牌……不写字面量"）
app.css     = 外壳（侧栏）样式
```

- 技术栈：React 19 + Vite 7 + **Tailwind CSS v4** + radix-ui + `@openai/apps-sdk-ui`（组件与图标源）
- 主题切换：`[data-theme='light'|'dark']`（**不是** `.dark` class）
- 自有令牌仅 12 个：`--kw-link #2b7de9`、字号 6 档、`--kw-sidebar-width 260px`、阴影 3 组、圆角别名 4 组

## 2. 实测 Token（亮色 / 暗色）

### 2.1 中性灰阶（暗色 = 灰阶倒置）

| Token | 亮 | 暗 | | Token | 亮 | 暗 |
| --- | --- | --- | --- | --- | --- | --- |
| gray-0 | #ffffff | #0d0d0d | | gray-400 | #8f8f8f | #414141 |
| gray-25 | #fcfcfc | #101010 | | gray-500 | #5d5d5d | #4f4f4f |
| gray-50 | #f9f9f9 | #131313 | | gray-600 | #414141 | #8f8f8f |
| gray-75 | #f3f3f3 | #161616 | | gray-700 | #303030 | #afafaf |
| gray-100 | #ededed | #181818 | | gray-800 | #212121 | #cdcdcd |
| gray-150 | #dfdfdf | #1c1c1c | | gray-900 | #181818 | #ededed |
| gray-200 | #cdcdcd | #212121 | | gray-950 | #131313 | #f3f3f3 |
| gray-300 | #afafaf | #303030 | | gray-1000 | #0d0d0d | #ffffff |

### 2.2 表面 / 文字 / 边框

| 角色 | Token | 亮 | 暗 |
| --- | --- | --- | --- |
| 内容面 | surface = gray-0 | #ffffff | #212121 |
| 侧栏/页面底 | surface-secondary = gray-50 | #f9f9f9 | #181818 |
| 三级面/信息块 | surface-tertiary = gray-75 | #f3f3f3 | #131313 |
| 浮层面 | surface-elevated | #ffffff | #303030 |
| 主文字 | text = gray-1000 | #0d0d0d | #ffffff |
| 次文字 | text-secondary = gray-500 | #5d5d5d | #afafaf |
| 三级文字 | text-tertiary = gray-400 | #8f8f8f | #8f8f8f |
| 弱边框 | border-subtle | 黑 5% | 白 6% |
| 常规边框 | border | 黑 10% | 白 12% |
| 强边框 | border-strong | 黑 15% | 白 20% |

> 边框全部走 **alpha 色阶**（黑/白透明度），不用固定灰 hex——这是 ChatGPT 系统的标志性做法，明暗自动可逆。

### 2.3 语义色（ChatGPT 色板）

| 语义 | 实底（亮→hover） | 文字色 | 状态点 |
| --- | --- | --- | --- |
| 主按钮 primary | **gray-900 #181818 → gray-700**（暗色 **#f3f3f3 白**） | 白 / 暗色黑 | — |
| 次按钮 secondary | gray-100 #ededed → gray-150 | gray-1000 | — |
| 链接 link | — | #2b7de9（--kw-link）/ blue-500 #0169cc | — |
| 信息 info | blue-400 **#0285ff** → blue-500 #0169cc | blue-500 / 暗 blue-200 #66b5ff | blue-400 #0285ff |
| 成功 success | green-500 **#00a240** | green-700 #00692a / 暗 green-400 #04b84c | green-500 #00a240 |
| 危险 danger | red-500 **#e02e2a** → red-600 | red-700 #911e1b / 暗 red-500 | red-500 #e02e2a |
| 警告 warning | orange-500 #e25507 → orange-600 | orange-700 #923b0f | orange-400 **#fb6a22** |
| 提示 caution | yellow-600 #ba8e00 | yellow-700 | yellow |

### 2.4 圆角阶梯（全登记）

`2px(2xs) / 4px(xs) / 6px(sm) / 8px(md) / 10px(lg) / 12px(xl) / 16px(2xl) / 20px(3xl) / 24px(4xl) / full`

KnowWork 映射：**控件 8**（--kw-radius-control=radius-md）、**卡片 12**、**弹窗/大卡 16**、**气泡 20**、**对话输入区 24**（composer）、**徽章 4**（badge-radius=radius-xs）、**头像/状态圆点/toast = full**。

### 2.5 间距（4px 基准 + 半档）

Tailwind 标准 4px 刻度（`--spacing: .25rem`）。实测常用：**2/3/4/6/8/10/12/14/16/20/24/32/48/56**（6=4×1.5、10=8×1.25?——menu-item=spacing×1.5=6px、td padding 10px 12px、侧栏 padding 12px 8px、菜单项 8px 12px、弹窗内边距 spacing×5=20px）。

### 2.6 字号（UI 档 + 标题档）

| 层 | 值 |
| --- | --- |
| KnowWork UI 档（tokens.css） | **xs 12 / sm 13 / base 14（默认正文基准）/ chat 15 / md 16 / title 20** |
| 组件库 text 档 | 3xs 8 / 2xs 10 / xs 12 / sm 14 / md 16 / lg 18 |
| 标题 heading 档 | xs 16 / sm 18 / md 20 / lg 24 / xl 32 / 2xl 36 / 3xl 48 / 4xl 60 / 5xl 72（全部 semibold） |

字重：normal 400 / medium 500 / semibold 600。数字用 `font-variant-numeric: tabular-nums`。

### 2.7 阴影（elevation 体系 + 发丝描边）

| Token | 值（亮） | 暗色 alpha |
| --- | --- | --- |
| shadow-100 | 0 1px 2px -1px + 黑 8% | 20% |
| shadow-200 | 0 2px 4px -1px + 黑 8% | 20% |
| shadow-300 | 0 4px 8px -2px + 黑 10% | 36% |
| shadow-400 | 0 8px 16px? + 黑 12% | 30% |
| hairline | **0 0 0 1px 边框色**（发丝描边，高分屏 .5px） | 同 |
| kw-shadow-floating | shadow-300 + hairline（浮层组合） | 同 |
| kw-shadow-input | 0 4px 16px 黑 6% | 同 |

卡片默认**无阴影**靠 alpha 边框；浮层 = 阴影 + 发丝描边组合。

### 2.8 过渡

`--transition-duration-basic: 150ms` + `cubic-bezier(.4,0,.2,1)`；侧栏宽度 160ms ease；toast 180ms；对话框 200ms；抽屉 220ms；专用缓动 cubic-enter/exit/move。

### 2.9 控件尺寸档

- 高度：3xs 22 / 2xs 24 / xs 26 / sm 28 / **md 32（默认）** / lg 36 / xl 40 / 2xl 44 / 3xl 48
- 图标：xs 14 / **sm 16（默认）** / md 18 / lg 20 / xl 22 / 2xl 24
- 按钮内 gap：sm 3 / md 4 / lg 6

## 3. 布局与组件实测规则

1. **侧边栏**：宽 **260px**（折叠 60px，过渡 160ms）；padding 12px 8px；菜单项 padding 8px 12px、圆角 8、字号 14；**选中态 = hover 同款浅灰底 gray-100，无任何彩色强调**（ChatGPT 式）。
2. **左下角固定区**：border-top 分隔 + **用户菜单**（Avatar 28px 圆形 + 姓名/邮箱两行 meta）；点开菜单含：个人设置(Settings) / 回答语言(Globe，带当前值) / 管理后台(BuildingWorkspace，仅管理员) / 退出登录(Logout)。**没有独立"系统设置"侧栏项**。
3. **整页永不滚动**（外壳 `overflow: clip`），只有内容层自己滚。
4. **表格**：th 12px 字 secondary 色 + border 底边；td padding 10px 12px、行分隔 border-subtle、hover 黑 5% 底；数字 tabular-nums。
5. **Tabs**：下划线式（active 2px 黑下划线 + 文字变黑），非胶囊。
6. **状态可见性**：**6px 圆点**（gray/green/red/orange/blue 语义色）+ 文字基线对齐（`.kw-status`，点居中文字按基线），不是实底彩色徽章；徽章（Badge）用 radius-xs 4px、semibold、12/14px 字。
7. **Toast**：黑底白字胶囊（radius-full、gray-900 底、shadow-300）。
8. **对话框**：radius-2xl 16px、surface-elevated、shadow-400；抽屉右滑 220ms。
9. **登录页**：居中卡片（max-width 380px、radius-2xl 16px、padding 32px、1px 边框）；登录按钮 `Button color="primary" size="lg"` = **黑实底 gray-900**、白字（暗色主题下白底黑字）；输入框 size lg=36px。

## 4. 图标风格

- **来源**：全部来自 `@openai/apps-sdk-ui/components/Icon`（ChatGPT 官方图标集，MIT），如 `Settings / Globe / Logout / BuildingWorkspace / Sidebar / ComposeEditSquare`；另有自建 `FileKindIcon`（文件类型）与 `resourceIcon`。
- **风格**：细线条 outline、圆角端点/连接（非填充风）、单色 currentColor 跟随文字。
- **尺寸**：默认 **16px**；侧栏折叠态 20px；toast 图标 16px；尺寸档 14/16/18/20/22/24。
- **菜单图标色**：与菜单文字同色（secondary 灰）。
- **文件类型图标**：彩色圆角方块（radius-sm 4px）+ 白色图案占 70%（彩色底上白图案两套主题不变，--kw-on-color #ffffff）。

## 5. 与 OpenaiStack v1 的差异清单（v2 已按左列改写）

| 维度 | v1（KnowFlow 指南底座） | v2（KnowWork 实测） |
| --- | --- | --- |
| 主按钮 | 蓝 #3b82f6 | 黑 #181818（暗色白） |
| 侧栏选中态 | 蓝实底白字 | 灰底 #ededed 黑字 |
| 中性灰 | slate（#f8fafc/#e2e8f0/#64748b/#0f172a） | 纯灰阶 + alpha 边框（#f9f9f9/#ededed/#5d5d5d/#0d0d0d） |
| 侧栏宽 / 底部 | 240px / 独立"系统设置"项 + 用户块 | 260px / 仅用户菜单（设置藏菜单内） |
| 圆角 | 6/8/12 | 2/4/6/8/10/12/16/20/24/full（卡片 12、徽章 4） |
| 间距 | 8px-only 六档 | 4px 基准（允许 6/10/14 半档与 2/3 微间距） |
| 字号 | 12–24 六档，基准 16 | UI 12/13/14(基准)/15/16/18/20 + 标题档 |
| 阴影 | shadow-xs 单档 | elevation 100–400 + hairline 组合 |
| 过渡 | 200ms | 150ms（浮层 150–220ms 档） |
| 状态徽章 | 实底彩色 Badge | 6px 状态点 + 文字（Badge 另有 4px 圆角样式） |
| 图标 | shadcn/lucide 未约定 | ChatGPT 官方 Icon 同款，16px 默认 |
| 主题切换 | .dark class | [data-theme] 属性 |
| 语义蓝 | #3b82f6 全场景 | link #2b7de9 / info 实底 #0285ff / 文字 #0169cc |

## 6. 审计补充证据（v2.1 查漏时的二次实测）

| 项 | 实测原文/值 | 出处 |
| --- | --- | --- |
| 浮层层级 | ui.css 注释原文：「遮罩 1000、对话框与抽屉 1001、下拉/菜单/气泡/悬停提示 1100、轻提示 2000」 | web/src/styles/ui.css 头部注释 |
| 键盘焦点 | `@layer base { :focus-visible { outline: 2px solid var(--kw-link); outline-offset: 2px; } }` | app.css |
| 输入框焦点边框 | `--input-outline-border-color-focus: var(--alpha-50)`（黑 50%） | bundle theme 层 |
| 禁用态 | `--color-background-disabled: var(--alpha-05)`、`--color-text-disabled: var(--gray-400)` | bundle theme 层 |
| 滚动条 | `--scrollbar-color: var(--alpha-30)` | bundle theme 层 |
| 断点 | 380 / 576 / 768 / 1024 / 1280 / 1536px | bundle @layer theme |
| 行高配对 | text-xs 12/18 · text-sm 14/20 · text-md 16/24 · text-lg 18/29；heading 档自带行高 | bundle --font-* 令牌 |
| 对话框尺寸 | min 250 / max 450px、内边距 spacing×5 = 20px、圆角 2xl 16px | bundle --dialog-* / --modal-* |
| 对话区宽度 | `--kw-chat-max-width: 760px`（组件库默认 800px） | tokens.css |
| 侧栏折叠态 | 60px、图标 20px、过渡 160ms ease | app.css .kw-sidebar.is-collapsed |

## 6b. 侧栏二级菜单实测证据（v2.3 新增，2026-11-06 三次实测）

> 场景：一级目录下挂可展开的二级菜单 / 部门树 / 知识源分组。此前 v2.1–v2.2 未覆盖，v2.3 补登。

| 项 | 实测原文/值 | 出处 |
| --- | --- | --- |
| 树行结构 | `.kw-tree-row { display:flex; align-items:center; gap:2px; border-radius:var(--radius-md) }`（圆角 8） | web/src/styles/ui.css §树 |
| 树行 hover | `--color-background-primary-soft-alt`（soft 灰底） | ui.css .kw-tree-row:hover |
| 树行选中 | `--color-surface-tertiary`（三级浅灰底，比一级选中态 gray-100 浅一档） | ui.css .kw-tree-row.is-selected |
| 展开开关 | `.kw-tree-toggle { width:20px; height:20px; color:var(--color-text-secondary) }`；展开 ChevronDown / 收起 ChevronRight **图标切换，无 rotate 动画** | ui.css + ui/Tree.tsx L61 |
| 标题 | `.kw-tree-title { padding:6px 6px 6px 2px; font-size:var(--font-text-sm-size)/*14px*/; nowrap+ellipsis }`；行高 32 = 20 开关 + 6×2 | ui.css .kw-tree-title |
| 节点图标 | `.kw-tree-node-icon svg { 16×16 }`，secondary 色，gap 6px | ui.css .kw-tree-node* |
| 缩进 | `style={{ paddingLeft: depth * 16 + 4 }}`（基线 4 + 每层 16：4/20/36/52；动态计算无字面量） | ui/Tree.tsx L52 |
| 分组节点 | `selectable=false` → 标题加 `.is-group`（secondary 灰），点标题即展开收起，不可选中 | Tree.tsx L14/L68 + ui.css .kw-tree-title.is-group |
| 空占位 | 无子级也渲染 `<span class="kw-tree-toggle" aria-hidden>` 保持对齐 | Tree.tsx L64 |
| 默认态与动画 | 注释原文：「默认全部展开，点三角收起，点名称选中」；子级直接显隐，无过渡动画 | Tree.tsx L2/L74 |
| 无障碍 | 注释原文：「键盘与读屏照 WAI-ARIA 的 tree 模式」；`role=tree/treeitem/group` + `aria-expanded` + `aria-selected` | Tree.tsx L4/L44-47 |
| 管理后台组织树 | `.kw-org-tree { padding:8px; border:1px solid; border-radius:var(--kw-radius-card) }`（卡片容器 12px 圆角） | web/src/styles/admin.css L204 |

## 7. v1 遗留处置记录

- 2026-11-05 按用户要求从包内删除（移入回收站）：`assets/task-panel.html`（v1 金样例）、`demo/sales-order-entry.html`、`demo/valve-quote.html`（v1 业务演示）及其全部截图与 `.temp` 分析中间产物。
- 金样例角色由 `demo/openaistack-v2-test.html`（v2 全量测试页）独自承担；重做业务 demo 时按 v2 模板（`references/component-library.md`、`references/page-templates.md`）从零生成即可，不需要参考 v1 旧文件。
