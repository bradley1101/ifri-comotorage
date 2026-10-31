/* Instant messaging: send with fetch, poll new messages every 3 s. */
(function () {
  const form = document.getElementById("chat-form");
  if (!form) return;
  const body = document.getElementById("chat-body");
  const input = form.querySelector("input[name=contenu]");
  const csrf = form.querySelector("input[name=csrfmiddlewaretoken]").value;
  let last = parseInt(form.dataset.last || "0", 10);

  const scroll = () => { body.scrollTop = body.scrollHeight; };
  function add(m) {
    if (m.id <= last && body.querySelector(`[data-id="${m.id}"]`)) return;
    document.getElementById("chat-empty")?.remove();
    const div = document.createElement("div");
    div.className = "bubble" + (m.moi ? " me" : "");
    div.dataset.id = m.id;
    div.textContent = m.contenu;
    const t = document.createElement("time");
    t.textContent = new Date(m.heure).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
    div.appendChild(t);
    body.appendChild(div);
    last = Math.max(last, m.id);
    scroll();
  }

  form.addEventListener("submit", async e => {
    e.preventDefault();
    const contenu = input.value.trim();
    if (!contenu) return;
    input.value = "";
    const r = await fetch(form.dataset.send, { method: "POST", headers: { "X-CSRFToken": csrf },
      body: new URLSearchParams({ contenu }) });
    if (r.ok) add((await r.json()).message);
  });

  async function poll() {
    try {
      const r = await fetch(`${form.dataset.poll}?after=${last}`);
      if (r.ok) (await r.json()).messages.forEach(add);
    } catch (_) { /* offline: retry next tick */ }
  }
  scroll();
  setInterval(poll, 3000);
})();
