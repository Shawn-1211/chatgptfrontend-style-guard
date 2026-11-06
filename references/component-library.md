# OpenaiStack v2 组件模板库（references/component-library.md）

> **定位**：写组件时的正例锚点与复制起点（v2 · KnowWork 实测体系）。
> **前提**：Token 已按 `references/design-tokens.md` 初始化（路线 A apps-sdk 或路线 B @theme inline）；类名即路线 B 的语义类。
> **约定**：层级（z-index）与阴影组合等非类名值用 `style` 内联写登记值；文件图标见 `references/framework-adapters.md` §7 注册表。
> **自查**：本文件已通过 `scripts/check-style.py`（0 ERROR）；新增模板也必须保持 0 ERROR。

## 1. Button（变体 × 尺寸档）

```html
<!-- 主按钮：黑实底（暗色主题自动反转白底），hover 150ms -->
<button class="inline-flex h-8 items-center justify-center gap-1.5 rounded-md bg-primary px-3 text-sm font-medium text-on-accent duration-150 hover:bg-primary-hover">主操作</button>
<!-- 次按钮 soft：灰底 -->
<button class="inline-flex h-8 items-center gap-1.5 rounded-md bg-soft px-3 text-sm font-medium text-foreground duration-150 hover:bg-soft-hover">次操作</button>
<!-- 描边 outline -->
<button class="inline-flex h-8 items-center gap-1.5 rounded-md border border-border-strong bg-surface px-3 text-sm font-medium text-foreground duration-150 hover:bg-soft">描边</button>
<!-- 幽灵 ghost -->
<button class="inline-flex h-8 items-center gap-1.5 rounded-md px-3 text-sm font-medium text-foreground duration-150 hover:bg-soft">幽灵</button>
<!-- 危险操作（需二次确认） -->
<button class="inline-flex h-8 items-center gap-1.5 rounded-md bg-danger px-3 text-sm font-medium text-on-accent duration-150">终止运行</button>
<!-- 文字链接 -->
<button class="text-sm text-link duration-150 hover:underline">文字链接</button>
<!-- 禁用态 -->
<button class="inline-flex h-8 items-center rounded-md bg-surface-tertiary px-3 text-sm font-medium text-tertiary" disabled>禁用</button>
```

尺寸档（高度）：`h-7` sm 28 / `h-8` md 32（默认）/ `h-9` lg 36 / `h-10` xl 40。

## 2. Card（12px 圆角，1px alpha 边框，无阴影）

```html
<section class="rounded-xl border border-border bg-surface p-6">
  <h3 class="text-lg font-semibold text-foreground">卡片标题</h3>
  <p class="mt-2 text-sm text-secondary">卡片靠 alpha 边框分层，不使用阴影。</p>
  <!-- 卡片内部分区：分隔线，禁止再嵌 Card -->
  <div class="mt-6 border-t border-border-subtle pt-4">…内容…</div>
</section>
```

## 3. 状态点（6px 语义圆点）与徽章（4px 圆角）

```html
<!-- 运行中：圆点居中、文字按基线（KnowWork 实测对齐方案） -->
<span class="inline-flex items-baseline gap-1.5 text-sm"><span class="h-1.5 w-1.5 self-center rounded-full bg-info"></span>运行中</span>
<!-- 已完成 -->
<span class="inline-flex items-baseline gap-1.5 text-sm"><span class="h-1.5 w-1.5 self-center rounded-full bg-success"></span>已完成</span>
<!-- 失败 -->
<span class="inline-flex items-baseline gap-1.5 text-sm"><span class="h-1.5 w-1.5 self-center rounded-full bg-danger"></span>失败</span>
<!-- 排队中 -->
<span class="inline-flex items-baseline gap-1.5 text-sm"><span class="h-1.5 w-1.5 self-center rounded-full bg-warning"></span>排队中</span>
<!-- 未启用 -->
<span class="inline-flex items-baseline gap-1.5 text-sm"><span class="h-1.5 w-1.5 self-center rounded-full bg-tertiary"></span>未启用</span>
```

```html
<!-- 徽章：4px 圆角、semibold，仅用于计数与标签类 -->
<span class="inline-flex h-5 items-center rounded-xs bg-primary px-1.5 text-xs font-semibold text-on-accent">3</span>
<span class="inline-flex h-5 items-center rounded-xs bg-soft px-1.5 text-xs font-semibold text-foreground">草稿</span>
<span class="inline-flex h-5 items-center rounded-xs border border-border-strong px-1.5 text-xs font-semibold text-secondary">审批中</span>
```

