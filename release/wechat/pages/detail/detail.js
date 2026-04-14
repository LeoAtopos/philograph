// pages/detail/detail.js
const I18n = require('../../utils/i18n.js');
const westernPhil = require('../../data/philosophers.js');
const westernConn = require('../../data/connections.js');
const chinesePhil = require('../../data/chinese-philosophers.js');
const chineseConn = require('../../data/chinese-connections.js');

const TAG_CLASS_MAP = {
  'Basics':'basics','Metaphysics':'metaphysics','Epistemology':'epistemology',
  'Logic':'logic','Ethics':'ethics','Political':'political','Aesthetics':'aesthetics',
  'Religion':'religion','Mind':'mind','Language':'language','Science':'science',
  'Metaphilosophy':'metaphilosophy','Confucianism':'confucianism','Taoism':'taoism',
  'Mohism':'mohism','Legalism':'legalism','Neo-Confucianism':'neo-confucianism',
  'Cosmology':'cosmology','Buddhism':'buddhism','Education':'education','History':'history'
};

Page({
  data: {
    phil: {},
    ideas: [],
    selectedIdeaId: '',
    selectedIdeaText: '',
    connectedItems: [],
    allConnections: [],
    scrollTargetIdea: '',
    i18n: {},
  },

  _tradition: 'western',
  _philId: '',
  _allPhilosophers: [],
  _allConnections: [],
  _connectionsByIdea: {},
  _philosopherMap: {},

  onLoad(options) {
    const app = getApp();
    I18n.init(app.globalData.lang || 'zh');

    this._tradition = options.tradition || 'western';
    this._philId = options.id;

    this._allPhilosophers = this._tradition === 'chinese' ? chinesePhil : westernPhil;
    this._allConnections = this._tradition === 'chinese' ? chineseConn : westernConn;

    // Build maps
    this._philosopherMap = {};
    for (const p of this._allPhilosophers) {
      this._philosopherMap[p.id] = p;
    }

    this._connectionsByIdea = {};
    for (const conn of this._allConnections) {
      if (!this._connectionsByIdea[conn.from]) this._connectionsByIdea[conn.from] = [];
      if (!this._connectionsByIdea[conn.to])   this._connectionsByIdea[conn.to]   = [];
      this._connectionsByIdea[conn.from].push(conn);
      this._connectionsByIdea[conn.to].push(conn);
    }

    this._renderPhil(options.ideaId);
    this._updateI18n();
  },

  _renderPhil(preselectedIdeaId) {
    const philData = this._philosopherMap[this._philId];
    if (!philData) return;

    const displayName = I18n.t('name', philData.id);
    const years = I18n.formatYears(philData.born, philData.died);
    const eraLabel = I18n.t('era', philData.era);

    // Count all agree/disagree for this philosopher
    let agreeCount = 0, disagreeCount = 0;
    for (const idea of philData.ideas) {
      const conns = this._connectionsByIdea[idea.id] || [];
      agreeCount += conns.filter(c => c.type === 'P').length;
      disagreeCount += conns.filter(c => c.type === 'N').length;
    }

    // Portrait
    let portrait = philData.portrait || '';
    if (portrait.startsWith('https://placehold')) portrait = '';

    const tagBadges = (philData.tags || []).slice(0, 3).map(tag => ({
      label: I18n.t('tag', tag),
      cls: TAG_CLASS_MAP[tag] || 'basics',
    }));

    const phil = {
      id: philData.id,
      displayName,
      years,
      eraLabel,
      portrait,
      initials: philData.name.slice(0, 2).toUpperCase(),
      tagBadges,
      agreeCount,
      disagreeCount,
      ideaCount: philData.ideas.length,
    };

    // Ideas
    const ideas = philData.ideas.map(idea => {
      const conns = this._connectionsByIdea[idea.id] || [];
      const agCount = conns.filter(c => c.type === 'P').length;
      const disCount = conns.filter(c => c.type === 'N').length;
      const primaryTag = (idea.tags && idea.tags[0]) || 'Basics';
      const tagBadges = (idea.tags || []).slice(0, 2).map(tag => ({
        label: I18n.t('tag', tag),
        cls: TAG_CLASS_MAP[tag] || 'basics',
      }));
      return {
        id: idea.id,
        text: I18n.t('idea', idea.id),
        dotCls: primaryTag,
        tagBadges,
        agreeCount: agCount,
        disagreeCount: disCount,
        selected: idea.id === preselectedIdeaId,
      };
    });

    // Build all connections for overview
    const allConns = [];
    const seen = new Set();
    for (const idea of philData.ideas) {
      const conns = this._connectionsByIdea[idea.id] || [];
      for (const conn of conns) {
        const key = `${conn.from}-${conn.to}`;
        if (seen.has(key)) continue;
        seen.add(key);
        const isFrom = conn.fromPhil === this._philId;
        const targetPhilId = isFrom ? conn.toPhil : conn.fromPhil;
        const targetIdeaId = isFrom ? conn.to : conn.from;
        const myIdeaId = isFrom ? conn.from : conn.to;
        const targetPhil = this._philosopherMap[targetPhilId];
        if (!targetPhil) continue;

        const myIdeaText = I18n.t('idea', myIdeaId);
        const theirIdeaText = I18n.t('idea', targetIdeaId);
        const connKey = `${conn.from}-${conn.to}`;
        const label = I18n.t('conn', connKey);

        allConns.push({
          id: key,
          type: conn.type,
          targetPhilId,
          targetIdeaId,
          philName: I18n.t('name', targetPhilId),
          myIdeaText: myIdeaText.length > 40 ? myIdeaText.slice(0, 38) + '…' : myIdeaText,
          theirIdeaText: theirIdeaText.length > 40 ? theirIdeaText.slice(0, 38) + '…' : theirIdeaText,
          direction: isFrom
            ? (I18n.getLang() === 'zh' ? '→ 影响/影响了' : '→ Influenced')
            : (I18n.getLang() === 'zh' ? '← 被影响于' : '← Influenced by'),
          label: label !== connKey ? label : '',
        });
      }
    }

    this.setData({ phil, ideas, allConnections: allConns });

    // Auto-select and scroll to preselected idea
    if (preselectedIdeaId) {
      this.setData({ scrollTargetIdea: '' });
      setTimeout(function() {
        this.setData({ scrollTargetIdea: 'idea-' + preselectedIdeaId });
        this._selectIdea(preselectedIdeaId);
      }.bind(this), 300);
    }

    // Set navigation title
    wx.setNavigationBarTitle({ title: displayName });
  },

  _selectIdea(ideaId) {
    const philData = this._philosopherMap[this._philId];
    if (!philData) return;

    const ideaData = philData.ideas.find(i => i.id === ideaId);
    if (!ideaData) return;

    const conns = this._connectionsByIdea[ideaId] || [];
    const connectedItems = conns.map(conn => {
      const isFrom = conn.from === ideaId;
      const targetPhilId = isFrom ? conn.toPhil : conn.fromPhil;
      const targetIdeaId = isFrom ? conn.to : conn.from;
      const targetPhil = this._philosopherMap[targetPhilId];
      if (!targetPhil) return null;

      const connKey = `${conn.from}-${conn.to}`;
      const label = I18n.t('conn', connKey);

      return {
        id: connKey,
        type: conn.type,
        philId: targetPhilId,
        ideaId: targetIdeaId,
        philName: I18n.t('name', targetPhilId),
        ideaText: I18n.t('idea', targetIdeaId),
        label: label !== connKey ? label : '',
      };
    }).filter(Boolean);

    const selectedIdeaText = I18n.t('idea', ideaId);
    const displayText = selectedIdeaText.length > 30 ? selectedIdeaText.slice(0, 28) + '…' : selectedIdeaText;

    // Update selected state on ideas
    const ideas = this.data.ideas.map(i => ({ ...i, selected: i.id === ideaId }));

    this.setData({
      ideas,
      selectedIdeaId: ideaId,
      selectedIdeaText: displayText,
      connectedItems,
    });
  },

  _updateI18n() {
    this.setData({
      i18n: {
        legendAgree: I18n.t('ui.legendAgree'),
        legendDisagree: I18n.t('ui.legendDisagree'),
        ideasLabel: I18n.getLang() === 'zh' ? '个思想' : 'Ideas',
        ideasSection: I18n.getLang() === 'zh' ? '思想条目' : 'IDEAS',
        connections: I18n.getLang() === 'zh' ? '相关连线' : 'CONNECTIONS',
        noConnections: I18n.getLang() === 'zh' ? '暂无相关连线' : 'No connections',
        allConnections: I18n.getLang() === 'zh' ? '全部连线' : 'ALL CONNECTIONS',
        total: I18n.getLang() === 'zh' ? '条' : 'total',
      }
    });
  },

  // ===== 事件处理 =====
  goBack() {
    wx.navigateBack();
  },

  selectIdea(e) {
    const ideaId = e.currentTarget.dataset.id;
    if (ideaId === this.data.selectedIdeaId) {
      // 取消选择
      const ideas = this.data.ideas.map(i => ({ ...i, selected: false }));
      this.setData({ ideas, selectedIdeaId: '', connectedItems: [] });
    } else {
      this._selectIdea(ideaId);
    }
  },

  jumpToPhil(e) {
    const id = e.currentTarget.dataset.id;
    const targetIdeaId = e.currentTarget.dataset.targetIdeaId || '';
    let url = '/pages/detail/detail?id=' + id + '&tradition=' + this._tradition;
    if (targetIdeaId) url += '&ideaId=' + targetIdeaId;
    wx.navigateTo({ url: url });
  },
});
