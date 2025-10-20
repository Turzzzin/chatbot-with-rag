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

  // Theme toggle logic
  const themeToggle = document.getElementById("theme-toggle");
  const body = document.body;

  const applyTheme = () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      body.classList.add("dark-theme");
      themeToggle.innerHTML = "☀️";
    } else {
      body.classList.remove("dark-theme");
      themeToggle.innerHTML = "🌙";
    }
  };

  applyTheme();

  themeToggle.addEventListener("click", () => {
    if (body.classList.contains("dark-theme")) {
      body.classList.remove("dark-theme");
      localStorage.setItem("theme", "light");
      themeToggle.innerHTML = "🌙";
    } else {
      body.classList.add("dark-theme");
      localStorage.setItem("theme", "dark");
      themeToggle.innerHTML = "☀️";
    }
  });

  // Modal logic
  const modal = document.getElementById("warning-modal");
  const closeButton = document.querySelector(".close-button");

  if (!sessionStorage.getItem("modalShown")) {
    modal.style.display = "block";
    sessionStorage.setItem("modalShown", "true");
  }

  closeButton.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target == modal) {
      modal.style.display = "none";
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
      // Parse markdown and handle line breaks
      const markdown = body.answer || body.message || "Sem resposta";
      const parsedContent = marked.parse(markdown);
      botDiv.querySelector("span").innerHTML = parsedContent;
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
