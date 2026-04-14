/**
 * SelectionManager — click highlight logic (shared by panel + renderers)
 */
const SelectionManager = (() => {

  function clearAll() {
    // Clear card states
    document.querySelectorAll('.philosopher-card').forEach(c => {
      c.classList.remove('selected', 'dimmed');
    });
    document.querySelectorAll('.idea-item').forEach(i => {
      i.classList.remove('selected');
    });
    ConnectionRenderer.clearHighlight();
    State.clearSelection();
  }

  function selectPhilosopher(philId) {
    const alreadySelected = State.get('selectedPhilosopherId') === philId && !State.get('selectedIdeaId');
    clearAll();
    if (alreadySelected) return;

    State.selectIdea(philId, null);

    // Highlight the card
    const myCard = document.getElementById(`card-${philId}`);
    if (myCard) myCard.classList.add('selected');

    // Dim other cards
    const connsByIdea = State.get('connectionsByIdea');
    const phil = State.get('philosopherMap')[philId];
    const connectedPhils = new Set([philId]);
    if (phil) {
      for (const idea of phil.ideas) {
        const myConns = connsByIdea[idea.id] || [];
        myConns.forEach(c => {
          connectedPhils.add(c.fromPhil);
          connectedPhils.add(c.toPhil);
        });
      }
    }

    document.querySelectorAll('.philosopher-card').forEach(c => {
      if (!connectedPhils.has(c.dataset.philId)) c.classList.add('dimmed');
    });

    ConnectionRenderer.applySelectionHighlight(null, philId);
  }

  function selectIdea(philId, ideaId) {
    const alreadySelected = State.get('selectedIdeaId') === ideaId;
    clearAll();
    if (alreadySelected) return;

    State.selectIdea(philId, ideaId);

    // Mark idea as selected
    const ideaEl = document.getElementById(`idea-${ideaId}`);
    if (ideaEl) ideaEl.classList.add('selected');

    // Highlight the card
    const myCard = document.getElementById(`card-${philId}`);
    if (myCard) myCard.classList.add('selected');

    // Determine connected philosophers
    const connsByIdea = State.get('connectionsByIdea');
    const myConns = connsByIdea[ideaId] || [];
    const connectedPhils = new Set([philId]);
    myConns.forEach(c => {
      connectedPhils.add(c.fromPhil);
      connectedPhils.add(c.toPhil);
    });

    document.querySelectorAll('.philosopher-card').forEach(c => {
      if (!connectedPhils.has(c.dataset.philId)) c.classList.add('dimmed');
    });

    // Highlight connected ideas
    myConns.forEach(c => {
      const otherId = c.from === ideaId ? c.to : c.from;
      const otherEl = document.getElementById(`idea-${otherId}`);
      if (otherEl) otherEl.classList.add('selected');
    });

    ConnectionRenderer.applySelectionHighlight(ideaId, philId);
  }

  function selectConnection(conn) {
    clearAll();
    // Treat as selecting the 'from' idea
    selectIdea(conn.fromPhil, conn.from);
  }

  return { clearAll, selectPhilosopher, selectIdea, selectConnection };
})();
