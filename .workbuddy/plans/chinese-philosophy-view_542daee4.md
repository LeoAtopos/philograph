---
name: chinese-philosophy-view
overview: 在现有哲学史可视化网站基础上，新增完整的中国哲学数据集（约20位哲学家，儒道墨法等），并在顶部导航栏添加"东方 ⇄ 西方"切换按钮，实现两套数据集的无缝视图切换。
design:
  architecture:
    framework: html
  styleKeywords:
    - Academic Visualization
    - Pill Tab Switcher
    - Dark Theme
    - Sliding Indicator
  fontSystem:
    fontFamily: Inter, sans-serif
    heading:
      size: 12px
      weight: 600
    subheading:
      size: 11px
      weight: 500
    body:
      size: 11px
      weight: 400
  colorSystem:
    primary:
      - "#4ade80"
      - "#f87171"
    background:
      - "#0f1117"
      - "#1a1e3a"
    text:
      - "#e8eaf0"
      - "#9ca3b8"
      - "#5a6282"
    functional:
      - "#4ade80"
      - "#f87171"
      - "#fbbf24"
todos:
  - id: create-chinese-data
    content: 创建中国哲学家数据文件 chinese-philosophers.json 和 chinese-connections.json（约20位哲学家+关系连线）
    status: completed
  - id: add-tradition-switcher
    content: 在 index.html topbar 中新增 Western/Chinese 切换按钮 HTML 结构
    status: completed
  - id: add-css-styles
    content: 在 main.css 中新增 tradition-switcher 样式和中国哲学 tag 颜色变量
    status: completed
  - id: update-state-module
    content: 修改 state.js 新增 currentTradition、数据缓存、switchTradition() 和 getEraOrder()
    status: completed
    dependencies:
      - create-chinese-data
  - id: update-card-renderer
    content: 修改 card-renderer.js：ERA_ORDER 动态化、getTagClass 扩展、新增 rerender()
    status: completed
    dependencies:
      - create-chinese-data
  - id: update-theme-app
    content: 修改 theme.js 和 app.js：实现 switchView 协调逻辑、动态过滤器面板、预加载中国数据
    status: completed
    dependencies:
      - add-tradition-switcher
      - add-css-styles
      - update-state-module
      - update-card-renderer
---

## Product Overview

在现有西方哲学可视化网站基础上，新增中国哲学家数据集，并在顶部导航栏添加"Western / Chinese"切换按钮，实现两套哲学体系的视图切换。

## Core Features

- 新增中国哲学数据集：约20位哲学家（先秦→汉→宋明→近现代），包含真实的思想观点和思想关系连线
- 顶部导航栏增加 Tab 切换组件："Western" 与 "Chinese"，带滑动指示器和过渡动画
- 切换视图时：重置画布位置、重新渲染卡片和连线、更新左侧面板过滤器标签和 INDEX 列表
- 中国哲学过滤器使用独立标签体系：儒学、道家、墨家、法家、佛学、理学、心学、政治哲学、伦理学、认识论、美学、形而上学
- 两套数据预加载，切换时无等待

## Tech Stack

- 复用现有纯 HTML + CSS + JavaScript 架构，无框架依赖

## Implementation Approach

采用数据预加载 + 视图切换策略。应用启动时同时加载两套 JSON 数据并缓存在 State 中，切换时仅需替换 `philosophers` 和 `connections`、重建内部映射（buildMaps）、清空并重新渲染 DOM，避免网络请求延迟。

核心改动点：

