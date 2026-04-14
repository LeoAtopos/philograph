/**
 * state.js — Global application state
 */
const State = (() => {
  const _state = {
    // Canvas transform
    scale: 0.75,
    translateX: 0,
    translateY: 0,

    // Selection
    selectedPhilosopherId: null,
    selectedIdeaId: null,

    // Filters: set of active tag names
    activeFilters: new Set([
      'Metaphysics','Epistemology','Logic','Ethics','Political',
      'Aesthetics','Religion','Mind','Language','Science','Metaphilosophy','Basics'
    ]),

    // Options
    darkMode: true,
    showPortraits: true,
    showLabels: false,
    showEras: true,

    // Tradition
    currentTradition: 'western', // 'western' | 'chinese'

    // Language
    currentLang: 'en', // 'en' | 'zh'

    // Data
    philosophers: [],
    connections: [],

    // Cached data for both traditions
    westernPhilosophers: [],
    westernConnections: [],
    chinesePhilosophers: [],
    chineseConnections: [],

    // Derived maps (populated after data load)
    philosopherMap: {},    // id -> philosopher
    ideaMap: {},           // ideaId -> {phil, idea}
    connectionsByIdea: {}, // ideaId -> [connections]
  };

  // Filter tags per tradition
  const FILTER_TAGS = {
    western: ['Basics','Metaphysics','Epistemology','Logic','Ethics','Political','Aesthetics','Religion','Mind','Language','Science','Metaphilosophy'],
    chinese: ['Confucianism','Taoism','Mohism','Legalism','Neo-Confucianism','Buddhism','Ethics','Political','Metaphysics','Epistemology','Aesthetics','Mind','Language','Education','History']
  };

  // Era order per tradition
  const ERA_ORDER = {
    western: ['Ancient', 'Medieval', 'Early Modern', 'Enlightenment', 'German Idealism', '19th Century', 'Analytic Origins', 'Analytic', 'Continental', '20th Century'],
    chinese: ['Pre-Qin', 'Han', 'Wei-Jin', 'Sui-Tang', 'Tang-Song', 'Ming-Qing', 'Modern']
  };

  // --- Private helper: rebuild derived maps from current philosophers/connections ---
  function buildMaps() {
    _state.philosopherMap = {};
    _state.ideaMap = {};
    _state.connectionsByIdea = {};

    for (const phil of _state.philosophers) {
      _state.philosopherMap[phil.id] = phil;
      for (const idea of phil.ideas) {
        _state.ideaMap[idea.id] = { phil, idea };
      }
    }

    for (const conn of _state.connections) {
      if (!_state.connectionsByIdea[conn.from]) _state.connectionsByIdea[conn.from] = [];
      if (!_state.connectionsByIdea[conn.to])   _state.connectionsByIdea[conn.to]   = [];
      _state.connectionsByIdea[conn.from].push(conn);
      _state.connectionsByIdea[conn.to].push(conn);
    }
  }

  return {
    get(key) { return _state[key]; },
    set(key, value) { _state[key] = value; },
    getState() { return _state; },

    // Convenience setters
    setTransform(scale, tx, ty) {
      _state.scale = scale;
      _state.translateX = tx;
      _state.translateY = ty;
    },
    selectIdea(philId, ideaId) {
      _state.selectedPhilosopherId = philId;
      _state.selectedIdeaId = ideaId;
    },
    clearSelection() {
      _state.selectedPhilosopherId = null;
      _state.selectedIdeaId = null;
    },
    toggleFilter(tag) {
      if (_state.activeFilters.has(tag)) {
        _state.activeFilters.delete(tag);
      } else {
        _state.activeFilters.add(tag);
      }
    },
    setAllFilters(tags) { _state.activeFilters = new Set(tags); },
    clearAllFilters() { _state.activeFilters = new Set(); },

    getFilterTags(tradition) {
      return FILTER_TAGS[tradition || _state.currentTradition];
    },

    getEraOrder(tradition) {
      return ERA_ORDER[tradition || _state.currentTradition];
    },

    switchTradition(tradition) {
      _state.currentTradition = tradition;
      if (tradition === 'chinese') {
        _state.philosophers = _state.chinesePhilosophers;
        _state.connections = _state.chineseConnections;
      } else {
        _state.philosophers = _state.westernPhilosophers;
        _state.connections = _state.westernConnections;
      }
      // Reset filters to default for this tradition
      _state.activeFilters = new Set(FILTER_TAGS[tradition]);
      // Clear selection
      _state.selectedPhilosopherId = null;
      _state.selectedIdeaId = null;
      // Rebuild derived maps
      buildMaps();
    },

    buildMaps
  };
})();
