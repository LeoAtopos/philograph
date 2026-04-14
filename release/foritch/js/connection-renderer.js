/**
 * connection-renderer.js — SVG Bezier curve connections between idea items
 */
const ConnectionRenderer = (() => {
  let svgGroup, svgEl;
  let currentTx = 0, currentTy = 0, currentScale = 1;

  function init() {
    svgEl = document.getElementById('connectionsSvg');
    svgGroup = document.getElementById('connectionsGroup');
  }

  // Get the center of the idea-dot (bullet) element, adjusted for SVG coord space
  function getIdeaAnchor(ideaId) {
    const li = document.getElementById(`idea-${ideaId}`);
    if (!li) return null;
    const dot = li.querySelector('.idea-dot');
    const target = dot || li;
    const rect = target.getBoundingClientRect();
    const wrapperRect = document.getElementById('canvasWrapper').getBoundingClientRect();
    return {
      x: rect.left - wrapperRect.left + rect.width * 0.5,
      y: rect.top  - wrapperRect.top  + rect.height * 0.5
    };
  }

  // Draw a semi-circular arc between two anchors
  // P (agree/green) arches upward, N (disagree/red) arches downward
  function makePath(x1, y1, x2, y2, type) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const dist = Math.hypot(dx, dy);

    if (dist < 10) return '';

    // Midpoint
    const mx = (x1 + x2) / 2;
    const my = (y1 + y2) / 2;

    // Perpendicular unit vector (rotate 90°)
    const nx = -dy / dist;
    const ny =  dx / dist;

    // Semi-circle bulge
    const bulge = dist * 0.55;

    // P (agree) → arch upward (negative screen-Y), N (disagree) → arch downward (positive screen-Y)
    // For mostly-vertical connections, fall back to left/right to avoid card overlap
    let archDir;
    if (Math.abs(dx) > Math.abs(dy)) {
      // Horizontal: P up (-1 in screen Y), N down (+1)
      archDir = type === 'P' ? -1 : 1;
    } else {
      // Vertical: P left, N right
      archDir = type === 'P' ? -1 : 1;
    }

    const cx = mx + nx * bulge * archDir;
    const cy = my + ny * bulge * archDir;

    return `M ${x1.toFixed(1)} ${y1.toFixed(1)} Q ${cx.toFixed(1)} ${cy.toFixed(1)}, ${x2.toFixed(1)} ${y2.toFixed(1)}`;
  }

  function render() {
    if (!svgGroup) return;
    svgGroup.innerHTML = '';

    const connections = State.get('connections');
    const showLabels = State.get('showLabels');

    for (const conn of connections) {
      const a1 = getIdeaAnchor(conn.from);
      const a2 = getIdeaAnchor(conn.to);
      if (!a1 || !a2) continue;

      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.dataset.connFrom = conn.from;
      g.dataset.connTo = conn.to;
      g.dataset.connType = conn.type;
      g.dataset.connFromPhil = conn.fromPhil;
      g.dataset.connToPhil = conn.toPhil;
      g.dataset.connLabel = conn.label || '';

      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', makePath(a1.x, a1.y, a2.x, a2.y, conn.type));
      path.setAttribute('class', `connection-path ${conn.type === 'P' ? 'agree' : 'disagree'}`);
      path.id = `conn-${conn.from}-${conn.to}`;

      // Hover tooltip
      path.addEventListener('mouseenter', (e) => showTooltip(e, conn));
      path.addEventListener('mousemove', (e) => moveTooltip(e));
      path.addEventListener('mouseleave', hideTooltip);
      path.addEventListener('click', (e) => {
        e.stopPropagation();
        SelectionManager.selectConnection(conn);
      });

      g.appendChild(path);

      // Optional label
      if (showLabels && conn.label) {
        const mx = (a1.x + a2.x) / 2;
        const my = (a1.y + a2.y) / 2;
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', mx);
        text.setAttribute('y', my - 6);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('class', 'conn-label');
        text.setAttribute('fill', conn.type === 'P' ? 'var(--color-agree)' : 'var(--color-disagree)');
        text.setAttribute('font-size', '9');
        text.setAttribute('font-family', 'Inter, Noto Serif SC, sans-serif');
        text.setAttribute('opacity', '0.7');
        const connKey = `${conn.from}-${conn.to}`;
        const label = I18n.t('conn', connKey);
        text.textContent = label !== connKey && label.length > 40 ? label.slice(0, 38) + '…' : (label !== connKey ? label : conn.label.length > 40 ? conn.label.slice(0, 38) + '…' : conn.label);
        g.appendChild(text);
      }

      svgGroup.appendChild(g);
    }
  }

  // Re-render paths (when canvas transforms change, we recalculate anchors)
  function rerender() {
    const connections = State.get('connections');
    const showLabels = State.get('showLabels');
    for (const conn of connections) {
      const g = svgGroup.querySelector(`[data-conn-from="${conn.from}"][data-conn-to="${conn.to}"]`);
      if (!g) continue;
      // Skip filtered-out connections (parent card is hidden, getBoundingClientRect would be 0)
      if (g.classList.contains('filtered-out')) continue;
      const a1 = getIdeaAnchor(conn.from);
      const a2 = getIdeaAnchor(conn.to);
      if (!a1 || !a2) continue;
      const path = g.querySelector('path');
      if (path) path.setAttribute('d', makePath(a1.x, a1.y, a2.x, a2.y, conn.type));
      if (showLabels) {
        const text = g.querySelector('text');
        if (text) {
          text.setAttribute('x', (a1.x + a2.x) / 2);
          text.setAttribute('y', (a1.y + a2.y) / 2 - 6);
        }
      }
    }
  }

  // The SVG sits fixed over the canvas-wrapper at top/left 0; no viewBox transform needed
  // (paths use wrapper-local screen coords)
  function updateSVGTransform(tx, ty, scale) {
    currentTx = tx; currentTy = ty; currentScale = scale;
    // Paths use screen coordinates that auto-update because getBoundingClientRect moves
    requestAnimationFrame(rerender);
  }

  function applySelectionHighlight(selectedIdeaId, selectedPhilId) {
    const paths = svgGroup.querySelectorAll('.connection-path');
    paths.forEach(p => {
      p.classList.remove('highlighted', 'dimmed');
    });

    if (!selectedIdeaId && !selectedPhilId) return;

    const connsByIdea = State.get('connectionsByIdea');
    let relevantConnIds = new Set();

    if (selectedIdeaId) {
      const myConns = connsByIdea[selectedIdeaId] || [];
      myConns.forEach(c => relevantConnIds.add(`${c.from}-${c.to}`));
    } else if (selectedPhilId) {
      // Highlight all connections for this philosopher
      const phil = State.get('philosopherMap')[selectedPhilId];
      if (phil) {
        for (const idea of phil.ideas) {
          const myConns = connsByIdea[idea.id] || [];
          myConns.forEach(c => relevantConnIds.add(`${c.from}-${c.to}`));
        }
      }
    }

    paths.forEach(p => {
      const connId = p.id.replace('conn-', '');
      if (relevantConnIds.has(connId)) {
        p.classList.add('highlighted');
      } else {
        p.classList.add('dimmed');
      }
    });
  }

  function clearHighlight() {
    const paths = svgGroup ? svgGroup.querySelectorAll('.connection-path') : [];
    paths.forEach(p => p.classList.remove('highlighted', 'dimmed'));
  }

  function applyFilteredConnections() {
    const activeFilters = State.get('activeFilters');
    const connections = State.get('connections');
    const ideaMap = State.get('ideaMap');

    for (const conn of connections) {
      const g = svgGroup.querySelector(`[data-conn-from="${conn.from}"][data-conn-to="${conn.to}"]`);
      if (!g) continue;
      // Show connection if at least one end belongs to a visible card
      const fromInfo = ideaMap[conn.from];
      const toInfo = ideaMap[conn.to];
      if (!fromInfo || !toInfo) { g.classList.add('filtered-out'); continue; }

      // Check if either end's philosopher card is filtered-out
      const fromCard = document.getElementById(`card-${fromInfo.phil.id}`);
      const toCard = document.getElementById(`card-${toInfo.phil.id}`);
      const fromHidden = fromCard && fromCard.classList.contains('filtered-out');
      const toHidden = toCard && toCard.classList.contains('filtered-out');
      if (fromHidden && toHidden) { g.classList.add('filtered-out'); continue; }
      if (fromHidden || toHidden) { g.classList.add('filtered-out'); continue; }

      // Both cards visible — check tag-based filter
      const fromTags = new Set([...fromInfo.phil.tags, ...fromInfo.idea.tags]);
      const toTags   = new Set([...toInfo.phil.tags,   ...toInfo.idea.tags]);
      const allTags  = new Set([...fromTags, ...toTags]);

      const visible = activeFilters.size === 0 || [...allTags].some(t => activeFilters.has(t));
      g.classList.toggle('filtered-out', !visible);
    }
  }

  // Tooltip
  function showTooltip(e, conn) {
    const tooltip = document.getElementById('connectionTooltip');
    const typeStr = conn.type === 'P' ? I18n.t('ui.tooltipAgree') : I18n.t('ui.tooltipDisagree');
    const fromInfo = State.get('ideaMap')[conn.from];
    const toInfo   = State.get('ideaMap')[conn.to];
    const fromName = fromInfo ? I18n.t('name', fromInfo.phil.id) : '';
    const toName   = toInfo   ? I18n.t('name', toInfo.phil.id)   : '';

    // Connection label lookup: use from-to key
    const connKey = `${conn.from}-${conn.to}`;
    const connLabel = I18n.t('conn', connKey);

    tooltip.innerHTML = `
      <div style="font-weight:600;color:${conn.type==='P'?'var(--color-agree)':'var(--color-disagree)'};margin-bottom:4px">${typeStr}</div>
      <div style="margin-bottom:2px"><strong>${fromName}</strong> → <strong>${toName}</strong></div>
      ${connLabel !== connKey ? `<div style="color:var(--text-muted);font-size:10.5px">${connLabel}</div>` : ''}
    `;
    moveTooltip(e);
    tooltip.classList.add('visible');
  }

  function moveTooltip(e) {
    const tooltip = document.getElementById('connectionTooltip');
    const tx = e.clientX + 14;
    const ty = e.clientY - 10;
    tooltip.style.left = Math.min(tx, window.innerWidth - 280) + 'px';
    tooltip.style.top = ty + 'px';
  }

  function hideTooltip() {
    document.getElementById('connectionTooltip').classList.remove('visible');
  }

  return { init, render, rerender, updateSVGTransform, applySelectionHighlight, clearHighlight, applyFilteredConnections };
})();