1. **数据层**：新增 `data/chinese-philosophers.json` 和 `data/chinese-connections.json`，数据格式与西方完全一致（`id, name, born, died, era, portrait, tags, ideas`），但使用中国哲学特有的 era 值（`Pre-Qin, Han, Tang-Song, Ming-Qing, Modern`）和 tags（`Confucianism, Taoism, Mohism, Legalism, Buddhism, Neo-Confucianism, Mind, Political, Ethics, Epistemology, Aesthetics, Metaphysics`）
2. **State**：新增 `currentTradition`（`'western'|'chinese'`）、`chinesePhilosophers`、`chineseConnections` 字段；新增 `switchTradition(tradition)` 方法，负责切换数据集、重建映射、重置过滤器和选中状态
3. **CardRenderer**：`ERA_ORDER` 改为根据当前 tradition 动态选择（`state.js` 中新增 `getEraOrder(tradition)`）；`getTagClass()` 扩展支持中国哲学 tag 映射；新增 `rerender()` 公共方法（清空容器后调用现有 `render()`）
4. **ThemeController**：新增 `buildFilterPanel(tradition)` 方法，动态生成 filter-list 内的 checkbox；新增 `switchView(tradition)` 协调方法，依次调用 State.switchTradition → buildFilterPanel → CardRenderer.rerender → ConnectionRenderer.render → buildIndex → CanvasManager.resetView
5. **CSS**：新增 `.tradition-switcher` 样式（pill-shaped tab button with sliding indicator），新增中国哲学 tag 颜色 CSS 变量，确保移动端适配

## Implementation Notes

- 切换动画：画布内容使用 opacity fade-out/fade-in 过渡（0.3s），避免突兀跳变
- `buildFilterPanel` 在 HTML 中保留 `filterList` 容器，由 JS 动态填充 checkbox 元素，避免维护两套硬编码 HTML
- 中国哲学的 tag 颜色在 `:root` 中新增 `--tag-confucianism, --tag-taoism, --tag-mohism` 等 CSS 变量
- 过滤器的 All/None 按钮逻辑需适配动态 tag 列表，从当前 activeFilters 获取 tag 集合
- 切换时需先执行 `SelectionManager.clearAll()` 清除高亮状态

## Architecture Design

```
                    ┌─────────────────────┐
                    │  Tradition Switcher  │ (topbar tab)
                    └─────────┬───────────┘
                              │ click
                    ┌─────────▼───────────┐
                    │ ThemeController      │
                    │  .switchView()       │
                    └──┬──────┬───────┬───┘
                       │      │       │
            ┌──────────▼┐ ┌──▼────┐ ┌─▼────────────┐
            │ State      │ │Filter │ │ Index        │
            │.switchTrad │ │Panel  │ │ .buildIndex()│
            └──────────┬┘ └───────┘ └──────────────┘
                       │
              ┌────────▼────────┐
              │ CardRenderer     │
              │  .rerender()    │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │ ConnectionRenderer│
              │  .render()       │
              └─────────────────┘
```

## Directory Structure

```
philograph/
├── index.html                      # [MODIFY] topbar 中新增 tradition-switcher 组件 HTML
├── css/
│   └── main.css                    # [MODIFY] 新增 tradition-switcher 样式 + 中国哲学 tag 颜色变量
├── js/
│   ├── state.js                    # [MODIFY] 新增 currentTradition、缓存数据、switchTradition()、getEraOrder()
│   ├── app.js                      # [MODIFY] 预加载中国哲学 JSON，初始化后调用 switchView
│   ├── card-renderer.js            # [MODIFY] ERA_ORDER 改为动态获取；getTagClass 扩展；新增 rerender()
│   ├── theme.js                    # [MODIFY] 新增 switchView()、buildFilterPanel()、动态绑定过滤器事件
│   └── canvas-manager.js           # [MODIFY] 无修改（resetView 通用）
├── data/
│   ├── philosophers.json           # [保留] 西方哲学家数据（不变）
│   ├── connections.json            # [保留] 西方连线数据（不变）
│   ├── chinese-philosophers.json   # [NEW] 中国哲学家数据（约20位）
│   └── chinese-connections.json    # [NEW] 中国哲学关系连线数据
```

## Design Approach

保持现有学术可视化暗色主题风格，在顶部导航栏中央位置新增一个 pill-shaped Tab 切换器，包含 "Western" 和 "Chinese" 两个选项，配有滑动背景指示器动画。切换时画布内容带有淡入淡出过渡效果。

## Page Changes

顶部导航栏布局调整为三段式：左侧（菜单+标题）、中间（Tradition Switcher）、右侧（图例+About）。切换器使用胶囊形按钮，当前选中项有亮色背景滑动指示器，整体风格与现有深色主题一致。

## Agent Extensions

### Skill

- **lucide-icons**
- Purpose: 下载切换按钮所需的小图标资源
- Expected outcome: 获取西方/中国哲学对应的图标 SVG