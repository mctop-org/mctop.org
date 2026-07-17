// Copy buttons and the theme toggle. Dark is the default; light is opt-in and
// remembered. The initial theme is set inline in <head> to avoid a flash.
(() => {
  document.querySelectorAll(".copy").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(btn.dataset.cmd);
        const label = btn.textContent;
        btn.textContent = "Copied"; btn.classList.add("ok");
        setTimeout(() => { btn.textContent = label; btn.classList.remove("ok"); }, 1500);
      } catch { btn.textContent = "Ctrl+C"; }
    });
  });
  const root = document.documentElement;
  const themeBtn = document.getElementById("theme");
  const syncPressed = () =>
    themeBtn?.setAttribute("aria-pressed", root.getAttribute("data-theme") === "light" ? "true" : "false");
  syncPressed();
  themeBtn?.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", next);
    localStorage.setItem("mctop-theme", next);
    syncPressed();
  });
})();
