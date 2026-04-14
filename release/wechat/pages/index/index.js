// pages/index/index.js
// Native WXML list view — no Canvas, best performance on real devices
const I18n = require('../../utils/i18n.js');
const westernPhil = require('../../data/philosophers.js');
const westernConn = require('../../data/connections.js');
const chinesePhil = require('../../data/chinese-philosophers.js');
const chineseConn = require('../../data/chinese-connections.js');

const TAG_COLORS = {
  'Metaphysics': '#7c8cff', 'Epistemology': '#60a5fa', 'Logic': '#fbbf24',
  'Ethics': '#4ade80', 'Political': '#f87171', 'Aesthetics': '#c4b5fd',
  'Religion': '#fb923c', 'Mind': '#e879f9', 'Language': '#2dd4bf',
  'Science': '#f8c864', 'Metaphilosophy': '#9ca3b8', 'Basics': '#5a6282',
  'Confucianism': '#c8a96e', 'Taoism': '#6ec8a9', 'Mohism': '#64b4c8',
  'Legalism': '#c86e6e', 'Neo-Confucianism': '#c8a96e',
  'Cosmology': '#7c8cff', 'Buddhism': '#ffc864',
  'Education': '#60a5fa', 'History': '#fb923c',
};

const FILTER_TAGS = {
  western: ['Basics','Metaphysics','Epistemology','Logic','Ethics','Political','Aesthetics','Religion','Mind','Language','Science','Metaphilosophy'],
  chinese: ['Confucianism','Taoism','Mohism','Legalism','Neo-Confucianism','Buddhism','Ethics','Political','Metaphysics','Epistemology','Aesthetics','Mind','Language','Education','History']
};

const ERA_ORDER = {
  western: ['Ancient','Medieval','Early Modern','Enlightenment','German Idealism','19th Century','Analytic Origins','Pragmatism','Analytic','Continental','Post-Structuralism','20th Century','Contemporary'],
  chinese: ['Pre-Qin','Han','Wei-Jin','Sui-Tang','Tang-Song','Ming-Qing','Modern']
};

