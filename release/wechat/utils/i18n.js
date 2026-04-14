// utils/i18n.js — 微信小程序多语言模块
// 依赖 i18n-data.js 中的 I18N_DATA

const I18N_DATA = require('./i18n-data.js');

let _lang = 'zh';

function init(lang) {
  _lang = lang || 'zh';
}

function getLang() { return _lang; }

function setLang(lang) {
  _lang = lang;
  wx.setStorageSync('philograph-lang', lang);
  const app = getApp();
  if (app) app.globalData.lang = lang;
}

/**
 * 翻译函数
 * t('ui.filters')          -> UI 文本
 * t('era', 'Ancient')      -> 时代名
 * t('tag', 'Metaphysics')  -> 标签名
 * t('name', 'socrates')    -> 哲学家名
 * t('idea', 'sc1')         -> 思想文本
 * t('conn', 'pl1-sc1')     -> 连线说明
 */
function t(category, key) {
  if (key !== undefined) {
    const entry = I18N_DATA[category] && I18N_DATA[category][key];
    if (!entry) return key;
    if (typeof entry === 'string') return entry;
    return entry[_lang] || entry.en || key;
  }
  const uiKey = category.startsWith('ui.') ? category.slice(3) : category;
  const entry = I18N_DATA.ui[uiKey];
  if (!entry) return category;
  return entry[_lang] || entry.en || category;
}

function formatYear(year) {
  if (!year && year !== 0) return '';
  if (year < 0) {
    return _lang === 'zh'
      ? `${Math.abs(year)}${t('ui.bc')}`
      : `${Math.abs(year)} BC`;
  }
  return year > 0 && _lang === 'zh'
    ? `${year}${t('ui.ad')}`
    : (year > 0 ? `${year} AD` : `${year}`);
}

function formatYears(born, died) {
  if (!born && !died) return '';
  if (!died) return formatYear(born) + ' –';
  return `${formatYear(born)} – ${formatYear(died)}`;
}

module.exports = { init, getLang, setLang, t, formatYear, formatYears };