## 4. 表单（尺寸档 / 焦点 / 错误 / 禁用）

```html
<div class="flex flex-col gap-1.5">
  <label class="text-sm font-medium text-foreground">任务名称</label>
  <!-- 焦点态：边框加深至 --border-focus（黑/白 50%），150ms -->
  <input class="h-9 w-full rounded-md border border-border bg-surface px-3 text-sm text-foreground duration-150 placeholder:text-tertiary focus:border-border-focus focus:outline-none" placeholder="输入任务名称" />
  <span class="text-xs text-secondary">辅助说明</span>
</div>
<!-- 尺寸档：h-7 sm 28 / h-8 md 32 / h-9 lg 36 -->
<!-- 错误态：红边框 + 红字提示 -->
<input class="h-9 w-full rounded-md border border-danger bg-surface px-3 text-sm duration-150" value="zhang" />
<span class="text-xs text-danger">请输入工作邮箱</span>
<!-- 禁用态 -->
<input class="h-9 w-full rounded-md border border-border bg-surface-tertiary px-3 text-sm text-tertiary" value="禁用" disabled />
```

键盘焦点：自定义可点元素由全局 `:focus-visible` 描边兜底（2px link 色 + 2px offset），禁止移除一切焦点指示。

## 5. Table（v2：表头无底色）

```html
<div class="overflow-x-auto rounded-xl border border-border bg-surface">
  <table class="w-full text-sm">
    <thead>
      <tr>
        <th class="border-b border-border px-3 py-2 text-left text-xs font-medium text-secondary">任务</th>
        <th class="border-b border-border px-3 py-2 text-left text-xs font-medium text-secondary">状态</th>
        <th class="border-b border-border px-3 py-2 text-right text-xs font-medium text-secondary">金额</th>
      </tr>
    </thead>
    <tbody>
      <tr class="duration-150 hover:bg-surface-tertiary">
        <td class="border-b border-border-subtle px-3 py-2.5 text-foreground">数据归集 · 每日增量</td>
        <td class="border-b border-border-subtle px-3 py-2.5"><!-- 状态点见 §3 --></td>
        <td class="border-b border-border-subtle px-3 py-2.5 text-right tabular-nums">¥86,400</td>
      </tr>
    </tbody>
  </table>
</div>
```

关键点：表头 12px 次文字色、**无底色**（与 v1 的表头灰底不同）；行 padding 10px 12px；行分隔 border-subtle；数字 `tabular-nums` + 右对齐。

## 6. Menu（菜单面板 / 危险项 / 分隔线）

```html
<div class="relative">
  <button class="inline-flex h-9 items-center gap-2 rounded-md px-3 text-sm text-foreground duration-150 hover:bg-soft">账号菜单</button>
  <!-- 面板：层级 1100（登记档），阴影 = shadow-300 + hairline 组合，150ms ease-enter -->
  <div class="absolute bottom-12 left-0 flex w-56 flex-col gap-0.5 rounded-xl bg-elevated p-1.5" style="z-index: 1100; box-shadow: var(--shadow-300), var(--shadow-hairline);">
    <button class="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-foreground duration-150 hover:bg-soft">个人设置</button>
    <button class="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-foreground duration-150 hover:bg-soft">回答语言<span class="ml-auto text-xs text-secondary">中文</span></button>
    <div class="my-1.5 h-px bg-border"></div>
    <button class="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-danger duration-150 hover:bg-soft">退出登录</button>
  </div>
</div>
```

关键点：这是左下角用户菜单的通用形态；危险操作用 `text-danger` 红字（不用实底红块）。

## 7. Dialog（遮罩 1000 / 对话框 200ms ease-enter）

```html
<div class="fixed inset-0 flex items-center justify-center p-4" style="z-index: 1000; background: var(--backdrop);">
  <div class="w-full rounded-2xl bg-elevated p-5" style="max-width: 450px; box-shadow: var(--shadow-400);">
    <h3 class="text-lg font-semibold text-foreground">确认提交？</h3>
    <p class="mt-1 text-sm text-secondary">提交后进入审批流，确认前仍可撤回。</p>
    <div class="mt-5 flex justify-end gap-2">
      <button class="inline-flex h-8 items-center rounded-md bg-soft px-3 text-sm font-medium text-foreground duration-150 hover:bg-soft-hover">取消</button>
      <button class="inline-flex h-8 items-center rounded-md bg-primary px-3 text-sm font-medium text-on-accent duration-150 hover:bg-primary-hover">确认</button>
    </div>
  </div>
</div>
```

关键点：宽 250–450px、内边距 20px（实测）、圆角 16、进入 `--ease-enter` 200ms。

