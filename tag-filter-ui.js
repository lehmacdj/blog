(function() {
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
  var rssTagLinks = document.querySelectorAll('.rss-tag-link');

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
    return '/tagged/' + encodeURIComponent(tag) + '/';
  }

  function updateUrl(activeTags) {
    if (isDefaultState(activeTags)) {
      history.replaceState(null, '', '/');
      return;
    }

    if (activeTags.length === 1) {
      history.replaceState(null, '', tagPageUrl(activeTags[0]));
      return;
    }

    // /everything means "no filter, show all" — distinct from
    // bare / which keeps the default 'recommended' tag active.
    if (activeTags.length === 0) {
      history.replaceState(null, '', '/everything');
    } else {
      history.replaceState(
        null, '', '/?tags=' + activeTags.join('+')
      );
    }
  }

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
    updateUrl(activeTags);
    TagFilterLayout.reorderTags(layoutOpts);
  }

  function filterTags(query) {
    var q = query.toLowerCase().trim();
    var hasQuery = q.length > 0;

    tagButtons.forEach(function(btn) {
      var matchesQuery = btn.dataset.tag.toLowerCase().includes(q);
      btn.classList.toggle('filtered-out', hasQuery && !matchesQuery);
    });

    clearBtn.classList.toggle('filtered-out', hasQuery);
    searchClearBtn.style.display = hasQuery ? '' : 'none';

    requestAnimationFrame(function() {
      TagFilterLayout.positionControls(layoutOpts);
    });
  }

  function initFromUrl() {
    var path = window.location.pathname.replace(/\/$/, '');

    if (path === '/everything') {
      tagButtons.forEach(function(btn) {
        btn.classList.remove('active');
      });
      return;
    }

    var tagMatch = path.match(/^\/tagged\/([^/]+)$/);
    if (tagMatch) {
      var urlTag = decodeURIComponent(tagMatch[1]);
      tagButtons.forEach(function(btn) {
        btn.classList.toggle('active', btn.dataset.tag === urlTag);
      });
      return;
    }

    var params = new URLSearchParams(window.location.search);
    if (!params.has('tags')) {
      return;
    }

    var tagsParam = params.get('tags');
    var urlTags = tagsParam ? tagsParam.split(' ') : [];

    tagButtons.forEach(function(btn) {
      btn.classList.toggle(
        'active', urlTags.includes(btn.dataset.tag)
      );
    });
  }

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

  initFromUrl();
  filterPosts();
})();
