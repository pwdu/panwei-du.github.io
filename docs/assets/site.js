/* No framework or tracking. All research content remains readable without JavaScript. */
document.documentElement.classList.add('js');
// Preserve incoming section links from the former single-page homepage.
if (document.body.dataset.page === 'home') {
  const destinations = { research: 'research/', publications: 'publications/', experience: 'experience/', teaching: 'experience/#teaching', contact: 'contact/' };
  const destination = destinations[location.hash.slice(1)];
  if (destination) location.replace(new URL(destination, location.href.split('#')[0]).href);
}
const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#nav');
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('open', open);
});
navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  toggle.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('open');
}));
const mesh = document.querySelector('#mesh-lines');
if (mesh) {
  const point = (u, v) => {
    const x = 50 + u * 315 + v * 126;
    const height = 104 * Math.sin(u * Math.PI) * Math.sin(v * Math.PI) + 44 * Math.sin(u * 2.6 + v * 1.3);
    return [x, 305 - u * 83 + v * 113 - height];
  };
  for (let axis = 0; axis < 2; axis++) {
    for (let line = 0; line <= 23; line++) {
      const vertices = [];
      for (let step = 0; step <= 52; step++) {
        const p = axis ? point(step / 52, line / 23) : point(line / 23, step / 52);
        vertices.push(`${step ? 'L' : 'M'}${p[0].toFixed(2)},${p[1].toFixed(2)}`);
      }
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', vertices.join(' '));
      mesh.append(path);
    }
  }
}
const papers = [...document.querySelectorAll('#publication-list .paper')];
const filters = [...document.querySelectorAll('[data-filter]')];
const search = document.querySelector('#publication-search');
let activeFilter = document.querySelector('#publication-list')?.dataset.defaultFilter || 'selected';
function updatePapers() {
  const query = search.value.toLowerCase().trim();
  let shown = 0;
  papers.forEach(paper => {
    const category = activeFilter === 'all' || (activeFilter === 'selected' ? paper.dataset.selected === 'true' : paper.dataset.category === activeFilter);
    const match = paper.textContent.toLowerCase().includes(query);
    paper.hidden = !(category && match);
    if (!paper.hidden) shown++;
  });
  filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === activeFilter)));
  document.querySelector('#publication-count').textContent = `${shown} ${activeFilter === 'selected' ? 'selected ' : ''}${shown === 1 ? 'journal paper' : 'journal papers'}${activeFilter === 'all' && !query ? ' · 2019–2026' : ''}`;
  document.querySelector('#no-results').hidden = shown > 0;
}
if (papers.length) {
  document.querySelector('.publication-tools').hidden = false;
  filters.forEach(button => button.addEventListener('click', () => { activeFilter = button.dataset.filter; updatePapers(); }));
  search.addEventListener('input', () => { if (search.value.trim()) activeFilter = 'all'; updatePapers(); });
  updatePapers();
}
document.querySelector('.print-button')?.addEventListener('click', () => window.print());
