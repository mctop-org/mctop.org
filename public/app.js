// copy buttons + persisted theme toggle. No animation; this is a text document.
(() => {
  document.querySelectorAll(".copy").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.cmd);
        const t = btn.textContent;
        btn.textContent = "copied"; btn.classList.add("ok");
        setTimeout(() => { btn.textContent = t; btn.classList.remove("ok"); }, 1500);
      } catch { btn.textContent = "ctrl+c"; }
    });
  });
  const root = document.documentElement;
  const saved = localStorage.getItem("mctop-theme");
  if (saved) root.setAttribute("data-theme", saved);
  document.getElementById("theme")?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    localStorage.setItem("mctop-theme", next);
  });
})();