Page({
  data: {
    lang: 'zh',
    tradition: 'western',
    i18n: {},
    filterTags: [],
    activeFilterCount: 0,
    totalFilterCount: 0,
    indexList: [],
    showFilter: false,
    showIndex: false,
    searchText: '',
    visibleCount: 0,
    totalCount: 0,
    // --- list data ---
    eras: [],          // [{label, sections}]
    scrollToId: '',    // for scroll-into-view
  },

  // Internal state
  _allPhilosophers: [],
  _allConnections: [],
  _connectionsByIdea: {},
  _activeFilters: new Set(),
  _searchText: '',

  onLoad() {
    const app = getApp();
    const lang = app.globalData.lang || 'zh';
    I18n.init(lang);
    this._loadTradition('western');
    this.setData({ lang });
    this._updateI18n();
  },

  // ===== Data loading =====
  _loadTradition(tradition) {
    var phils = tradition === 'chinese' ? chinesePhil : westernPhil;
    var conns = tradition === 'chinese' ? chineseConn : westernConn;

    this._allPhilosophers = phils;
    this._allConnections = conns;
    this._activeFilters = new Set(FILTER_TAGS[tradition]);
    this._searchText = '';

    this._connectionsByIdea = {};
    for (var i = 0; i < conns.length; i++) {
      var conn = conns[i];
      if (!this._connectionsByIdea[conn.from]) this._connectionsByIdea[conn.from] = [];
      if (!this._connectionsByIdea[conn.to])   this._connectionsByIdea[conn.to]   = [];
      this._connectionsByIdea[conn.from].push(conn);
      this._connectionsByIdea[conn.to].push(conn);
    }

    this.setData({
      tradition: tradition,
      searchText: '',
      showFilter: false,
      showIndex: false,
    });
    this._rebuildView();
  },

  // ===== Build list data =====
  _buildListData() {
    var phils = this._allPhilosophers;
    var eraOrder = ERA_ORDER[this.data.tradition];
    var activeFilters = this._activeFilters;
    var searchText = this._searchText.toLowerCase();
    var lang = I18n.getLang();

    // Group by era
    var groups = {};
    for (var i = 0; i < phils.length; i++) {
      var phil = phils[i];
      if (!groups[phil.era]) groups[phil.era] = [];
      groups[phil.era].push(phil);
    }

    var sortedEras = [];
    for (var j = 0; j < eraOrder.length; j++) {
      if (groups[eraOrder[j]]) sortedEras.push(eraOrder[j]);
    }

    var eras = [];
    var visibleCount = 0;

    for (var e = 0; e < sortedEras.length; e++) {
      var era = sortedEras[e];
      var eraPhils = groups[era];
      eraPhils.sort(function(a, b) { return (a.born || 0) - (b.born || 0); });

      var cards = [];
      for (var p = 0; p < eraPhils.length; p++) {
        var phil = eraPhils[p];
        var displayName = I18n.t('name', phil.id);
        var years = I18n.formatYears(phil.born, phil.died);

        // Search
        var searchMatch = true;
        if (searchText) {
          var matchName = displayName.toLowerCase().indexOf(searchText) >= 0 ||
            phil.name.toLowerCase().indexOf(searchText) >= 0;
          var matchIdea = false;
          for (var ii = 0; ii < phil.ideas.length; ii++) {
            if (I18n.t('idea', phil.ideas[ii].id).toLowerCase().indexOf(searchText) >= 0) {
              matchIdea = true;
              break;
            }
          }
          searchMatch = matchName || matchIdea;
        }

        // Filter
        var allTags = {};
        for (var ti = 0; ti < (phil.tags || []).length; ti++) {
          allTags[phil.tags[ti]] = true;
        }
        for (var ii2 = 0; ii2 < phil.ideas.length; ii2++) {
          var ideaTags = phil.ideas[ii2].tags || [];
          for (var ti2 = 0; ti2 < ideaTags.length; ti2++) {
            allTags[ideaTags[ti2]] = true;
          }
        }
        var tagMatch = activeFilters.size === 0;
        if (!tagMatch) {
          var tagKeys = Object.keys(allTags);
          for (var tk = 0; tk < tagKeys.length; tk++) {
            if (activeFilters.has(tagKeys[tk])) {
              tagMatch = true;
              break;
            }
          }
        }

        var filtered = !searchMatch || !tagMatch;
        if (!filtered) visibleCount++;

        // Build tagBadges
        var tagBadges = [];
        var tags = phil.tags || [];
        for (var tb = 0; tb < Math.min(tags.length, 3); tb++) {
          var tag = tags[tb];
          tagBadges.push({
            label: I18n.t('tag', tag),
            color: TAG_COLORS[tag] || '#5a6282'
          });
        }

        // Build idea list
        var ideaList = [];
        for (var il = 0; il < phil.ideas.length; il++) {
          var idea = phil.ideas[il];
          var primaryTag = (idea.tags && idea.tags[0]) || 'Basics';
          var conns = this._connectionsByIdea[idea.id] || [];
          var agreeCount = 0;
          var disagreeCount = 0;
          for (var ci = 0; ci < conns.length; ci++) {
            if (conns[ci].type === 'P') agreeCount++;
            else disagreeCount++;
          }

          ideaList.push({
            id: idea.id,
            text: I18n.t('idea', idea.id),
            dotColor: TAG_COLORS[primaryTag] || '#5a6282',
            agreeCount: agreeCount,
            disagreeCount: disagreeCount,
          });
        }

        // Initials for avatar placeholder
        var initials = phil.name.slice(0, 2).toUpperCase();

        cards.push({
          id: phil.id,
          displayName: displayName,
          years: years,
          era: era,
          eraLabel: I18n.t('era', era),
          portrait: phil.portrait || '',
          initials: initials,
          tagBadges: tagBadges,
          ideaList: ideaList,
          filtered: filtered,
        });
      }

      eras.push({
        id: 'era-' + era,
        label: I18n.t('era', era),
        cards: cards,
      });
    }

    this.setData({
      eras: eras,
      visibleCount: visibleCount,
      totalCount: phils.length,
    });
  },

  // ===== View rebuild =====
  _rebuildView() {
    var tradition = this.data.tradition;
    var lang = I18n.getLang();
    var filterTags = FILTER_TAGS[tradition];
    var activeFilters = this._activeFilters;

    this._buildListData();

    var filterTagList = [];
    for (var i = 0; i < filterTags.length; i++) {
      var tag = filterTags[i];
      filterTagList.push({
        value: tag,
        label: I18n.t('tag', tag),
        cls: TAG_COLORS[tag] || '#5a6282',
        active: activeFilters.has(tag),
      });
    }

    var indexList = [];
    for (var j = 0; j < this._allPhilosophers.length; j++) {
      var p = this._allPhilosophers[j];
      indexList.push({
        id: p.id,
        name: I18n.t('name', p.id),
        year: p.born ? I18n.formatYear(p.born) : '',
      });
    }
    indexList.sort(function(a, b) {
      return a.name.localeCompare(b.name, lang === 'zh' ? 'zh-CN' : 'en');
    });

    this.setData({
      filterTags: filterTagList,
      activeFilterCount: activeFilters.size,
      totalFilterCount: filterTags.length,
      indexList: indexList,
    });
  },

  _updateI18n() {
    this.setData({
      i18n: {
        siteTitleMain: I18n.t('ui.siteTitleMain'),
        siteTitleSub: I18n.t('ui.siteTitleSub'),
        western: I18n.t('ui.western'),
        eastern: I18n.t('ui.eastern'),
        filters: I18n.t('ui.filters'),
        index: I18n.t('ui.index'),
        selectAll: I18n.t('ui.selectAll'),
        clearAll: I18n.t('ui.clearAll'),
        legendAgree: I18n.t('ui.legendAgree'),
        legendDisagree: I18n.t('ui.legendDisagree'),
        search: I18n.getLang() === 'zh' ? '搜索哲学家或思想...' : 'Search philosophers or ideas...',
        philosophers: I18n.getLang() === 'zh' ? '位哲学家可见' : 'philosophers visible',
      }
    });
  },

  // ===== Event handlers =====
  setLang(e) {
    var lang = e.currentTarget.dataset.lang;
    if (lang === I18n.getLang()) return;
    I18n.setLang(lang);
    this.setData({ lang: lang });
    this._updateI18n();
    this._rebuildView();
    wx.showToast({ title: lang === 'zh' ? '已切换为中文' : 'Switched to English', icon: 'none', duration: 1200 });
  },

  switchTradition(e) {
    var tradition = e.currentTarget.dataset.tradition;
    if (tradition === this.data.tradition) return;
    this._loadTradition(tradition);
    this._updateI18n();
  },

  toggleFilter() {
    this.setData({ showFilter: !this.data.showFilter, showIndex: false });
  },

  toggleIndex() {
    this.setData({ showIndex: !this.data.showIndex, showFilter: false });
  },

  closeIndex() {
    this.setData({ showIndex: false });
  },

  toggleFilterTag(e) {
    var tag = e.currentTarget.dataset.tag;
    if (this._activeFilters.has(tag)) {
      this._activeFilters.delete(tag);
    } else {
      this._activeFilters.add(tag);
    }
    this._rebuildView();
  },

  selectAllFilters() {
    this._activeFilters = new Set(FILTER_TAGS[this.data.tradition]);
    this._rebuildView();
  },

  clearAllFilters() {
    this._activeFilters = new Set();
    this._rebuildView();
  },

  onSearch(e) {
    this._searchText = e.detail.value || '';
    this.setData({ searchText: this._searchText });
    this._buildListData();
  },

  onSearchConfirm() {
    this._buildListData();
  },

  clearSearch() {
    this._searchText = '';
    this.setData({ searchText: '' });
    this._buildListData();
  },

  // Jump to a philosopher card via index
  jumpToPhil(e) {
    var id = e.currentTarget.dataset.id;
    this.setData({
      showIndex: false,
      scrollToId: 'card-' + id,
    });
    // Reset after scroll so we can tap same item again
    setTimeout(function() {
      this.setData({ scrollToId: '' });
    }.bind(this), 500);
  },

  // Navigate to detail page
  onCardTap(e) {
    var id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/detail/detail?id=' + id + '&tradition=' + this.data.tradition,
    });
  },

  onIdeaTap(e) {
    var id = e.currentTarget.dataset.philid;
    var ideaId = e.currentTarget.dataset.ideaid;
    wx.navigateTo({
      url: '/pages/detail/detail?id=' + id + '&tradition=' + this.data.tradition + '&ideaId=' + ideaId,
    });
  },

  // Scroll to top
  scrollTop() {
    this.setData({ scrollToId: 'era-' + (this.data.eras[0] ? this.data.eras[0].id.replace('era-', '') : '') });
    setTimeout(function() {
      this.setData({ scrollToId: '' });
    }.bind(this), 500);
  },
});
