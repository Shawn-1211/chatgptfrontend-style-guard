# OpenaiStack v2 设计 Token 落地文件（references/design-tokens.md）

> **定位**：`SKILL.md` §一登记表的**落地实现（复制即用）**，属于"字面量豁免区"。数值 = KnowWork v0.0.2 实测（ChatGPT 官方设计系统），证据见 `references/knowwork-analysis.md`。
> **维护纪律**：改 Token 先在 SKILL.md 登记，再同步本文件；冲突时以 SKILL.md 为准。
> **主题机制**：`[data-theme='light' | 'dark']` 属性切换（不是 `.dark` class）。

## 路线 A：React 项目直接用 apps-sdk-ui（推荐，KnowWork 同款）

```bash
npm install @openai/apps-sdk-ui
```

```ts
// 样式入口（对应 KnowWork web/src/styles/index.css）
import '@openai/apps-sdk-ui/css';
```

```css
/* index.css：Tailwind v4 + 组件库令牌 + 中文字体补全（KnowWork 原文照搬） */
@import 'tailwindcss';
@import '@openai/apps-sdk-ui/css';
@source '../node_modules/@openai/apps-sdk-ui';

@theme {
  --font-sans: ui-sans-serif, -apple-system, system-ui, 'Segoe UI', 'Noto Sans', 'Helvetica',
               'Arial', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
}
```

组件（Button/Menu/Avatar/Badge/Icon/Input/Dialog…）与全部 `--color-* / --radius-* / --shadow-*` 令牌即开即用；主题用 `data-theme` 属性切。产品自有令牌（对应 KnowWork tokens.css）：

```css
:root {
  --kw-link: #2b7de9;
  --kw-radius-control: var(--radius-md);      /* 8px */
  --kw-radius-card: var(--radius-xl);         /* 12px */
  --kw-radius-card-lg: var(--radius-2xl);     /* 16px */
  --kw-radius-bubble: var(--radius-3xl);      /* 20px */
  --kw-font-xs: 12px;
  --kw-font-sm: 13px;
  --kw-font-base: 14px;
  --kw-font-chat: 15px;
  --kw-font-md: 16px;
  --kw-font-title: 20px;
  --kw-sidebar-width: 260px;
  --kw-shadow-input: 0 4px 16px rgb(0 0 0 / 6%);
  --kw-shadow-floating: var(--shadow-300), var(--shadow-hairline);
}
```

## 路线 B：自建 Token（Tailwind v4 无组件库 / Vue / 纯 HTML 通用）

