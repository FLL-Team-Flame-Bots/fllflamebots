
function show(id, el) {
  document.querySelectorAll('section').forEach(s => s.classList.remove('visible'));
  document.getElementById(id).classList.add('visible');
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
  if (el) el.classList.add('active');
  window.scrollTo(0, 0);
}
