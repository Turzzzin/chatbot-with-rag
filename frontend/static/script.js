let id = "";
const API_URL = "http://localhost:8000/ask";

function sendMessage() {
  const inputField = document.getElementById("input");
  let input = inputField.value.trim();
  if (input !== "") {
    handleChat(input);
    inputField.value = "";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("input");
  const sendBtn = document.querySelector(".send");
  sendBtn.addEventListener("click", sendMessage);

  inputField.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
});

function handleChat(userMsg) {
  const mainDiv = document.getElementById("message-section");

  let userDiv = document.createElement("div");
  userDiv.classList.add("message", "user-message");
  userDiv.innerHTML = `<span>${userMsg}</span>`;
  mainDiv.appendChild(userDiv);

  let botDiv = document.createElement("div");
  botDiv.classList.add("message", "bot-message");
  botDiv.innerHTML = `<span class="loading">...</span>`;
  mainDiv.appendChild(botDiv);

  scrollChat();

  fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: userMsg, session_id: id }),
  })
    .then((response) => response.json())
    .then((body) => {
      if (!id && body.session_id) {
        id = body.session_id;
      }
      botDiv.querySelector("span").classList.remove("loading");
      botDiv.querySelector("span").innerHTML =
        (body.answer || body.message || "Sem resposta").replace(/\n/g, "<br>");
      scrollChat();
    })
    .catch((error) => {
      botDiv.querySelector("span").classList.remove("loading");
      botDiv.querySelector("span").innerHTML =
        "Parece ter um erro no servidor!<br>Por favor, entre em contato com o responsável técnico.";
      scrollChat();
    });
}

function scrollChat() {
  const messageSection = document.getElementById("message-section");
  messageSection.scrollTop = messageSection.scrollHeight;
}
