const filters = document.querySelector('.filters');
if (filters) {
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    const category = button.dataset.filter;
    filters.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    document.querySelectorAll('.paper[data-category]').forEach(paper => {
      paper.hidden = category !== 'All' && paper.dataset.category !== category;
      if (!paper.hidden) count++;
    });
    document.querySelectorAll('.pub-year').forEach(group => {
      group.hidden = !Array.from(group.querySelectorAll('.paper')).some(paper => !paper.hidden);
    });
    document.querySelector('.filter-status').textContent = `${count} publications`;
  });
}
