/**
 * DS Tools Database - Search and Filter Functionality
 * Uses Fuse.js for fuzzy search
 */

document.addEventListener('DOMContentLoaded', function() {
  // Get elements
  const searchInput = document.getElementById('search-input');
  const filterButtons = document.querySelectorAll('.filter-btn');
  const clearFiltersBtn = document.getElementById('clear-filters');
  const toolsGrid = document.getElementById('tools-grid');
  const toolCards = document.querySelectorAll('.tool-card');
  const resultsCount = document.getElementById('results-count');
  const noResults = document.getElementById('no-results');

  // Get tools data from embedded JSON
  const toolsDataEl = document.getElementById('tools-data');
  const toolsData = toolsDataEl ? JSON.parse(toolsDataEl.textContent) : [];

  // Current state
  let currentCategory = 'all';
  let currentSearch = '';

  // Initialize Fuse.js for fuzzy search
  const fuse = new Fuse(toolsData, {
    keys: [
      { name: 'name', weight: 2 },
      { name: 'description', weight: 1 },
      { name: 'categories', weight: 0.5 }
    ],
    threshold: 0.3,
    ignoreLocation: true,
    includeScore: true
  });

  // Debounce function for search input
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Filter and display tools
  function filterTools() {
    let visibleCount = 0;
    let matchingIds = new Set();

    // If there's a search query, use Fuse.js
    if (currentSearch.trim()) {
      const results = fuse.search(currentSearch);
      results.forEach(result => matchingIds.add(result.item.id));
    }

    toolCards.forEach(card => {
      const cardCategories = card.dataset.categories.split(',').map(c => c.trim());
      const cardName = card.dataset.name.toLowerCase();
      const cardDescription = (card.dataset.description || '').toLowerCase();

      // Check category filter
      const categoryMatch = currentCategory === 'all' || cardCategories.includes(currentCategory);

      // Check search filter
      let searchMatch = true;
      if (currentSearch.trim()) {
        // Use Fuse.js results if available, otherwise fallback to simple search
        if (matchingIds.size > 0) {
          // Find the tool's ID from the data
          const tool = toolsData.find(t => t.name === card.dataset.name);
          searchMatch = tool && matchingIds.has(tool.id);
        } else {
          // Simple search fallback
          const searchLower = currentSearch.toLowerCase();
          searchMatch = cardName.includes(searchLower) || cardDescription.includes(searchLower);
        }
      }

      // Show/hide card
      if (categoryMatch && searchMatch) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    // Update results count
    updateResultsCount(visibleCount);

    // Show/hide no results message
    if (visibleCount === 0) {
      noResults.style.display = 'block';
      toolsGrid.style.display = 'none';
    } else {
      noResults.style.display = 'none';
      toolsGrid.style.display = 'grid';
    }

    // Show/hide clear filters button
    if (currentCategory !== 'all' || currentSearch.trim()) {
      clearFiltersBtn.style.display = 'block';
    } else {
      clearFiltersBtn.style.display = 'none';
    }
  }

  // Update results count text
  function updateResultsCount(count) {
    const categoryText = currentCategory === 'all' ? '' : ` in "${currentCategory}"`;
    const searchText = currentSearch.trim() ? ` matching "${currentSearch}"` : '';
    resultsCount.textContent = `Showing ${count} tool${count !== 1 ? 's' : ''}${categoryText}${searchText}`;
  }

  // Handle search input
  const handleSearch = debounce(function(e) {
    currentSearch = e.target.value;
    filterTools();
  }, 200);

  searchInput.addEventListener('input', handleSearch);

  // Handle category filter clicks
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Update active state
      filterButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');

      // Update current category
      currentCategory = this.dataset.category;
      filterTools();
    });
  });

  // Handle clear filters
  clearFiltersBtn.addEventListener('click', function() {
    currentCategory = 'all';
    currentSearch = '';
    searchInput.value = '';

    filterButtons.forEach(btn => {
      btn.classList.remove('active');
      if (btn.dataset.category === 'all') {
        btn.classList.add('active');
      }
    });

    filterTools();
  });

  // Handle category tag clicks within cards
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('category-tag')) {
      const category = e.target.textContent;
      const targetButton = document.querySelector(`.filter-btn[data-category="${category}"]`);

      if (targetButton) {
        filterButtons.forEach(btn => btn.classList.remove('active'));
        targetButton.classList.add('active');
        currentCategory = category;
        filterTools();

        // Scroll to top of filters
        document.querySelector('.filters-section').scrollIntoView({ behavior: 'smooth' });
      }
    }
  });

  // Initialize
  filterTools();
});
