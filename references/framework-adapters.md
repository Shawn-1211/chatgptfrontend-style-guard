# OpenaiStack 框架适配器（references/framework-adapters.md）

> **定位**：确定技术栈后读本文件，把 Token 接入对应的框架/技术路线。类名在所有框架下完全一致（Tailwind 语义类名跨框架通用）。

## 1. React 项目（路线 A，推荐）

直接安装并引入 `@openai/apps-sdk-ui`，见 `references/design-tokens.md` 路线 A（KnowWork 同款令牌与组件，含 Button/Menu/Avatar/Badge/Icon/Input/Dialog 全套）。

## 2. Tailwind v4 自建（路线 B）

按 `references/design-tokens.md` 路线 B 的 `@theme inline` 注册语义类名；圆角变量与 v4 主题命名空间同名，:root 直接覆盖默认值，类名与路线 A 完全一致。

## 3. React + shadcn/ui（路线 B 场景）

- 若沿用 shadcn/ui，组件本体可继续用，但**类名按路线 B 映射改写**：`bg-background`→`bg-surface`、`text-muted-foreground`→`text-tertiary`、`text-primary-foreground`→`text-on-accent`、`bg-muted`→`bg-soft`；卡片去掉自带阴影；
- **运行状态优先用 6px 状态点**（见 component-library §3），徽章只用于计数/标签：

```tsx
// 徽章变体（v2：4px 圆角、semibold）
const badgeVariants = cva(
  "inline-flex h-5 items-center rounded-xs px-1.5 text-xs font-semibold text-on-accent",
  {
    variants: {
      variant: {
        solid: "bg-primary",
        success: "bg-success",
        danger: "bg-danger",
        warning: "bg-warning",
        soft: "bg-soft text-foreground",
        outline: "border border-border-strong text-secondary",
      },
    },
    defaultVariants: { variant: "soft" },
  }
)
// 状态映射：运行中→状态点(蓝) / 已完成→success / 失败→danger / 排队→warning；运行态不用实底徽章
```

## 4. Vue 3（自建）

类名与 React 完全一致；状态点组件示例（v2 首选形态）：

```vue
<!-- components/StatusDot.vue -->
<script setup lang="ts">
type Status = 'run' | 'ok' | 'err' | 'wait' | 'off'
const props = defineProps<{ status: Status }>()
const LABELS: Record<Status, string> = { run: '运行中', ok: '已完成', err: '失败', wait: '排队中', off: '未启用' }
const MAP: Record<Status, string> = {
  run: 'bg-info', ok: 'bg-success', err: 'bg-danger', wait: 'bg-warning', off: 'bg-tertiary',
}
</script>

<template>
  <!-- 圆点 6px 居中、文字按基线（实测对齐方案） -->
  <span class="inline-flex items-baseline gap-1.5 text-sm">
    <i class="h-1.5 w-1.5 self-center rounded-full" :class="MAP[props.status]" />
    {{ LABELS[props.status] }}
  </span>
</template>
```

## 5. 纯 HTML / CSS 项目（无 Tailwind）

1. 把 `references/design-tokens.md` 路线 B 的 `:root` / `[data-theme='dark']` 变量复制进全局 `<style>`；
2. 手写类时**只引用 var()**，禁止任何 Hex / 未登记间距 / 圆角 / 时长：

```css
.btn {
  height: 36px;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;          /* var(--radius-md) */
  background: var(--primary);
  color: var(--on-accent);
  font-size: 14px;            /* UI 档内 */
  font-weight: 500;
  cursor: pointer;
  transition: background-color 150ms;
}
.btn:hover { background: var(--primary-hover); }
```

3. 完整可运行的参照实现见 `demo/openaistack-v2-test.html`（浏览器直接打开，含明暗主题切换与全部交互）。

## 6. 审查接入

- 开发中 / 提交前：`python scripts/check-style.py src`（Windows 同）；
- pre-commit 示例：`python scripts/check-style.py src || exit 1`；
- CI：脚本退出码 ERROR=1 / 干净=0，可直接作为流水线门禁。

脚本管机械项（R1 颜色 / R2 间距档 / R3 圆角档 / R4 任意像素值 / R5 字号档 / R6 渐变 / R7 阴影体系 / R8 背景图 / R9 时长档 / R10 层级白名单 / R11 Token 引用登记），语义项按 SKILL.md §五 人工/模型审查。

