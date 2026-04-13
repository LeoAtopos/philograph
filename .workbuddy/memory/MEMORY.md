# Philograph 项目 - 长期记忆

## 项目概述
- 哲学思想关系图谱可视化 web 应用
- 位于 `c:\Users\leoni\Documents\GitHub\philograph\`
- 主要数据文件在 `data/` 目录

## 数据文件结构
- `philosophers.json` - 西方哲学家 (50位)
- `chinese-philosophers.json` - 中国哲学家 (50位)  
- `connections.json` - 西方思想连线 (175条)
- `chinese-connections.json` - 中国思想连线 (158条)

## 数据规则
- 思想条目数量: 3-10条/哲学家 (孔子13条, 康德13条, 亚里士多德13条等核心人物可超10条)
- 连线结构: `{"from": "idea_id", "fromPhil": "phil_id", "to": "idea_id", "toPhil": "phil_id", "type": "P/N", "label": "description"}`
- 只通过 Python 脚本修改 JSON 数据
- 中文哲学家连线不能引用西方哲学家 (反之亦然)

## 技术栈
- 纯前端: HTML + CSS + JavaScript (无框架)
- D3.js 用于图谱可视化