## 8. Drawer / 抽屉（右滑 220ms ease-move，层级 1001）

```html
<div class="fixed bottom-0 right-0 top-0 flex w-80 flex-col bg-surface" style="z-index: 1001; box-shadow: var(--shadow-400);">
  <div class="flex items-center gap-2 border-b border-border-subtle px-3 py-2" style="min-height: 52px;">
    <h3 class="flex-1 text-md font-semibold text-foreground">运行信息</h3>
    <button class="flex h-8 items-center rounded-md px-3 text-sm text-secondary duration-150 hover:bg-soft" aria-label="关闭抽屉">关闭</button>
  </div>
  <div class="flex-1 overflow-y-auto px-5 pb-6 pt-4">
    <!-- 详情键值行 -->
    <div class="grid gap-3 border-b border-border-subtle py-2 text-sm" style="grid-template-columns: 120px minmax(0, 1fr);">
      <dt class="text-secondary">状态</dt><dd><!-- 状态点见 §3 --></dd>
    </div>
  </div>
</div>
```

## 9. Toast（黑胶囊，层级 2000，180ms ease-enter）

```html
<div class="fixed left-1/2 top-6 flex -translate-x-1/2 items-center gap-2 rounded-full px-4 py-2 text-sm" style="z-index: 2000; background: var(--gray-900); color: var(--gray-0); box-shadow: var(--shadow-300);">
  已保存草稿
</div>
```

关键点：底/字用 `--gray-900`/`--gray-0` 双引用——暗色主题下自动反转为浅底深字（实测同款）。

## 10. Tabs（下划线式二级菜单）

```html
<nav class="flex items-center gap-6 border-b border-border px-6 py-2">
  <button class="border-b-2 border-foreground pb-2.5 text-sm font-medium text-foreground">全部任务</button>
  <button class="border-b-2 border-transparent pb-2.5 text-sm font-medium text-secondary duration-150 hover:text-foreground">我创建的</button>
  <button class="border-b-2 border-transparent pb-2.5 text-sm font-medium text-secondary duration-150 hover:text-foreground">共享给我</button>
</nav>
```

## 11. 企业级分区（非卡片嵌套）

```html
<section class="rounded-md border border-border-subtle bg-surface-tertiary p-4">
  <h4 class="text-sm font-medium text-foreground">审批与权限</h4>
  <p class="mt-2 text-xs text-secondary">分区 = 1px subtle 边框 + 三级浅灰底；子块只换底色不加边框。</p>
  <div class="mt-4 grid grid-cols-2 gap-4">
    <div class="rounded-md bg-surface p-4"><h5 class="text-sm font-medium">权限管控</h5><p class="mt-2 text-xs text-secondary">价格库仅管理员可维护。</p></div>
    <div class="rounded-md bg-surface p-4"><h5 class="text-sm font-medium">审批流</h5><p class="mt-2 text-xs text-secondary">折扣超 15% 加签总监。</p></div>
  </div>
</section>
```

## 12. 空状态 / 骨架屏 / 生成中指示

```html
<!-- 空状态 -->
<div class="rounded-xl border border-dashed border-border-subtle bg-surface p-10 text-center">
  <p class="text-sm text-secondary">暂无任务</p>
</div>
<!-- 骨架屏：14px 高、radius 6，仅加载态允许的循环动画 -->
<div class="flex flex-col gap-3">
  <div class="h-3.5 w-4/5 rounded-sm bg-surface-tertiary" style="animation: pulse 1.4s ease-in-out infinite;"></div>
  <div class="h-3.5 w-3/5 rounded-sm bg-surface-tertiary" style="animation: pulse 1.4s ease-in-out infinite;"></div>
</div>
<!-- 生成中三点：AI 流式输出指示，错峰 0.2s -->
<span class="inline-flex items-center gap-1">
  <span class="h-1.5 w-1.5 rounded-full bg-tertiary" style="animation: gen-wave 1.2s ease-in-out infinite;"></span>
  <span class="h-1.5 w-1.5 rounded-full bg-tertiary" style="animation: gen-wave 1.2s ease-in-out infinite; animation-delay: 0.2s;"></span>
  <span class="h-1.5 w-1.5 rounded-full bg-tertiary" style="animation: gen-wave 1.2s ease-in-out infinite; animation-delay: 0.4s;"></span>
</span>
```

## 13. 文件类型图标

走注册表（类别形 × 登记语义色 × 扩展名文字，未注册自动兜底），规则与实现见 `references/framework-adapters.md` §7——新增格式只加注册表行，不加颜色、不加组件。
