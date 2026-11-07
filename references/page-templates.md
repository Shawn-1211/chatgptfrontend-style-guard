# OpenaiStack v2 页面骨架（references/page-templates.md）

> **定位**：写页面时的布局起点（v2 · KnowWork 实测体系），全部通过 `scripts/check-style.py`（0 ERROR）。
> **前提**：Token 已按 `references/design-tokens.md` 初始化；组件细部直接引用 `references/component-library.md`。

## 1. 应用骨架（侧边栏 260px + 可展开二级菜单 + 下划线 Tabs + 卡片内容区）

```html
<!-- 整页永不滚动：外壳 overflow-clip，只有内容层滚 -->
<div class="flex h-screen overflow-clip bg-surface">
  <!-- 一级侧边栏：260px（折叠 60px，160ms ease） -->
  <aside class="flex flex-col px-2 py-3" style="width: var(--sidebar-width);">
    <div class="flex items-center gap-2 px-3 pb-2">
      <span class="h-6 w-6 rounded-sm bg-primary"></span>
      <span class="text-md font-semibold text-foreground">Agent 控制台</span>
    </div>
    <nav class="flex flex-col gap-0.5">
      <!-- 选中态 = 浅灰底（与 hover 同款），禁止彩色实底 -->
      <a class="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-foreground duration-150 hover:bg-soft" href="#workbench">工作台</a>
      <!-- 可展开一级项 + 二级菜单（v2.3）：形态见 component-library §14 -->
      <div role="treeitem" aria-expanded="true" class="flex flex-col gap-0.5">
        <div class="flex items-center gap-2 rounded-md py-2 pr-1.5" style="padding-left: 8px;">
          <button type="button" class="inline-flex h-5 w-5 flex-none items-center justify-center rounded-xs text-secondary duration-150 hover:bg-soft" aria-label="收起" aria-expanded="true">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l4 4 4-4"/></svg>
          </button>
          <a class="min-w-0 flex-1 truncate bg-soft rounded-md px-2 py-2 text-sm font-medium text-foreground" href="#tasks">任务管理</a>
        </div>
        <div class="flex items-center gap-2 rounded-md py-2 pr-1.5" style="padding-left: 20px;">
          <span class="inline-flex h-5 w-5 flex-none" aria-hidden="true"></span>
          <a class="min-w-0 flex-1 truncate rounded-md bg-surface-tertiary px-2 py-2 text-sm text-foreground" href="#tasks-all">全部任务</a>
        </div>
        <div class="flex items-center gap-2 rounded-md py-2 pr-1.5" style="padding-left: 20px;">
          <span class="inline-flex h-5 w-5 flex-none" aria-hidden="true"></span>
          <a class="min-w-0 flex-1 truncate rounded-md px-2 py-2 text-sm text-foreground duration-150 hover:bg-soft" href="#tasks-mine">我创建的</a>
        </div>
      </div>
      <a class="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-foreground duration-150 hover:bg-soft" href="#knowledge">知识库</a>
    </nav>

    <!-- 左下角固定区：用户菜单（mt-auto 钉底），设置藏在菜单内，不设独立"系统设置"侧栏项 -->
    <div class="relative mt-auto border-t border-border pt-2">
      <button class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-left text-sm text-foreground duration-150 hover:bg-soft">
        <span class="flex h-7 w-7 flex-none items-center justify-center rounded-full bg-surface-tertiary text-xs font-semibold text-secondary">李</span>
        <span class="flex min-w-0 flex-col leading-tight">
          <span class="truncate text-sm">李工</span>
          <small class="truncate text-xs text-secondary">li@zhigong.ai</small>
        </span>
      </button>
      <!-- 菜单面板（个人设置 / 回答语言 / 管理后台 / 退出登录）见 component-library §6 -->
    </div>
  </aside>

  <div class="flex min-w-0 flex-1 flex-col overflow-clip bg-surface">
    <!-- 顶部二级导航：下划线式 Tabs（与侧栏可展开菜单是两种形态，勿混用） -->
    <nav class="flex items-center gap-6 border-b border-border px-6 py-2">
      <button class="border-b-2 border-foreground pb-2.5 text-sm font-medium text-foreground">全部任务</button>
      <button class="border-b-2 border-transparent pb-2.5 text-sm font-medium text-secondary duration-150 hover:text-foreground">我创建的</button>
      <button class="border-b-2 border-transparent pb-2.5 text-sm font-medium text-secondary duration-150 hover:text-foreground">共享给我</button>
    </nav>
    <!-- 卡片内容区：唯一滚动层 -->
    <main class="flex-1 overflow-y-auto p-8">
      <!-- 页面内容（见下方模板） -->
    </main>
  </div>
</div>
```

关键点：侧栏 260px、选中态灰底无彩色；一级项可展开下挂二级菜单（缩进首层 20px、树内选中 surface-tertiary）；左下角用户菜单 + border-top 分隔；整页 `overflow-clip`；正文基准 14px。

## 2. 列表页（页头 + 统计卡 + 表格 + 企业级分区）

