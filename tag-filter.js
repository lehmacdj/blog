// Tag Filter Layout Module
// Declarative positioning logic for tag filter controls
//
// Layout specification:
// - Order: selected tags → X (clear) button → unselected tags → >/< button
// - Selected tags always before unselected tags
// - X button appears after selected tags (only if any are selected)
// - X and >/< buttons are always visible
// - Collapsed: tags limited to one row, > at end of row
// - Expanded: all tags shown with wrapping, < at the very end

var TagFilterLayout = (function() {
  var ROW_HEIGHT = 30;

  // Sort comparator: by count descending, then alphabetically
  function compareByCountThenName(a, b) {
    var countDiff = parseInt(b.dataset.count) - parseInt(a.dataset.count);
    if (countDiff !== 0) return countDiff;
    return a.dataset.tag.localeCompare(b.dataset.tag);
  }

  function getTagButtons(container) {
    return Array.from(container.querySelectorAll('.tag-btn[data-tag]'));
  }

  function getVisibleTags(container) {
    return getTagButtons(container).filter(function(btn) {
      return !btn.classList.contains('filtered-out');
    });
  }

  function isOnFirstRow(element, firstRowBottom) {
    var rect = element.getBoundingClientRect();
    return rect.top < firstRowBottom;
  }

  /**
   * Rebuild DOM in correct order and handle collapsed state.
   */
  function reorderTags(opts) {
    var tagsContainer = opts.tagsContainer;
    var clearBtn = opts.clearBtn;
    var expandBtn = opts.expandBtn;

    var allBtns = getTagButtons(tagsContainer);

    // Separate and sort
    var activeBtns = allBtns
      .filter(function(btn) { return btn.classList.contains('active'); })
      .sort(compareByCountThenName);

    var inactiveBtns = allBtns
      .filter(function(btn) { return !btn.classList.contains('active'); })
      .sort(compareByCountThenName);

    var hasActiveTags = activeBtns.length > 0;

    // Update clear button visibility
    clearBtn.style.display = hasActiveTags ? '' : 'none';

    // Clear previous collapsed-hidden state
    allBtns.forEach(function(btn) {
      btn.classList.remove('collapsed-hidden');
    });

    // Build correct DOM order: selected → X → unselected → >
    var fragment = document.createDocumentFragment();
    activeBtns.forEach(function(btn) { fragment.appendChild(btn); });
    if (hasActiveTags) fragment.appendChild(clearBtn);
    inactiveBtns.forEach(function(btn) { fragment.appendChild(btn); });
    fragment.appendChild(expandBtn);
    tagsContainer.appendChild(fragment);

    // Handle collapsed state
    if (opts.sync) {
      layoutCollapsed(opts);
    } else {
      requestAnimationFrame(function() {
        layoutCollapsed(opts);
      });
    }
  }

  /**
   * When collapsed, hide tags that don't fit on the first row.
   * Always keeps X and > visible.
   */
  function layoutCollapsed(opts) {
    var container = opts.container;
    var tagsContainer = opts.tagsContainer;
    var expandBtn = opts.expandBtn;

    // Clear previous collapsed-hidden state
    var allTags = getTagButtons(tagsContainer);
    allTags.forEach(function(tag) {
      tag.classList.remove('collapsed-hidden');
    });

    // When expanded, show everything
    if (container.classList.contains('expanded')) {
      return;
    }

    // Force layout calculation
    void tagsContainer.offsetWidth;

    var containerRect = tagsContainer.getBoundingClientRect();
    var firstRowBottom = containerRect.top + ROW_HEIGHT;

    // Check if expand button is already on first row
    if (isOnFirstRow(expandBtn, firstRowBottom)) {
      return; // Everything fits
    }

    // Get visible tags (not filtered out) to potentially hide
    var visibleTags = getVisibleTags(tagsContainer);

    // Hide tags from the end until > fits on first row
    // Since DOM order is [selected] [X] [unselected] [>],
    // working backwards hides unselected first, then selected
    for (var i = visibleTags.length - 1; i >= 0; i--) {
      visibleTags[i].classList.add('collapsed-hidden');

      // Force reflow and check
      void tagsContainer.offsetWidth;
      if (isOnFirstRow(expandBtn, firstRowBottom)) {
        break;
      }
    }
  }

  /**
   * Position controls for current state.
   * Called after DOM changes or resize.
   */
  function positionControls(opts) {
    layoutCollapsed(opts);
  }

  return {
    ROW_HEIGHT: ROW_HEIGHT,
    positionControls: positionControls,
    reorderTags: reorderTags,
    compareByCountThenName: compareByCountThenName
  };
})();

// Export for testing (Node.js/CommonJS environments)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TagFilterLayout;
}
