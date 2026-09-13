// Reads content straight from the rendered shelf rows — no duplicated
// data here, this just wires up the hover-preview pane on the homepage.
document.addEventListener('DOMContentLoaded', function () {
  var stack = document.getElementById('preview-stack');
  var titleEl = document.getElementById('preview-title');
  var metaEl = document.getElementById('preview-meta');
  var hintEl = document.getElementById('preview-hint');
  if (!stack) return; // not on the homepage

  var p1 = stack.querySelector('.p1');
  var p2 = stack.querySelector('.p2');
  var p3 = stack.querySelector('.p3');

  function setCard(card, url) {
    if (url) {
      card.style.backgroundImage = "url('" + url + "')";
      card.style.backgroundSize = 'cover';
      card.style.backgroundPosition = 'center';
    } else {
      card.style.backgroundImage = '';
      card.style.backgroundSize = '';
      card.style.backgroundPosition = '';
    }
  }

  document.querySelectorAll('.shelf-row').forEach(function (row) {
    function activate() {
      var type = row.dataset.type;
      var titleNode = row.querySelector('.title');
      var tagNode = row.querySelector('.tag');

      stack.dataset.type = type;
      stack.classList.add('filled', 'fanned');

      setCard(p1, row.dataset.cover1);
      setCard(p2, row.dataset.cover2);
      setCard(p3, row.dataset.cover3);

      if (titleNode) titleEl.textContent = titleNode.textContent;
      if (tagNode) metaEl.textContent = tagNode.textContent;
      if (hintEl) hintEl.style.display = 'none';
    }
    function deactivate() {
      stack.classList.remove('fanned');
    }
    row.addEventListener('mouseenter', activate);
    row.addEventListener('mouseleave', deactivate);
    row.addEventListener('focus', activate);
    row.addEventListener('blur', deactivate);
  });
});