```html
<header class="mb-6 flex items-center justify-between gap-4">
  <div>
    <h1 class="text-xl font-semibold text-foreground">Agent 任务面板</h1>
    <p class="mt-2 text-sm text-secondary">查看与管理系统内全部任务</p>
  </div>
  <button class="inline-flex h-8 items-center gap-1.5 rounded-md bg-primary px-3 text-sm font-medium text-on-accent duration-150 hover:bg-primary-hover">新建任务</button>
</header>

<!-- 统计卡：语义色数值 -->
<section class="mb-6 grid grid-cols-4 gap-4">
  <div class="rounded-xl border border-border bg-surface p-6">
    <p class="text-sm text-secondary">运行中</p>
    <p class="mt-2 text-xl font-semibold text-info">2</p>
  </div>
  <div class="rounded-xl border border-border bg-surface p-6">
    <p class="text-sm text-secondary">已完成</p>
    <p class="mt-2 text-xl font-semibold text-success">128</p>
  </div>
  <div class="rounded-xl border border-border bg-surface p-6">
    <p class="text-sm text-secondary">失败</p>
    <p class="mt-2 text-xl font-semibold text-danger">3</p>
  </div>
  <div class="rounded-xl border border-border bg-surface p-6">
    <p class="text-sm text-secondary">排队中</p>
    <p class="mt-2 text-xl font-semibold text-warning">5</p>
  </div>
</section>

<!-- 任务表格（component-library §5）+ 企业级分区（§11） -->
```

关键点：统计数值直接用语义色文字（info/success/danger/warning），状态可扫描；mb-6=24px 页头间距。

## 3. 详情页（主内容 + 信息栏 + 键值行）

```html
<div class="grid grid-cols-3 gap-4">
  <section class="col-span-2 rounded-xl border border-border bg-surface p-6">
    <h1 class="text-xl font-semibold text-foreground">任务 #1024</h1>
    <p class="mt-2 text-sm text-secondary">数据归集 · 每日增量 · 调度器触发</p>
    <div class="mt-8 border-t border-border-subtle pt-4">
      <!-- 运行日志 / 结果 -->
    </div>
  </section>
  <aside class="rounded-xl border border-border bg-surface p-6">
    <h3 class="text-md font-semibold text-foreground">运行信息</h3>
    <div class="mt-4 flex flex-col gap-4 text-sm">
      <div class="grid gap-3 border-b border-border-subtle py-2" style="grid-template-columns: 120px minmax(0, 1fr);">
        <dt class="text-secondary">状态</dt><dd><!-- 状态点 --></dd>
      </div>
      <div class="grid gap-3 border-b border-border-subtle py-2" style="grid-template-columns: 120px minmax(0, 1fr);">
        <dt class="text-secondary">负责人</dt><dd>李工</dd>
      </div>
      <div class="grid gap-3 py-2" style="grid-template-columns: 120px minmax(0, 1fr);">
        <dt class="text-secondary">累计金额</dt><dd class="tabular-nums">¥1,286,400</dd>
      </div>
    </div>
  </aside>
</div>
```

关键点：键值行用登记的 120px 标签宽 + subtle 分隔（实测 descriptions 形态）；金额 tabular-nums。

## 4. 登录页（居中卡片，实测 380px / 圆角 16 / 内边距 32）

```html
<main class="flex min-h-screen items-center justify-center bg-surface-secondary p-4">
  <section class="w-full rounded-2xl border border-border bg-surface p-8" style="max-width: 380px;">
    <h1 class="text-xl font-semibold text-foreground">登录 Agent 控制台</h1>
    <p class="mt-2 text-sm text-secondary">使用工作邮箱登录</p>
    <form class="mt-8 flex flex-col gap-4">
      <!-- 表单项见 component-library §4；尺寸用 lg 36 -->
      <button type="submit" class="mt-1 h-9 w-full rounded-md bg-primary text-sm font-medium text-on-accent duration-150 hover:bg-primary-hover">登录</button>
    </form>
  </section>
</main>
```

关键点：主按钮黑实底（暗色主题反转白底）；输入框 lg 36px（登录页同款）。

## 5. 设置页（企业级分区示范）

```html
<section class="rounded-xl border border-border bg-surface p-6">
  <h3 class="text-md font-semibold text-foreground">权限与安全</h3>
  <!-- 分区块：border-subtle + surface-tertiary，不是嵌套卡片 -->
  <div class="mt-4 rounded-md border border-border-subtle bg-surface-tertiary p-4">
    <h4 class="text-sm font-medium text-foreground">权限管控</h4>
    <p class="mt-2 text-xs text-secondary">仅管理员可修改运行配置与知识库发布权限。</p>
  </div>
  <div class="mt-4 rounded-md border border-border-subtle bg-surface-tertiary p-4">
    <h4 class="text-sm font-medium text-foreground">沙箱隔离</h4>
    <p class="mt-2 text-xs text-secondary">Agent 文件与网络操作默认在沙箱内执行。</p>
  </div>
  <div class="mt-4 rounded-md border border-border-subtle bg-surface-tertiary p-4">
    <h4 class="text-sm font-medium text-foreground">审批流程</h4>
    <p class="mt-2 text-xs text-secondary">生产环境执行需两名管理员审批。</p>
  </div>
</section>
```

关键点：Card 内部只放分区块，**不出现 Card 套 Card**；分区标题 text-sm + medium。
