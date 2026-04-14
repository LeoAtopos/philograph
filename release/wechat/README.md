# Philograph — 微信小程序版本

哲学史可视化应用的微信小程序适配版本。

## 目录结构

```
release/wechat/
├── app.js              # 小程序全局入口
├── app.json            # 小程序全局配置
├── app.wxss            # 全局样式和 CSS 变量
├── sitemap.json        # 微信搜索索引
├── pages/
│   ├── index/          # 主页（哲学家列表 + 筛选 + 索引）
│   │   ├── index.js
│   │   ├── index.wxml
│   │   ├── index.wxss
│   │   └── index.json
│   └── detail/         # 哲学家详情页（思想条目 + 连线关系）
│       ├── detail.js
│       ├── detail.wxml
│       ├── detail.wxss
│       └── detail.json
├── utils/
│   ├── i18n.js         # 多语言模块（CommonJS）
│   └── i18n-data.js    # 翻译数据（从 js/i18n-data.js 自动生成）
└── data/
    ├── philosophers.js          # 50 位西方哲学家
    ├── chinese-philosophers.js  # 50 位中国哲学家
    ├── connections.js           # 175 条西方连线
    └── chinese-connections.js   # 158 条中国连线
```

## 与网页版的差异

| 功能 | 网页版 | 小程序版 |
|------|--------|---------|
| 布局 | 无限横向画布 | 竖向滚动列表 |
| 交互 | 鼠标拖拽/缩放 | 点击卡片进入详情 |
| 连线展示 | SVG 曲线覆盖图谱 | 详情页中文字列表 |
| 筛选 | 侧边栏 | 下拉面板 |
| 索引 | 侧边栏 | 右侧抽屉 |

## 如何导入微信开发者工具

1. 打开**微信开发者工具**
2. 选择「小程序」→「导入项目」
3. 项目目录选择本目录（`release/wechat/`）
4. 填入你的 AppID（或使用测试号）
5. 点击「确定」即可预览

## 数据更新

当 `data/*.json` 有更新时，运行以下脚本重新生成小程序数据文件：

```bash
# 在项目根目录运行
python data/update_wechat_data.py
```

## 注意事项

- 头像图片使用网络 URL（Wikipedia），需要在小程序后台配置合法域名
  - `upload.wikimedia.org`
  - `placehold.co`（placeholder 回退）
- 数据文件全部内联（`require()`），无需网络请求，可完全离线使用
