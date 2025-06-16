document.addEventListener("DOMContentLoaded", function () {
    // Прокрутка к истории переводов, если она есть
    var chatHistory = document.querySelector('.chat-history');
    if (chatHistory) {
        setTimeout(function() {
            chatHistory.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 200);
    }

    // Кнопка смены языков
    var swapBtn = document.getElementById("swap-languages");
    if (swapBtn) {
        swapBtn.addEventListener("click", function () {
            let sourceLang = document.getElementById("source_lang");
            let targetLang = document.getElementById("target_lang");
            let temp = sourceLang.value;
            sourceLang.value = targetLang.value;
            targetLang.value = temp;
        });
    }
});
