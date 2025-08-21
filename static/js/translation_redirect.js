document.addEventListener("DOMContentLoaded", function () {
  // Прокрутка к истории
  const chatHistory = document.querySelector('.chat-history');
  if (chatHistory) {
    setTimeout(() => chatHistory.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
  }

  // Переключение языков
  const swapBtn = document.getElementById("swap-languages");
  if (!swapBtn) return;

  swapBtn.addEventListener("click", function () {
    const src = document.getElementById("source_lang");
    const tgt = document.getElementById("target_lang");
    if (!src || !tgt) return;

    // Если выбран placeholder (disabled), попробуем сдвинуться на первый реальный пункт
    const fixIndex = (sel) => {
      if (sel.selectedIndex < 0) sel.selectedIndex = 0;
      // если отмечен disabled — сместиться на следующий доступный
      if (sel.options[sel.selectedIndex]?.disabled) {
        for (let i = 0; i < sel.options.length; i++) {
          if (!sel.options[i].disabled) { sel.selectedIndex = i; break; }
        }
      }
    };
    fixIndex(src);
    fixIndex(tgt);

    // Меняем выбранные элементы местами по индексу
    const srcIdx = src.selectedIndex;
    const tgtIdx = tgt.selectedIndex;
    src.selectedIndex = tgtIdx;
    tgt.selectedIndex = srcIdx;

    // Сообщим слушателям об изменении (на случай сторонних обработчиков)
    src.dispatchEvent(new Event('change', { bubbles: true }));
    tgt.dispatchEvent(new Event('change', { bubbles: true }));
  });
});