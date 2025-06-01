let id = "";

function sendMessage() {
  const inputField = document.getElementById("input");
  let input = inputField.value.trim();
  input != "" && output(input);
  inputField.value = "";
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded");
  const inputField = document.getElementById("input");
  inputField.addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
      let input = inputField.value.trim();
      input != "" && output(input);
      inputField.value = "";
    }
  });
});

function output(input) {
  addChat(input, "...", true);
  fetch(`${API_URL}/api/v1/chatbot`, {
    method: "post",
    body: JSON.stringify({ question: input, session_id: id }),
  })
    .then((response) => {
      return response.json();
    })
    .then((body) => {
      console.log(body);
      removeDots();

      if (!id) {
        id = body["session_id"];
      }

      addChat(null, body["message"].replace(/\n/g, "<br>"));
      addChat(null, "Em caso de duvida contatar o responsável técnico");
    })
    .catch((error) => {
      console.error(error);
      removeDots();
      addChat(
        null,
        "Parece ter um erro no Servidor!\nPor favor, entre em contato com o responsável técnico"
      );
    });
  return;
}

function addChat(input, product, loading) {
  const mainDiv = document.getElementById("message-section");

  if (input) {
    let userDiv = document.createElement("div");
    userDiv.id = "user";
    userDiv.classList.add("message");
    userDiv.innerHTML = `<span id="user-response">${input}</span>`;
    mainDiv.appendChild(userDiv);
  }

  if (product) {
    let botDiv = document.createElement("div");
    botDiv.id = "bot";
    botDiv.classList.add("message");
    botDiv.innerHTML = `<span id="bot-response">${product}</span>`;
    mainDiv.appendChild(botDiv);

    if (loading) {
      const dotsSpan = botDiv.querySelector("#bot-response");
      dotsSpan.classList.add("loading");
    }
  }

  scrollChat();
}

function removeDots() {
  const messages = document.querySelectorAll(".message");

  messages.forEach((message) => {
    const messageContent = message.querySelector("span").textContent;
    if (messageContent.endsWith("...")) {
      message.remove();
    }
  });
}

function scrollChat() {
  const scroll = document.getElementById("message-section");
  const offsetPercentage = 40;
  const windowHeight = window.innerHeight;
  const offsetPixels = (windowHeight * offsetPercentage) / 100;

  window.scrollTo(0, scroll.scrollHeight);
  window.scrollBy(0, -offsetPixels);
}