## 7. 文件类型图标注册表（FileKindIcon · v2）

> 解决"格式无限扩展"：**格式进注册表，颜色只从登记语义色取，类别形有限，未注册走兜底**。新增 .md / .dwg 只改注册表——不加颜色、不加图标组件。

### 7.1 规则

1. 文件图标 = 彩色圆角方块（radius-xs 4px）+ 白色类别形（--on-accent）+ 旁侧扩展名文字；
2. **类别形按"大类"而非"格式"**，共 5 类：文档 / 表格 / 演示 / 图纸 / 压缩；
3. **颜色 = 类别色**，只从 SKILL.md §1.3 登记语义色取；同类别格式同色，靠扩展名文字区分；**个别格式可按惯例覆盖类别色**（如 PDF 惯例红），覆盖色同样只取登记语义色；
4. **未注册格式兜底**：中性灰（gray-500）+ 通用文档形 + 扩展名大写文字——任何新格式立即有正确表示，永不缺图；
5. 需要新类别色时：先从实测色板（references/knowwork-analysis.md §2）选色 → 登记 SKILL.md §1.3 → design-tokens 落地 → 注册表加类别。

### 7.2 注册表

| 类别 | 扩展名 | 颜色 Token | 备注 |
| --- | --- | --- | --- |
| 文档 doc | pdf | `--danger` 红 | PDF 惯例红 |
| 文档 doc | doc / docx / md / txt / rtf | `--info` 蓝 | **md 零新增**：文档类复用蓝，扩展名文字区分 |
| 表格 sheet | xls / xlsx / csv | `--success` 绿 | |
| 演示 slide | ppt / pptx | `--warning` 橙 | |
| 图纸 cad | dwg / dxf / step / stp / iges | `--discovery` 紫（按登记路径新增，实测色板取值） | 图纸 / CAD 行业核心类 |
| 压缩 archive | zip / rar / 7z / tar | `--gray-500` 灰 | |
| 未知 fallback | 其他任意 | `--gray-500` + 通用形 + 扩展名文字 | 兜底，永不缺图 |

### 7.3 实现（React）

```tsx
const CATS = {
  doc: 'var(--info)', sheet: 'var(--success)', slide: 'var(--warning)',
  cad: 'var(--discovery)', archive: 'var(--gray-500)',
} as const

const KINDS: Record<string, string> = {
  pdf: 'doc',
  doc: 'doc', docx: 'doc', md: 'doc', txt: 'doc',
  xls: 'sheet', xlsx: 'sheet', csv: 'sheet',
  ppt: 'slide', pptx: 'slide',
  dwg: 'cad', dxf: 'cad', step: 'cad', stp: 'cad',
  zip: 'archive', rar: 'archive',
}

/* 惯例覆盖：个别格式按惯例单独着色，同样只取登记语义色 */
const OVERRIDE: Record<string, string> = { pdf: 'var(--danger)' }

/** 未注册格式自然落入 archive 兜底色 + 通用形；扩展名文字由调用方渲染 */
export function FileKindIcon({ ext, size = 32 }: { ext: string; size?: number }) {
  const e = ext.toLowerCase()
  const cat = KINDS[e] ?? 'archive'
  return (
    <span style={{ width: size, height: size,
                   background: OVERRIDE[e] ?? CATS[cat],
                   borderRadius: 'var(--radius-xs)', color: 'var(--on-accent)',
                   display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
      <CatGlyph cat={cat} />  {/* 5 个类别形，复用同一套 SVG */}
    </span>
  )
}
```

### 7.4 新增一个格式的三种情况

| 情况 | 做法 |
| --- | --- |
| 同类别（如 .md、.rtf → 文档类） | 注册表 KINDS 加一行 → 完成，**零新增颜色** |
| 新类别（如 .dwg → 图纸类） | ① 实测色板选色 → ② SKILL.md §1.3 登记 → ③ design-tokens 落地 → ④ 注册表加类别与行 |
| 未知 / 暂不收录 | **什么都不做**——兜底自动生效（灰底 + 通用形 + 扩展名文字） |
