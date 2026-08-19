/* Yorug'/qorong'i rejim almashtirgichi.
   Tanlov localStorage'da saqlanadi; tanlov bo'lmasa tizim sozlamasi olinadi. */
(function () {
  "use strict";

  var root = document.documentElement;
  var media = window.matchMedia("(prefers-color-scheme: dark)");

  function stored() {
    try {
      return localStorage.getItem("theme");
    } catch (e) {
      return null;
    }
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    var btn = document.getElementById("theme-toggle");
    if (btn) {
      btn.setAttribute("aria-pressed", String(theme === "dark"));
      btn.setAttribute(
        "aria-label",
        theme === "dark"
          ? "Yorug' rejimga o'tish"
          : "Qorong'i rejimga o'tish"
      );
    }
  }

  function current() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  document.addEventListener("DOMContentLoaded", function () {
    apply(current());

    var btn = document.getElementById("theme-toggle");
    if (!btn) return;

    btn.hidden = false;
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      try {
        localStorage.setItem("theme", next);
      } catch (e) {
        /* saqlab bo'lmasa ham rejim almashaveradi */
      }
      apply(next);
    });
  });

  // Foydalanuvchi qo'lda tanlamagan bo'lsa, tizim rejimi o'zgarsa ergashadi.
  media.addEventListener("change", function (event) {
    if (!stored()) apply(event.matches ? "dark" : "light");
  });
})();
