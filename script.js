
function show(id, el) {
  document.querySelectorAll('section').forEach(s => s.classList.remove('visible'));
  document.getElementById(id).classList.add('visible');
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
  if (el) el.classList.add('active');
  window.scrollTo(0, 0);
}

function showTop(group, id, el) {
  document.querySelectorAll('.top-tab-panel[data-group="' + group + '"]').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelectorAll('.top-tab-btn[data-group="' + group + '"]').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
}

function showSub(group, id, el) {
  document.querySelectorAll('.sub-tab-panel[data-group="' + group + '"]').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelectorAll('.sub-tab-btn[data-group="' + group + '"]').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
}
