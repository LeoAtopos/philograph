/**
 * app.js — Application entry point
 * Loads JSON data, initializes all modules, renders everything
 */
(async function main() {

  // --- Load data ---
  async function loadJSON(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(`Failed to load ${url}: ${r.status}`);
    return r.json();
  }

  let westernPhil, westernConn, chinesePhil, chineseConn;
  try {
    [westernPhil, westernConn, chinesePhil, chineseConn] = await Promise.all([
      loadJSON('data/philosophers.json'),
      loadJSON('data/connections.json'),
      loadJSON('data/chinese-philosophers.json'),
      loadJSON('data/chinese-connections.json')
    ]);
  } catch (err) {
    console.error('Data load failed:', err);
    document.body.innerHTML = `
      <div style="position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#0f1117;color:#e8eaf0;font-family:sans-serif;text-align:center;padding:40px">
        <div>
          <h2 style="margin-bottom:12px">Failed to load data</h2>
          <p style="color:#9ca3b8">${err.message}</p>
          <p style="color:#5a6282;font-size:12px;margin-top:8px">Please make sure all data files are present in the data/ directory.</p>
        </div>
      </div>
    `;
    return;
  }

  // --- Store all data in state ---
  State.set('westernPhilosophers', westernPhil);
  State.set('westernConnections', westernConn);
  State.set('chinesePhilosophers', chinesePhil);
  State.set('chineseConnections', chineseConn);

  // Default to western
  State.set('philosophers', westernPhil);
  State.set('connections', westernConn);
  State.buildMaps();

  // --- Initialize i18n FIRST (before any rendering) ---
  I18n.init();

  // --- Initialize modules ---
  ConnectionRenderer.init();
  CanvasManager.init();

  // --- Render cards ---
  CardRenderer.render();

  // --- Initial canvas position ---
  await new Promise(r => requestAnimationFrame(r));
  await new Promise(r => requestAnimationFrame(r));

  const wrapper = document.getElementById('canvasWrapper');
  const wrapperRect = wrapper.getBoundingClientRect();
  State.setTransform(0.72, 40, 90);
  CanvasManager.applyTransform();

  // --- Render connections (after cards have positions) ---
  await new Promise(r => setTimeout(r, 120));
  ConnectionRenderer.render();

  setTimeout(() => ConnectionRenderer.rerender(), 300);

  // --- Init theme & UI controllers ---
  ThemeController.init();
  ThemeController.buildIndex();

  // --- Language switcher ---
  const langBtns = document.querySelectorAll('.lang-btn');
  langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;
      if (lang === I18n.getLang()) return;
      langBtns.forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
      I18n.setLang(lang);
    });
  });

  // --- Re-render connections on window resize ---
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => ConnectionRenderer.rerender(), 150);
  });

  // --- Startup animation: gentle fade-in ---
  const loadingScreen = document.getElementById('loadingScreen');
  if (loadingScreen) {
    loadingScreen.classList.add('fade-out');
    setTimeout(() => { loadingScreen.style.display = 'none'; }, 700);
  }

})();
