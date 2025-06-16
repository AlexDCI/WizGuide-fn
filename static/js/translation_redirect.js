// static/js/translation_redirect.js

// Пример с имитацией завершения перевода после запроса
document.addEventListener("DOMContentLoaded", function () {
    const translateButton = document.querySelector(".cta-button");

    if (translateButton) {
        translateButton.addEventListener("click", function (e) {
            // Можно заменить на реальную логику, если есть async-запрос
            e.preventDefault();

            // Здесь может быть ваш fetch() или Ajax запрос — и после успешного ответа:
            // setTimeout используется как имитация "завершения перевода"
            setTimeout(() => {
                window.location.href = "/history/";
            }, 3000); // 3 секунды — замени на реальное событие
        });
    }
});