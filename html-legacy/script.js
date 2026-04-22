/* ── Nav toggle ── */
const menuButton = document.getElementById("menu-button");
const navPanel   = document.getElementById("nav-panel");

if (menuButton && navPanel) {
  menuButton.addEventListener("click", () => {
    const expanded = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!expanded));
    navPanel.classList.toggle("is-open");
  });

  navPanel.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menuButton.setAttribute("aria-expanded", "false");
      navPanel.classList.remove("is-open");
    });
  });
}

