document.querySelectorAll('.slider-nav').forEach(btn => {
  btn.addEventListener('click', () => {
    const targetId = btn.dataset.target;
    const slider = document.getElementById(targetId);
    const scrollAmount = btn.classList.contains('next')
      ? slider.offsetWidth
      : -slider.offsetWidth;
    slider.scrollBy({ left: scrollAmount * 0.8, behavior: 'smooth' });
  });
});
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('search-input');
  const box   = document.getElementById('suggestions');
  let timer;

  function escapeRegex(s){ return s.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'); }

  input.addEventListener('input', () => {
    clearTimeout(timer);
    const q = input.value.trim();
    if (!q) { box.classList.add('d-none'); return; }

    timer = setTimeout(() => {
      fetch(`/ajax/suggest/?q=${encodeURIComponent(q)}`)
        .then(r => r.json())
        .then(data => {
          if (!data.results.length) {
            box.classList.add('d-none');
            return;
          }
          const regex = new RegExp(`(${escapeRegex(q)})`, 'i');
          box.innerHTML = data.results.map(item => {
            // resaltamos la coincidencia
            const title = item.title.replace(regex, '<strong>$1</strong>');
            return `<div class="suggestion-item" data-id="${item.id}">${title}</div>`;
          }).join('');
          box.classList.remove('d-none');

          // clic en sugerencia: rellenar y enviar
          box.querySelectorAll('.suggestion-item').forEach(div => {
            div.addEventListener('click', () => {
              input.value = div.textContent;
              box.classList.add('d-none');
              input.form.submit();
            });
          });
        });
    }, 300); // espera 300 ms tras última tecla
  });

  // cerrar al perder foco
  document.addEventListener('click', e => {
    if (!input.contains(e.target) && !box.contains(e.target)) {
      box.classList.add('d-none');
    }
  });
});
