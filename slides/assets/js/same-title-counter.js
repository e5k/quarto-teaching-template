(function () {
  function getTitle(slide) {
    const h = slide.querySelector("h1, h2, h3");
    return h ? h.textContent.trim() : null;
  }

  function update() {
    if (!window.Reveal) return;

    // Only real slides (not stack containers, not hidden)
    const slides = Array.from(
      document.querySelectorAll(".reveal .slides section")
    ).filter(s =>
      !s.classList.contains("stack") &&
      s.offsetParent !== null   // filters out display:none (.hide-slide)
    );

    // Group slides by title
    const groups = {};
    slides.forEach(slide => {
      const title = getTitle(slide);
      if (!title) return;
      (groups[title] ||= []).push(slide);
    });

    // Rewrite titles as "Title (i/n)"
    Object.entries(groups).forEach(([title, group]) => {
      if (group.length < 2) return;

      group.forEach((slide, i) => {
        const h = slide.querySelector("h1, h2, h3");
        if (!h) return;
        h.textContent = `${title} (${i + 1}/${group.length})`;
      });
    });
  }

  function boot() {
    if (!window.Reveal) return setTimeout(boot, 50);
    Reveal.on("ready", update);
    update();
  }

  boot();
})();
