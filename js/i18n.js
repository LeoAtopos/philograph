/**
 * i18n.js — Internationalization module
 * Provides t(), init(), setLang(), apply() functions.
 * Depends on I18N_DATA from i18n-data.js and State from state.js.
 */
const I18n = (() => {
  let _lang = 'en'; // 'en' | 'zh'

  /**
   * Initialize language from localStorage or browser default.
   * Call once at app startup.
   */
  function init() {
    const saved = localStorage.getItem('philograph-lang');
    if (saved === 'zh' || saved === 'en') {
      _lang = saved;
    } else {
      // Auto-detect from browser
      const nav = navigator.language || navigator.userLanguage || '';
      _lang = nav.startsWith('zh') ? 'zh' : 'en';
    }
    State.set('currentLang', _lang);
    apply();
  }

  function getLang() {
    return _lang;
  }

  /**
   * Translate by key.
   * Supports:
   *   I18n.t('ui.siteTitleMain')           -> UI text
   *   I18n.t('era', 'Ancient')             -> era name
   *   I18n.t('tag', 'Metaphysics')         -> tag label
   *   I18n.t('name', 'socrates')           -> philosopher name (returns string)
   *   I18n.t('idea', 'sc1')                -> idea text (returns string)
   *   I18n.t('conn', 'pl1-sc1')            -> connection label (returns string)
   */
  function t(category, key) {
    if (key !== undefined) {
      const entry = I18N_DATA[category] && I18N_DATA[category][key];
      if (!entry) return key;
      if (typeof entry === 'string') return entry; // name, conn entries
      return entry[_lang] || entry.en || key;
    }
    // Single-key lookup: support both "ui.siteTitleMain" and "siteTitleMain"
    const uiKey = category.startsWith('ui.') ? category.slice(3) : category;
    const entry = I18N_DATA.ui[uiKey];
    if (!entry) return category;
    return entry[_lang] || entry.en || category;
  }

  /**
   * Set language and re-render everything.
   */
  function setLang(lang) {
    if (lang === _lang) return;
    _lang = lang;
    State.set('currentLang', _lang);
    localStorage.setItem('philograph-lang', _lang);
    apply();
  }

  /**
   * Apply translations to the entire UI.
   * 1. Update HTML elements with [data-i18n] attributes
   * 2. Update [data-i18n-html] attributes (innerHTML)
   * 3. Re-render dynamic content (cards, connections, filter panel, index)
   */
  function apply() {
    // 1. Static text nodes
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      el.textContent = t(key);
    });

    // 2. InnerHTML elements (e.g., about modal list items)
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const key = el.getAttribute('data-i18n-html');
      el.innerHTML = t(key);
    });

    // 3. Page title
    const titleKey = document.querySelector('title');
    if (titleKey) document.title = t('ui.pageTitle');

    // 4. Re-render dynamic modules
    CardRenderer.render();
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        ConnectionRenderer.render();
      });
    });

    // Rebuild filter panel for current tradition
    const tradition = State.get('currentTradition');
    ThemeController.buildFilterPanel(tradition);

    // Rebuild index
    ThemeController.buildIndex();

    // Update lang attribute on <html>
    document.documentElement.lang = _lang === 'zh' ? 'zh-CN' : 'en';
  }

  /**
   * Format year with BC/AD suffix in current language.
   * @param {number} year
   * @returns {string}
   */
  function formatYear(year) {
    if (year < 0) {
      return _lang === 'zh'
        ? `${Math.abs(year)} BC`.replace('BC', t('ui.bc'))
        : `${Math.abs(year)} BC`;
    }
    return year > 0 && _lang === 'zh'
      ? `${year} AD`.replace('AD', t('ui.ad'))
      : (year > 0 ? `${year} AD` : `${year}`);
  }

  /**
   * Format year range "born – died"
   */
  function formatYears(born, died) {
    if (!born && !died) return '';
    if (!died) return formatYear(born) + ' –';
    return `${formatYear(born)} – ${formatYear(died)}`;
  }

  return { init, getLang, setLang, t, apply, formatYear, formatYears };
})();
