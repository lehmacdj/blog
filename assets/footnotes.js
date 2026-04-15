(function () {
  'use strict';

  var refs = document.querySelectorAll('sup[id^="fnref:"] a.footnote');
  if (!refs.length) return;

  var hoverCapable = window.matchMedia('(hover: hover)').matches;

  var popup = document.createElement('div');
  popup.className = 'footnote-popup';
  popup.setAttribute('role', 'tooltip');
  document.body.appendChild(popup);

  var hideTimer = null;
  var currentTrigger = null;

  function clearHideTimer() {
    if (hideTimer) {
      clearTimeout(hideTimer);
      hideTimer = null;
    }
  }

  function scheduleHide() {
    clearHideTimer();
    hideTimer = setTimeout(hidePopup, 180);
  }

  function hidePopup() {
    clearHideTimer();
    popup.classList.remove('is-visible');
    currentTrigger = null;
  }

  function getFootnoteContent(href) {
    var id = href.replace(/^.*#/, '');
    var li = document.getElementById(id);
    if (!li) return null;
    var clone = li.cloneNode(true);
    return clone.innerHTML;
  }

  function positionPopup(trigger) {
    // Reset to measure natural size.
    popup.style.left = '0px';
    popup.style.top = '0px';
    popup.style.maxHeight = '';

    var rect = trigger.getBoundingClientRect();
    var scrollX = window.pageXOffset;
    var scrollY = window.pageYOffset;
    var vw = document.documentElement.clientWidth;
    var vh = document.documentElement.clientHeight;
    var margin = 8;

    var pw = popup.offsetWidth;
    var ph = popup.offsetHeight;

    // Horizontal: align popup's left edge with trigger's left edge;
    // if that overflows to the right, align popup's right edge with
    // trigger's right edge instead.
    var left = rect.left;
    if (left + pw > vw - margin) {
      left = rect.right - pw;
    }
    if (left < margin) left = margin;

    // Vertical: prefer below; flip above if not enough space.
    var spaceBelow = vh - rect.bottom;
    var top;
    if (spaceBelow >= ph + margin || spaceBelow >= vh - rect.top) {
      top = rect.bottom + 6;
    } else {
      top = rect.top - ph - 6;
      if (top < margin) top = margin;
    }

    popup.style.left = (left + scrollX) + 'px';
    popup.style.top = (top + scrollY) + 'px';
  }

  function showPopup(trigger) {
    clearHideTimer();
    var href = trigger.getAttribute('href');
    var content = getFootnoteContent(href);
    if (!content) return;

    popup.innerHTML = content;

    currentTrigger = trigger;
    popup.classList.add('is-visible');
    positionPopup(trigger);
  }

  // Attach handlers per trigger.
  refs.forEach(function (ref) {
    if (hoverCapable) {
      ref.addEventListener('mouseenter', function () {
        showPopup(ref);
      });
      ref.addEventListener('mouseleave', scheduleHide);
      ref.addEventListener('focus', function () { showPopup(ref); });
      ref.addEventListener('blur', scheduleHide);
      // Click falls through to native behavior (jump to footnote).
    } else {
      ref.addEventListener('click', function (e) {
        e.preventDefault();
        if (currentTrigger === ref) {
          hidePopup();
        } else {
          showPopup(ref);
        }
      });
    }
  });

  if (hoverCapable) {
    popup.addEventListener('mouseenter', clearHideTimer);
    popup.addEventListener('mouseleave', scheduleHide);
  } else {
    // Tap outside dismisses.
    document.addEventListener('click', function (e) {
      if (!popup.classList.contains('is-visible')) return;
      if (popup.contains(e.target)) return;
      if (e.target.closest && e.target.closest('sup[id^="fnref:"] a.footnote')) return;
      hidePopup();
    }, true);
  }

  window.addEventListener('resize', function () {
    if (currentTrigger) positionPopup(currentTrigger);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') hidePopup();
  });

  // Center the target in the viewport for footnote jumps (both directions).
  function centerScroll(e) {
    if (e.defaultPrevented) return;
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) !== '#') return;
    if (!(a.classList.contains('footnote') ||
          a.classList.contains('reversefootnote'))) return;
    var target = document.getElementById(href.slice(1));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ block: 'center', behavior: 'smooth' });
    history.pushState(null, '', href);
  }
  document.addEventListener('click', centerScroll);
})();
