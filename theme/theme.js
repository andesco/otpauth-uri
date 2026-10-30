(function () {
  const root = document.documentElement;
  let preferredTheme = null;

  try {
    preferredTheme = localStorage.getItem("theme");
  } catch (error) {
    preferredTheme = null;
  }

  const isDark = preferredTheme
    ? preferredTheme === "dark"
    : window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;

  root.classList.toggle("dark", isDark);
  root.setAttribute("data-theme", isDark ? "dark" : "light");
})();