```css
:root {
  /* 中性灰阶（亮） */
  --gray-0: #ffffff;   --gray-25: #fcfcfc; --gray-50: #f9f9f9; --gray-75: #f3f3f3;
  --gray-100: #ededed; --gray-150: #dfdfdf; --gray-200: #cdcdcd; --gray-300: #afafaf;
  --gray-400: #8f8f8f; --gray-500: #5d5d5d; --gray-600: #414141; --gray-700: #303030;
  --gray-800: #212121; --gray-900: #181818; --gray-950: #131313; --gray-1000: #0d0d0d;
  /* 表面 / 文字 / 边框（alpha 体系） */
  --surface: var(--gray-0);
  --surface-secondary: var(--gray-50);
  --surface-tertiary: var(--gray-75);
  --surface-elevated: var(--gray-0);
  --text: var(--gray-1000);
  --text-secondary: var(--gray-500);
  --text-tertiary: var(--gray-400);
  --on-accent: #ffffff;
  --backdrop: rgb(0 0 0 / 30%);
  --border-subtle: rgb(0 0 0 / 5%);
  --border: rgb(0 0 0 / 10%);
  --border-strong: rgb(0 0 0 / 15%);
  --border-focus: rgb(0 0 0 / 50%);
  --scrollbar: rgb(0 0 0 / 30%);
  /* 语义色 */
  --primary: var(--gray-900);        /* 主按钮黑（暗色主题下为白） */
  --primary-hover: var(--gray-700);
  --soft: var(--gray-100);           /* 次按钮/选中态底 */
  --soft-hover: var(--gray-150);
  --link: #2b7de9;
  --info: #0285ff;   --info-hover: #0169cc;   --info-text: #0169cc;
  --success: #00a240;                 --success-text: #00692a;
  --danger: #e02e2a;  --danger-hover: #ba2623; --danger-text: #911e1b;
  --warning: #e25507;                 --warning-text: #923b0f;
  --discovery: #924ff7;  --discovery-hover: #8046d9; --discovery-text: #532d8d;
  --status-neutral: var(--gray-400);
  /* 圆角 */
  --radius-2xs: 2px; --radius-xs: 4px; --radius-sm: 6px; --radius-md: 8px; --radius-lg: 10px;
  --radius-xl: 12px; --radius-2xl: 16px; --radius-3xl: 20px; --radius-4xl: 24px; --radius-full: 9999px;
  /* 阴影（elevation + hairline） */
  --shadow-100: 0 1px 2px -1px rgb(0 0 0 / 8%);
  --shadow-200: 0 2px 4px -1px rgb(0 0 0 / 8%);
  --shadow-300: 0 4px 8px -2px rgb(0 0 0 / 10%);
  --shadow-400: 0 8px 16px -2px rgb(0 0 0 / 12%);
  --shadow-hairline: 0 0 0 1px var(--border);
  /* 过渡 / 字号 / 尺寸 */
  --duration: 150ms;
  --ease: cubic-bezier(.4, 0, .2, 1);
  --font-xs: 12px; --font-sm: 13px; --font-base: 14px; --font-chat: 15px; --font-md: 16px; --font-title: 20px;
  --control-size-sm: 28px; --control-size-md: 32px; --control-size-lg: 36px;
  --icon-size: 16px;
  --sidebar-width: 260px;
  --chat-max-width: 760px;
  --font-sans: ui-sans-serif, -apple-system, system-ui, 'Segoe UI', 'Noto Sans', 'Helvetica', 'Arial', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  --font-mono: ui-monospace, 'SF Mono', 'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace;
}

[data-theme='dark'] {
  --gray-0: #0d0d0d;   --gray-25: #101010; --gray-50: #131313; --gray-75: #161616;
  --gray-100: #181818; --gray-150: #1c1c1c; --gray-200: #212121; --gray-300: #303030;
  --gray-400: #414141; --gray-500: #4f4f4f; --gray-600: #8f8f8f; --gray-700: #afafaf;
  --gray-800: #cdcdcd; --gray-900: #ededed; --gray-950: #f3f3f3; --gray-1000: #ffffff;
  --surface: var(--gray-200);
  --surface-secondary: var(--gray-100);
  --surface-tertiary: var(--gray-50);
  --surface-elevated: var(--gray-300);
  --text: var(--gray-1000);
  --text-secondary: var(--gray-700);
  --text-tertiary: var(--gray-600);
  --on-accent: #ffffff;
  --backdrop: rgb(0 0 0 / 50%);
  --border-subtle: rgb(255 255 255 / 6%);
  --border: rgb(255 255 255 / 12%);
  --border-strong: rgb(255 255 255 / 20%);
  --border-focus: rgb(255 255 255 / 50%);
  --scrollbar: rgb(255 255 255 / 30%);
  /* 主按钮在暗色下反转为白底黑字 */
  --primary: var(--gray-950);
  --primary-hover: var(--gray-900);
  --soft: var(--gray-300);
  --soft-hover: var(--gray-400);   /* 暗色 hover 应比 soft(#303030) 更亮，取最近登记档 gray-400(#414141)，替代不存在的 gray-350 */
  --info: #0285ff;  --info-text: #66b5ff;
  --success: #00a240; --success-text: #04b84c;
  --danger: #e02e2a;  --danger-text: #e02e2a;
  --warning: #e25507; --warning-text: #e25507;
  --discovery: #924ff7; --discovery-hover: #8046d9; --discovery-text: #be95fa;
  --status-neutral: var(--gray-400);
  --shadow-100: 0 1px 2px -1px rgb(0 0 0 / 20%);
  --shadow-200: 0 2px 4px -1px rgb(0 0 0 / 20%);
  --shadow-300: 0 4px 8px -2px rgb(0 0 0 / 36%);
  --shadow-400: 0 8px 16px -2px rgb(0 0 0 / 30%);
}
```

