/**
 * card-renderer.js — Philosopher card DOM generation and update
 */
const CardRenderer = (() => {

  function getEraOrder() {
    return State.getEraOrder();
  }

  function getTagClass(tag) {
    const map = {
      'Metaphysics': 'metaphysics', 'Epistemology': 'epistemology', 'Ethics': 'ethics',
      'Logic': 'logic', 'Political': 'political', 'Aesthetics': 'aesthetics',
      'Religion': 'religion', 'Mind': 'mind', 'Language': 'language',
      'Science': 'science', 'Metaphilosophy': 'metaphilosophy', 'Basics': 'basics',
      'Confucianism': 'confucianism', 'Taoism': 'taoism', 'Mohism': 'mohism',
      'Legalism': 'legalism', 'Neo-Confucianism': 'neo-confucianism', 'Cosmology': 'cosmology'
    };
    return map[tag] || 'basics';
  }

  function buildCard(phil) {
    const card = document.createElement('div');
    card.className = 'philosopher-card';
    card.id = `card-${phil.id}`;
    card.dataset.philId = phil.id;

    // Check if any idea has connections for agree/disagree classes
    const connMap = State.get('connectionsByIdea');

    // --- Header ---
    const header = document.createElement('div');
    header.className = 'card-header';

    // Portrait
    const portrait = document.createElement('img');
    portrait.className = 'card-portrait';
    portrait.src = phil.portrait;
    portrait.alt = I18n.t('name', phil.id);
    portrait.onerror = function() {
      this.src = `https://placehold.co/44x44/1a1a3e/9ca3b8?text=${encodeURIComponent(phil.name.slice(0,2).toUpperCase())}`;
    };
    if (!State.get('showPortraits')) portrait.classList.add('hidden');
    portrait.dataset.portrait = 'true';

    const meta = document.createElement('div');
    meta.className = 'card-meta';

    const nameEl = document.createElement('div');
    nameEl.className = 'card-name';
    nameEl.textContent = I18n.t('name', phil.id);
    nameEl.addEventListener('click', (e) => {
      e.stopPropagation();
      SelectionManager.selectPhilosopher(phil.id);
    });

    const yearsEl = document.createElement('div');
    yearsEl.className = 'card-years';
    yearsEl.textContent = I18n.formatYears(phil.born, phil.died);

    const eraEl = document.createElement('div');
    eraEl.className = 'card-era era-tag';
    eraEl.textContent = I18n.t('era', phil.era);

    meta.appendChild(nameEl);
    meta.appendChild(yearsEl);
    meta.appendChild(eraEl);

    header.appendChild(portrait);
    header.appendChild(meta);
    card.appendChild(header);

    // --- Tag badges ---
    const tagsEl = document.createElement('div');
    tagsEl.className = 'card-tags';
    const shownTags = phil.tags.slice(0, 3);
    for (const tag of shownTags) {
      const badge = document.createElement('span');
      badge.className = `tag-badge tag-${getTagClass(tag)}`;
      badge.textContent = I18n.t('tag', tag);
      tagsEl.appendChild(badge);
    }
    card.appendChild(tagsEl);

    // --- Ideas list ---
    const ideasEl = document.createElement('ul');
    ideasEl.className = 'card-ideas';

    for (const idea of phil.ideas) {
      const li = document.createElement('li');
      li.className = 'idea-item';
      li.id = `idea-${idea.id}`;
      li.dataset.ideaId = idea.id;
      li.dataset.philId = phil.id;

      // Determine primary tag for dot
      const primaryTag = idea.tags && idea.tags[0] ? idea.tags[0] : 'Basics';
      const dot = document.createElement('span');
      dot.className = `idea-dot ${primaryTag}`;

      const text = document.createElement('span');
      text.className = 'idea-text';
      text.textContent = I18n.t('idea', idea.id);

      li.appendChild(dot);
      li.appendChild(text);

      // Add connection type hints
      const myConns = connMap[idea.id] || [];
      const hasAgree = myConns.some(c => c.type === 'P');
      const hasDisagree = myConns.some(c => c.type === 'N');
      if (hasAgree) li.classList.add('has-agree');
      if (hasDisagree) li.classList.add('has-disagree');

      li.addEventListener('click', (e) => {
        e.stopPropagation();
        SelectionManager.selectIdea(phil.id, idea.id);
      });

      ideasEl.appendChild(li);
    }

    card.appendChild(ideasEl);
    return card;
  }

  function render() {
    const philosophers = State.get('philosophers');
    const container = document.getElementById('philosophersContainer');
    container.innerHTML = '';

    // Group by era
    const groups = {};
    for (const phil of philosophers) {
      if (!groups[phil.era]) groups[phil.era] = [];
      groups[phil.era].push(phil);
    }

    // Sort eras
    const sortedEras = getEraOrder().filter(e => groups[e]);

    for (const era of sortedEras) {
      const eraPhils = groups[era];
      const eraGroup = document.createElement('div');
      eraGroup.className = 'era-group';
      eraGroup.dataset.era = era;

      const eraLabel = document.createElement('div');
      eraLabel.className = `era-label${State.get('showEras') ? '' : ' hidden'}`;
      eraLabel.textContent = I18n.t('era', era);
      eraLabel.dataset.eraLabel = 'true';
      eraGroup.appendChild(eraLabel);

      // Sort philosophers within era by birth year
      eraPhils.sort((a, b) => (a.born || 0) - (b.born || 0));

      for (const phil of eraPhils) {
        eraGroup.appendChild(buildCard(phil));
      }

      container.appendChild(eraGroup);
    }
  }

  function updatePortraitVisibility(show) {
    document.querySelectorAll('[data-portrait]').forEach(img => {
      img.classList.toggle('hidden', !show);
    });
  }

  function updateEraVisibility(show) {
    document.querySelectorAll('[data-era-label]').forEach(el => {
      el.classList.toggle('hidden', !show);
    });
  }

  function applyFilters() {
    const activeFilters = State.get('activeFilters');
    const philosophers = State.get('philosophers');

    for (const phil of philosophers) {
      const card = document.getElementById(`card-${phil.id}`);
      if (!card) continue;

      // A card is visible if any of its tags (or ideas' tags) matches active filters
      const philTags = new Set(phil.tags);
      const ideaTags = new Set(phil.ideas.flatMap(i => i.tags || []));
      const allTags = new Set([...philTags, ...ideaTags]);

      const visible = activeFilters.size === 0 || [...allTags].some(t => activeFilters.has(t));
      card.classList.toggle('filtered-out', !visible);
    }
  }

  return { render, updatePortraitVisibility, updateEraVisibility, applyFilters, getTagClass, getEraOrder };
})();
