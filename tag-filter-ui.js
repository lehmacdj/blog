(function() {
  // DOM elements
  var container = document.querySelector('.tag-filter-container');
  var tagsContainer = document.querySelector('.tag-filter-tags');
  var tagButtons = document.querySelectorAll(
    '.tag-filter-tags .tag-btn[data-tag]'
  );
  var clearBtn = document.querySelector('.tag-clear-btn');
  var posts = document.querySelectorAll('.post-list li');
  var searchInput = document.querySelector('.tag-search');
  var searchClearBtn = document.querySelector('.tag-search-clear');
  var expandBtn = document.querySelector('.tag-expand-btn');

  // Layout options for TagFilterLayout
  var layoutOpts = {
    container: container,
    tagsContainer: tagsContainer,
    clearBtn: clearBtn,
    expandBtn: expandBtn
  };

  function getActiveTags() {
    return Array.from(tagButtons)
      .filter(function(btn) {
        return btn.classList.contains('active');
      })
      .map(function(btn) { return btn.dataset.tag; });
  }

  function isDefaultState(tags) {
    return tags.length === 1 && tags[0] === 'recommended';
  }

  function tagPageUrl(tag) {
    return '/tags/' + encodeURIComponent(tag) + '/';
  }

  function updateUrl() {
    var activeTags = getActiveTags();

    if (isDefaultState(activeTags)) {
      // Default state: bare index path
      history.replaceState(null, '', '/');
      return;
    }

    if (activeTags.length === 1) {
      // Single tag: use /tags/X/ for rich link previews
      history.replaceState(null, '', tagPageUrl(activeTags[0]));
      return;
    }

    // /everything means "no filter, show all" — distinct from
    // bare / which keeps the default 'recommended' tag active.
    if (activeTags.length === 0) {
      history.replaceState(null, '', '/everything');
    } else {
      var search = '?tags=' + activeTags.join('+');
      history.replaceState(null, '', '/' + search);
    }
  }

  var rssTagLinks = document.querySelectorAll('.rss-tag-link');

  function updateRssLinks(activeTags) {
    rssTagLinks.forEach(function(link) {
      link.classList.toggle(
        'visible', activeTags.includes(link.dataset.tag)
      );
    });
  }

  function filterPosts() {
    var activeTags = getActiveTags();
    posts.forEach(function(post) {
      var postTags = (post.dataset.tags || '').split(' ');
      var isVisible = activeTags.length === 0 ||
        activeTags.every(function(tag) {
          return postTags.includes(tag);
        });
      post.classList.toggle('hidden', !isVisible);
    });
    updateRssLinks(activeTags);
    updateUrl();
    TagFilterLayout.reorderTags(layoutOpts);
  }

  function filterTags(query) {
    var q = query.toLowerCase().trim();
    var hasQuery = q.length > 0;

    tagButtons.forEach(function(btn) {
      var matchesQuery = btn.dataset.tag.toLowerCase().includes(q);
      btn.classList.toggle('filtered-out', hasQuery && !matchesQuery);
    });

    // Hide tag clear button during search to avoid confusion
    clearBtn.classList.toggle('filtered-out', hasQuery);
    searchClearBtn.style.display = hasQuery ? '' : 'none';

    requestAnimationFrame(function() {
      TagFilterLayout.positionControls(layoutOpts);
    });
  }

  function initFromUrl() {
    var path = window.location.pathname.replace(/\/$/, '');

    // /everything — show all posts, no tags active
    if (path === '/everything') {
      tagButtons.forEach(function(btn) {
        btn.classList.remove('active');
      });
      return;
    }

    // /tags/{tag} — single tag active
    var tagMatch = path.match(/^\/tags\/([^/]+)$/);
    if (tagMatch) {
      var urlTag = decodeURIComponent(tagMatch[1]);
      tagButtons.forEach(function(btn) {
        btn.classList.toggle('active', btn.dataset.tag === urlTag);
      });
      return;
    }

    // ?tags= query param (legacy / multi-tag)
    var params = new URLSearchParams(window.location.search);
    if (!params.has('tags')) {
      return;  // No param: keep template default (recommended)
    }

    var tagsParam = params.get('tags');
    var urlTags = tagsParam ? tagsParam.split(' ') : [];

    tagButtons.forEach(function(btn) {
      btn.classList.toggle(
        'active', urlTags.includes(btn.dataset.tag)
      );
    });
  }

  // Event listeners
  tagButtons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      btn.classList.toggle('active');
      filterPosts();
    });
  });

  clearBtn.addEventListener('click', function() {
    tagButtons.forEach(function(btn) {
      btn.classList.remove('active');
    });
    filterPosts();
  });

  searchInput.addEventListener('input', function(e) {
    filterTags(e.target.value);
    if (e.target.value.trim()) {
      container.classList.add('expanded');
    }
  });

  searchClearBtn.addEventListener('click', function() {
    searchInput.value = '';
    filterTags('');
    searchInput.focus();
  });

  expandBtn.addEventListener('click', function() {
    container.classList.toggle('expanded');
    requestAnimationFrame(function() {
      TagFilterLayout.positionControls(layoutOpts);
    });
  });

  window.addEventListener('resize', function() {
    requestAnimationFrame(function() {
      TagFilterLayout.positionControls(layoutOpts);
    });
  });

  // Initialize
  initFromUrl();
  filterPosts();
})();