Tailwind v4 映射（`@theme inline`，语义类名与组件库一致）：

```css
@theme inline {
  --color-border: var(--border);
  --color-border-subtle: var(--border-subtle);
  --color-border-strong: var(--border-strong);
  --color-border-focus: var(--border-focus);
  --color-surface: var(--surface);
  --color-surface-secondary: var(--surface-secondary);
  --color-surface-tertiary: var(--surface-tertiary);
  --color-elevated: var(--surface-elevated);
  --color-foreground: var(--text);
  --color-secondary: var(--text-secondary);
  --color-tertiary: var(--text-tertiary);
  --color-primary: var(--primary);
  --color-primary-hover: var(--primary-hover);
  --color-on-accent: var(--on-accent);
  --color-soft: var(--soft);
  --color-soft-hover: var(--soft-hover);
  --color-link: var(--link);
  --color-info: var(--info);
  --color-success: var(--success);
  --color-danger: var(--danger);
  --color-warning: var(--warning);
  --color-discovery: var(--discovery);
  /* 圆角变量名与 Tailwind v4 主题命名空间同名：:root 直接覆盖默认值即可（apps-sdk 同款做法），
     无需在此映射——rounded-sm/md/lg/xl/2xl 自动取 6/8/10/12/16px，与路线 A 完全一致 */
}
```

## 语义类名速查（v2）

| 类名/变量 | 值 | 用途 |
| --- | --- | --- |
| `bg-surface` / `bg-surface-secondary` | `#fff` / `#f9f9f9` | 内容区 / 侧栏与页面底 |
| `text-foreground` / `text-secondary` / `text-tertiary` | `#0d0d0d` / `#5d5d5d` / `#8f8f8f` | 主/次/三级文字 |
| `border-border` / `border-border-subtle` | 黑 10% / 5% | 常规边框 / 行分隔与弱分隔 |
| `border-border-focus` | 黑/白 50% | 输入框焦点边框 |
| `bg-primary text-on-accent` | `#181818` + 白 | 主按钮（暗色主题自动反转为白底黑字） |
| `bg-soft` | `#ededed` | 次按钮、选中态、hover 底 |
| `bg-elevated` | surface-elevated | 浮层面（菜单/对话框） |
| `text-link` | `#2b7de9` | 链接；也是 focus-visible 描边色 |
| 状态点 | 绿 `#00a240` / 红 `#e02e2a` / 橙 `#fb6a22` / 蓝 `#0285ff` / 灰 `#8f8f8f`，6px 圆 | 运行状态 |
| `rounded-sm` / `rounded-md` / `rounded-lg` / `rounded-xl` / `rounded-2xl` | 6 / 8 / 10 / 12 / 16px | 小控件 / 控件 / 小卡片 / 卡片 / 弹窗 |
| `var(--shadow-300) + var(--shadow-hairline)` | elevation 组合 | 仅浮层 |
| `duration-150` | 150ms | 所有默认过渡 |
| `--ease-enter` / `--ease-exit` / `--ease-move` | 实测缓动曲线 | 进入 / 退出 / 位移（浮层动画专用） |
| `z-index: 1000 / 1001 / 1100 / 2000` | 层级档 | 遮罩 / 对话框·抽屉 / 菜单·气泡 / 轻提示 |
