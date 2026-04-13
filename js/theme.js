/**
 * theme.js — Dark/light mode, panel interaction wiring, and tradition switching
 */
const ThemeController = (() => {

  function applyTheme(dark) {
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    State.set('darkMode', dark);
  }

  // --- Build filter panel dynamically ---
  function buildFilterPanel(tradition) {
    const filterList = document.getElementById('filterList');
    filterList.innerHTML = '';
    const tags = State.getFilterTags(tradition);
    const tagClassMap = {
      'Basics': 'basics', 'Metaphysics': 'metaphysics', 'Epistemology': 'epistemology',
      'Logic': 'logic', 'Ethics': 'ethics', 'Political': 'political', 'Aesthetics': 'aesthetics',
      'Religion': 'religion', 'Mind': 'mind', 'Language': 'language', 'Science': 'science',
      'Metaphilosophy': 'metaphilosophy',
      'Confucianism': 'confucianism', 'Taoism': 'taoism', 'Mohism': 'mohism',
      'Legalism': 'legalism', 'Neo-Confucianism': 'neo-confucianism', 'Cosmology': 'cosmology'
    };

    for (const tag of tags) {
      const label = document.createElement('label');
      label.className = 'filter-item';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.value = tag;
      cb.className = 'filter-cb';
      cb.checked = true; // all active by default
      const dot = document.createElement('span');
      dot.className = `filter-dot ${tagClassMap[tag] || 'basics'}`;
      const text = document.createTextNode(I18n.t('tag', tag));
      label.appendChild(cb);
      label.appendChild(dot);
      label.appendChild(text);
      filterList.appendChild(label);
    }

    // Re-bind filter events
    bindFilterEvents();
  }

  function bindFilterEvents() {
    document.querySelectorAll('.filter-cb').forEach(cb => {
      // Remove old listeners by replacing node
      const newCb = cb.cloneNode(true);
      cb.parentNode.replaceChild(newCb, cb);
      newCb.addEventListener('change', (e) => {
        if (e.ctrlKey || e.metaKey) {
          // Ctrl/Cmd+click → only this filter, deselect all others
          const tradition = State.get('currentTradition');
          const allTags = State.getFilterTags(tradition);
          State.setAllFilters([newCb.value]);
          document.querySelectorAll('.filter-cb').forEach(c => c.checked = c === newCb);
        } else {
          State.toggleFilter(newCb.value);
        }
        CardRenderer.applyFilters();
        ConnectionRenderer.applyFilteredConnections();
        ConnectionRenderer.rerender();
      });
    });
  }

  function init() {
    // === Theme toggle ===
    const toggleDark = document.getElementById('toggleDark');
    toggleDark.checked = State.get('darkMode');
    toggleDark.addEventListener('change', () => {
      applyTheme(toggleDark.checked);
    });

    // === Portraits toggle ===
    const togglePortraits = document.getElementById('togglePortraits');
    togglePortraits.checked = State.get('showPortraits');
    togglePortraits.addEventListener('change', () => {
      State.set('showPortraits', togglePortraits.checked);
      CardRenderer.updatePortraitVisibility(togglePortraits.checked);
    });

    // === Labels toggle ===
    const toggleLabels = document.getElementById('toggleLabels');
    toggleLabels.checked = State.get('showLabels');
    toggleLabels.addEventListener('change', () => {
      State.set('showLabels', toggleLabels.checked);
      ConnectionRenderer.render();
    });

    // === Eras toggle ===
    const toggleEras = document.getElementById('toggleEras');
    toggleEras.checked = State.get('showEras');
    toggleEras.addEventListener('change', () => {
      State.set('showEras', toggleEras.checked);
      CardRenderer.updateEraVisibility(toggleEras.checked);
    });

    // === Panel menu toggle ===
    const menuBtn = document.getElementById('menuToggle');
    const panel = document.getElementById('sidePanel');
    const canvasWrapper = document.getElementById('canvasWrapper');

    menuBtn.addEventListener('click', () => {
      panel.classList.toggle('collapsed');
      canvasWrapper.classList.toggle('panel-collapsed', panel.classList.contains('collapsed'));
      setTimeout(() => ConnectionRenderer.rerender(), 280);
    });

    // === Panel section accordion ===
    document.querySelectorAll('.panel-section-header').forEach(header => {
      header.addEventListener('click', () => {
        const section = header.closest('.panel-section');
        section.classList.toggle('collapsed');
      });
    });

    // === Select all / None buttons ===
    document.getElementById('btnSelectAll').addEventListener('click', () => {
      const tradition = State.get('currentTradition');
      const allTags = State.getFilterTags(tradition);
      State.setAllFilters(allTags);
      document.querySelectorAll('.filter-cb').forEach(cb => cb.checked = true);
      CardRenderer.applyFilters();
      ConnectionRenderer.applyFilteredConnections();
      ConnectionRenderer.rerender();
    });

    document.getElementById('btnClearAll').addEventListener('click', () => {
      State.clearAllFilters();
      document.querySelectorAll('.filter-cb').forEach(cb => cb.checked = false);
      CardRenderer.applyFilters();
      ConnectionRenderer.applyFilteredConnections();
      ConnectionRenderer.rerender();
    });

    // === Tradition switcher ===
    const switcherBtns = document.querySelectorAll('.switcher-btn');
    const indicator = document.querySelector('.switcher-indicator');
    switcherBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const tradition = btn.dataset.tradition;
        if (tradition === State.get('currentTradition')) return;
        switchView(tradition);
      });
    });

    // === About modal ===
    document.getElementById('btnAbout').addEventListener('click', () => {
      document.getElementById('aboutModal').classList.add('active');
    });
    document.getElementById('modalClose').addEventListener('click', () => {
      document.getElementById('aboutModal').classList.remove('active');
    });
    document.getElementById('aboutModal').addEventListener('click', (e) => {
      if (e.target === document.getElementById('aboutModal')) {
        document.getElementById('aboutModal').classList.remove('active');
      }
    });

    // Note: click-on-canvas-background clearing selection is handled
    // by CanvasManager.onMouseUp with drag detection — do NOT duplicate here.

    // === Keyboard shortcuts ===
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        SelectionManager.clearAll();
        document.getElementById('aboutModal').classList.remove('active');
      }
      if (e.key === '=' || e.key === '+') {
        const r = document.getElementById('canvasWrapper').getBoundingClientRect();
        CanvasManager.animateTo(State.get('scale') + 0.12, State.get('translateX'), State.get('translateY'));
      }
      if (e.key === '-') {
        CanvasManager.animateTo(Math.max(0.2, State.get('scale') - 0.12), State.get('translateX'), State.get('translateY'));
      }
      if (e.key === '0') CanvasManager.resetView();
    });

    // === Build initial filter panel ===
    buildFilterPanel('western');
  }

  // === Switch between Western and Chinese traditions ===
  function switchView(tradition) {
    const switcherBtns = document.querySelectorAll('.switcher-btn');
    const indicator = document.querySelector('.switcher-indicator');
    const transform = document.getElementById('canvasTransform');

    // Update switcher UI
    switcherBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tradition === tradition);
    });
    if (tradition === 'chinese') {
      indicator.classList.add('chinese');
    } else {
      indicator.classList.remove('chinese');
    }

    // Fade out canvas
    transform.classList.add('switching');

    setTimeout(() => {
      // Switch data
      State.switchTradition(tradition);

      // Clear selection highlights
      SelectionManager.clearAll();

      // Rebuild filter panel
      buildFilterPanel(tradition);

      // Re-render cards
      CardRenderer.render();

      // Wait for layout, then render connections
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          ConnectionRenderer.render();

          // Reset canvas position
          setTimeout(() => {
            CanvasManager.resetView();
            // Fade in
            transform.classList.remove('switching');
          }, 100);
        });
      });

      // Rebuild index
      buildIndex();
    }, 220);
  }

  function buildIndex() {
    const philosophers = State.get('philosophers');
    const lang = I18n.getLang();
    const sorted = [...philosophers].sort((a, b) => {
      const nameA = I18n.t('name', a.id);
      const nameB = I18n.t('name', b.id);
      return nameA.localeCompare(nameB, lang === 'zh' ? 'zh-CN' : 'en');
    });
    const indexList = document.getElementById('indexList');
    indexList.innerHTML = '';

    for (const phil of sorted) {
      const item = document.createElement('div');
      item.className = 'index-item';
      item.innerHTML = `
        <span class="index-name">${I18n.t('name', phil.id)}</span>
        <span class="index-years">${I18n.formatYear(phil.born)}</span>
      `;
      item.addEventListener('click', () => {
        CanvasManager.scrollToPhilosopher(phil.id);
        setTimeout(() => SelectionManager.selectPhilosopher(phil.id), 450);
      });
      indexList.appendChild(item);
    }
  }

  return { init, buildIndex, applyTheme, switchView, buildFilterPanel };
})();
