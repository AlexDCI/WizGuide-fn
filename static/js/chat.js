document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const responseDiv = document.getElementById("response");

    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();
            const formData = new FormData(form);
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch(form.action || "", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken
                    },
                    body: formData,
                });

                const data = await response.json();
                if (response.ok) {
                    responseDiv.innerHTML = `<p><b>Ответ ИИ:</b> ${data.response}</p>`;
                } else {
                    responseDiv.innerHTML = `<p style="color:red;">Ошибка: ${data.error}</p>`;
                }
            } catch (error) {
                responseDiv.innerHTML = `<p style="color:red;">Произошла ошибка: ${error.message}</p>`;
            }
        });
    }
});
