# Philograph — History of Philosophy, Summarized & Visualized

An interactive visualization of the history of philosophy, showing the relationships — agreements and disagreements — between the ideas of 100 major philosophers across Western and Eastern traditions.

![Philograph](https://img.shields.io/badge/Philosophers-100-blue) ![Connections](https://img.shields.io/badge/Connections-333-green) ![Languages](https://img.shields.io/badge/Languages-EN%20%7C%20中文-orange)

## Features

- **Dual Traditions** — Switch between Western (50 philosophers) and Eastern/Chinese (50 philosophers) philosophical traditions
- **Idea Map** — Each philosopher is represented by 3–13 key ideas, displayed as an interactive node graph
- **Connection Lines** — Agreements and disagreements between ideas are visualized as connection lines (333 total)
- **Branch Filtering** — Filter by philosophical branches (Metaphysics, Ethics, Confucianism, Taoism, Buddhism, etc.)
- **Bilingual** — Full support for English and Chinese (中文), auto-detected from browser language
- **Dark Mode** — Built-in dark/light theme toggle
- **Zoom & Pan** — Drag to navigate, scroll to zoom the canvas
- **Index** — Quick jump to any philosopher
- **Responsive** — Works on desktop and tablet screens

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Structure | Semantic HTML5 |
| Styling | CSS3 (custom properties, flexbox, grid) |
| Visualization | [D3.js](https://d3js.org/) v7 |
| Fonts | [Playfair Display](https://fonts.google.com/specimen/Playfair+Display), [Inter](https://fonts.google.com/specimen/Inter), [Noto Serif SC](https://fonts.google.com/noto/specimen/Noto+Serif+SC) |
| i18n | Custom lightweight i18n module |

**No build tools required.** This is a zero-dependency static site — just open `index.html` in a browser.

## Project Structure

```
philograph/
├── index.html              # Main entry point
├── css/
│   └── main.css            # All styles
├── js/
│   ├── app.js              # App initialization & event binding
│   ├── canvas.js           # Zoom/pan canvas manager
│   ├── card-renderer.js    # Philosopher card rendering
│   ├── connection-renderer.js  # Connection line rendering
│   ├── theme.js            # Dark mode, filter panel, index
│   ├── i18n.js             # Internationalization module
│   ├── i18n-data.js        # Translation data (EN/ZH)
│   └── state.js            # Global state management
├── data/
│   ├── philosophers.json          # 50 Western philosophers
│   ├── chinese-philosophers.json  # 50 Chinese philosophers
│   ├── connections.json           # 175 Western connections
│   ├── chinese-connections.json   # 158 Chinese connections
│   └── portraits/                 # Philosopher portrait images
└── README.md
```

## Quick Start

### Local Development

Clone the repo and open in a browser, or use any local HTTP server:

```bash
# Option 1: Just open the file
open index.html

# Option 2: Python HTTP server (recommended for fetch to work)
cd philograph
python -m http.server 8080
# Then visit http://localhost:8080

# Option 3: Node.js
npx serve .
```

### GitHub Pages

1. Go to **Settings → Pages**
2. Set **Source** to "Deploy from a branch"
3. Select **main** branch, **/ (root)** directory
4. Save — your site will be live at `https://<username>.github.io/philograph/`

## Data Format

### Philosopher

```json
{
  "id": "kant",
  "name": "Immanuel Kant",
  "born": 1724,
  "died": 1804,
  "era": "Enlightenment",
  "portrait": "data/portraits/kant.jpg",
  "tags": ["Metaphysics", "Epistemology", "Ethics"],
  "ideas": [
    { "id": "kt1", "text": "Synthetic a priori judgments" },
    { "id": "kt2", "text": "Categorical imperative" }
  ]
}
```

### Connection

```json
{
  "from": "kt1",
  "fromPhil": "kant",
  "to": "sc1",
  "toPhil": "schopenhauer",
  "type": "P",
  "label": "Kant's transcendental idealism directly influenced Schopenhauer"
}
```

- `type: "P"` — Positive (agrees / influenced by)
- `type: "N"` — Negative (disagrees / criticizes)

## Credits

Inspired by [Deniz Cem Önduygu's original Philographics](https://www.denizcemonduygu.com/philo/browse/).

## License

This project is for educational purposes.
