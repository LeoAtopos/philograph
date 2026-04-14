/**
 * canvas-manager.js — Drag/pan and zoom behavior for the infinite canvas
 */
const CanvasManager = (() => {
  let wrapper, transform;
  let isDragging = false;
  let lastX = 0, lastY = 0;
  let dragStartX = 0, dragStartY = 0;
  let hasMoved = false;

  // Touch pinch state
  let lastPinchDist = 0;

  const MIN_SCALE = 0.2;
  const MAX_SCALE = 2.5;
  const ZOOM_STEP = 0.12;

  // Repaint timer — forces browser to re-rasterize text after zoom
  let repaintTimer = null;
  function scheduleRepaint() {
    if (repaintTimer) clearTimeout(repaintTimer);
    repaintTimer = setTimeout(() => {
      repaintTimer = null;
      // Force Chrome to discard the cached raster tile and re-render
      const t = document.getElementById('canvasTransform');
      const v = t.style.transform;
      t.style.transform = 'translateZ(0)';
      void t.offsetHeight;           // force reflow
      t.style.transform = v;
    }, 80);
  }

  function applyTransform() {
    const { scale, translateX, translateY } = State.getState();
    transform.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    document.getElementById('zoomLevel').textContent = Math.round(scale * 100) + '%';
    // Also update SVG viewBox so paths stay aligned
    ConnectionRenderer.updateSVGTransform(translateX, translateY, scale);
  }

  function clampScale(s) {
    return Math.max(MIN_SCALE, Math.min(MAX_SCALE, s));
  }

  // Zoom toward a point (cx, cy) in screen coordinates
  function zoomToward(cx, cy, newScale) {
    const st = State.getState();
    const oldScale = st.scale;
    newScale = clampScale(newScale);
    if (newScale === oldScale) return;

    // Adjust translate so the canvas point under (cx, cy) stays fixed
    const wrapperRect = wrapper.getBoundingClientRect();
    const px = cx - wrapperRect.left;
    const py = cy - wrapperRect.top;
    const ratio = newScale / oldScale;
    const newTx = px - ratio * (px - st.translateX);
    const newTy = py - ratio * (py - st.translateY);
    State.setTransform(newScale, newTx, newTy);
    applyTransform();
  }

  function onMouseDown(e) {
    if (e.button !== 0) return;
    // Allow clicks on cards & buttons to propagate normally
    if (e.target.closest('.philosopher-card') || e.target.closest('.connection-path')) return;
    isDragging = true;
    hasMoved = false;
    lastX = e.clientX;
    lastY = e.clientY;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    wrapper.classList.add('dragging');
    e.preventDefault();
  }

  function onMouseMove(e) {
    if (!isDragging) return;
    const dx = e.clientX - lastX;
    const dy = e.clientY - lastY;
    lastX = e.clientX;
    lastY = e.clientY;
    // Only consider it a real drag if moved more than 5px
    if (!hasMoved && Math.hypot(e.clientX - dragStartX, e.clientY - dragStartY) > 5) {
      hasMoved = true;
    }
    if (hasMoved) {
      const st = State.getState();
      State.setTransform(st.scale, st.translateX + dx, st.translateY + dy);
      applyTransform();
    }
  }

  function onMouseUp(e) {
    if (!isDragging) return;
    isDragging = false;
    wrapper.classList.remove('dragging');
    // Only clear selection on a real click (no significant drag movement)
    if (!hasMoved && SelectionManager) {
      SelectionManager.clearAll();
    }
  }

  function onWheel(e) {
    e.preventDefault();
    const st = State.getState();
    const delta = e.deltaY < 0 ? ZOOM_STEP : -ZOOM_STEP;
    zoomToward(e.clientX, e.clientY, st.scale + delta);
    scheduleRepaint();
  }

  // Touch events
  function getTouchDist(e) {
    const dx = e.touches[0].clientX - e.touches[1].clientX;
    const dy = e.touches[0].clientY - e.touches[1].clientY;
    return Math.hypot(dx, dy);
  }

  function onTouchStart(e) {
    if (e.touches.length === 1) {
      isDragging = true;
      lastX = e.touches[0].clientX;
      lastY = e.touches[0].clientY;
    } else if (e.touches.length === 2) {
      isDragging = false;
      lastPinchDist = getTouchDist(e);
    }
  }

  function onTouchMove(e) {
    if (e.touches.length === 1 && isDragging) {
      const dx = e.touches[0].clientX - lastX;
      const dy = e.touches[0].clientY - lastY;
      lastX = e.touches[0].clientX;
      lastY = e.touches[0].clientY;
      const st = State.getState();
      State.setTransform(st.scale, st.translateX + dx, st.translateY + dy);
      applyTransform();
      e.preventDefault();
    } else if (e.touches.length === 2) {
      e.preventDefault();
      const dist = getTouchDist(e);
      const st = State.getState();
      const ratio = dist / lastPinchDist;
      const midX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
      const midY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
      zoomToward(midX, midY, st.scale * ratio);
      lastPinchDist = dist;
    }
  }

  function onTouchEnd() { isDragging = false; }

  function init() {
    wrapper = document.getElementById('canvasWrapper');
    transform = document.getElementById('canvasTransform');

    wrapper.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    wrapper.addEventListener('wheel', onWheel, { passive: false });
    wrapper.addEventListener('touchstart', onTouchStart, { passive: false });
    wrapper.addEventListener('touchmove', onTouchMove, { passive: false });
    wrapper.addEventListener('touchend', onTouchEnd);

    // Zoom buttons
    document.getElementById('zoomIn').addEventListener('click', () => {
      const r = wrapper.getBoundingClientRect();
      zoomToward(r.left + r.width / 2, r.top + r.height / 2, State.get('scale') + ZOOM_STEP);
      scheduleRepaint();
    });
    document.getElementById('zoomOut').addEventListener('click', () => {
      const r = wrapper.getBoundingClientRect();
      zoomToward(r.left + r.width / 2, r.top + r.height / 2, State.get('scale') - ZOOM_STEP);
      scheduleRepaint();
    });
    document.getElementById('zoomReset').addEventListener('click', resetView);
  }

  function resetView() {
    // Center the canvas content
    const wrapperRect = wrapper.getBoundingClientRect();
    const defaultScale = 0.75;
    const container = document.getElementById('philosophersContainer');
    if (!container) { State.setTransform(defaultScale, 60, 100); applyTransform(); return; }
    const containerW = container.scrollWidth * defaultScale;
    const containerH = container.scrollHeight * defaultScale;
    const tx = (wrapperRect.width - containerW) > 0 ? (wrapperRect.width - containerW) / 2 : 40;
    const ty = (wrapperRect.height - containerH) > 0 ? (wrapperRect.height - containerH) / 2 : 60;
    animateTo(defaultScale, tx, ty);
  }

  function animateTo(targetScale, targetTx, targetTy) {
    const start = { scale: State.get('scale'), tx: State.get('translateX'), ty: State.get('translateY') };
    const duration = 400;
    const startTime = performance.now();

    function easeInOut(t) { return t < 0.5 ? 2*t*t : -1+(4-2*t)*t; }

    function step(now) {
      const t = Math.min((now - startTime) / duration, 1);
      const e = easeInOut(t);
      const s = start.scale + (targetScale - start.scale) * e;
      const tx = start.tx + (targetTx - start.tx) * e;
      const ty = start.ty + (targetTy - start.ty) * e;
      State.setTransform(s, tx, ty);
      applyTransform();
      if (t < 1) requestAnimationFrame(step);
      else scheduleRepaint();
    }
    requestAnimationFrame(step);
  }

  // Scroll/jump a philosopher card into center view
  function scrollToPhilosopher(philId) {
    const card = document.getElementById(`card-${philId}`);
    if (!card) return;
    const wrapper = document.getElementById('canvasWrapper');
    const wrapperRect = wrapper.getBoundingClientRect();

    // Get card position in canvas space
    const containerEl = document.getElementById('philosophersContainer');
    const containerRect = containerEl.getBoundingClientRect();
    const cardRect = card.getBoundingClientRect();

    // Current transform
    const st = State.getState();

    // Card center in screen coordinates
    const cardCx = cardRect.left + cardRect.width / 2;
    const cardCy = cardRect.top + cardRect.height / 2;

    // Target: bring card center to wrapper center
    const targetTx = st.translateX + (wrapperRect.left + wrapperRect.width / 2) - cardCx;
    const targetTy = st.translateY + (wrapperRect.top + wrapperRect.height / 2) - cardCy;

    animateTo(st.scale < 0.6 ? 0.75 : st.scale, targetTx, targetTy);
  }

  return { init, applyTransform, resetView, scrollToPhilosopher, animateTo };
})();
