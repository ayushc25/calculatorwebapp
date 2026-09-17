/* ==========================================================================
   guide.js — progressive enhancement for the educational article below each
   calculator. Independent of engine.js / app.js: it touches nothing the
   calculator uses, and the page works without it.

   The article's sections are collapsed <details> blocks. Their headings carry
   ids, so a search result, a shared link or an in-page anchor can point at a
   section that happens to be closed. Without this, following such a link
   scrolls to a collapsed block and the visitor sees nothing.
   ========================================================================== */
(function () {
  'use strict';

  /* The heading is inside <summary>, so climb to the <details> that owns it. */
  function foldFor(el) {
    return el && el.closest ? el.closest('details.guide-section, details.faq-item') : null;
  }

  function reveal(hash, smooth) {
    if (!hash || hash.length < 2) return false;

    var target;
    try {
      target = document.querySelector(hash);
    } catch (e) {
      return false;               /* not a usable selector, e.g. "#" */
    }
    if (!target) return false;

    var fold = foldFor(target);
    if (fold && !fold.open) fold.open = true;

    /* scroll-margin-top in the stylesheet keeps this clear of the header. */
    if (smooth) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    return true;
  }

  /* Landing directly on /calculators/bmi/#different-populations. The browser
     has already tried to scroll, before the section was open, so re-run the
     scroll once the fold is expanded. */
  function onLoad() {
    if (window.location.hash) {
      /* rAF so the open state is applied before we measure where to scroll */
      window.requestAnimationFrame(function () {
        reveal(window.location.hash, true);
      });
    }
  }

  /* Any in-page link, including ones added later. */
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest ? ev.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var hash = a.getAttribute('href');
    if (!hash || hash === '#') return;
    if (reveal(hash, true)) {
      ev.preventDefault();
      if (window.history && window.history.pushState) {
        window.history.pushState(null, '', hash);
      }
    }
  });

  window.addEventListener('hashchange', function () {
    reveal(window.location.hash, true);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onLoad);
  } else {
    onLoad();
  }
})();
