// Main JavaScript for IPO Listing Page

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the page
    initPage();

    // Set up event listeners
    setupEventListeners();
});

// Initialize the page with IPO listings
function initPage() {
    // Show loading state
    showLoadingState();
    
    // Simulate API call delay
    setTimeout(() => {
        // Render IPO cards with default sorting (open date ascending)
        renderIPOCards(ipoData);
        
        // Hide loading state
        hideLoadingState();
    }, 800);
}

// Set up event listeners for filtering and sorting
function setupEventListeners() {
    // Sort dropdown change event
    document.getElementById('sort-by').addEventListener('change', function() {
        applyFiltersAndSort();
    });
    
    // Filter dropdowns change events
    document.getElementById('issue-type').addEventListener('change', function() {
        applyFiltersAndSort();
    });
    
    document.getElementById('price-range').addEventListener('change', function() {
        applyFiltersAndSort();
    });
    
    document.getElementById('issue-size').addEventListener('change', function() {
        applyFiltersAndSort();
    });
}

// Apply filters and sorting to IPO data
function applyFiltersAndSort() {
    // Show loading state
    showLoadingState();
    
    // Get filter values
    const issueType = document.getElementById('issue-type').value;
    const priceRange = document.getElementById('price-range').value;
    const issueSize = document.getElementById('issue-size').value;
    const sortBy = document.getElementById('sort-by').value;
    
    // Filter the data
    let filteredData = filterIPOData(ipoData, issueType, priceRange, issueSize);
    
    // Sort the filtered data
    filteredData = sortIPOData(filteredData, sortBy);
    
    // Simulate API call delay
    setTimeout(() => {
        // Render the filtered and sorted IPO cards
        renderIPOCards(filteredData);
        
        // Hide loading state
        hideLoadingState();
    }, 400);
}

// Filter IPO data based on selected filters
function filterIPOData(data, issueType, priceRange, issueSize) {
    return data.filter(ipo => {
        // Filter by issue type
        if (issueType !== 'all' && ipo.issueType.toLowerCase() !== issueType.replace('-', ' ')) {
            return false;
        }
        
        // Filter by price range
        if (priceRange !== 'all' && ipo.priceBand !== 'Not Issued') {
            const price = extractMaxPrice(ipo.priceBand);
            
            if (priceRange === '0-100' && (price < 0 || price > 100)) return false;
            if (priceRange === '101-500' && (price < 101 || price > 500)) return false;
            if (priceRange === '501-1000' && (price < 501 || price > 1000)) return false;
            if (priceRange === '1001+' && price < 1001) return false;
        }
        
        // Filter by issue size
        if (issueSize !== 'all' && ipo.issueSize !== 'Not Issued') {
            const size = extractIssueSize(ipo.issueSize);
            
            if (issueSize === 'small' && size >= 100) return false;
            if (issueSize === 'medium' && (size < 100 || size > 500)) return false;
            if (issueSize === 'large' && size <= 500) return false;
        }
        
        return true;
    });
}

// Sort IPO data based on selected sort option
function sortIPOData(data, sortBy) {
    const sortedData = [...data];
    
    switch (sortBy) {
        case 'open-date-asc':
            sortedData.sort((a, b) => {
                if (a.openDate === 'Not Issued') return 1;
                if (b.openDate === 'Not Issued') return -1;
                return new Date(a.openDate) - new Date(b.openDate);
            });
            break;
            
        case 'open-date-desc':
            sortedData.sort((a, b) => {
                if (a.openDate === 'Not Issued') return 1;
                if (b.openDate === 'Not Issued') return -1;
                return new Date(b.openDate) - new Date(a.openDate);
            });
            break;
            
        case 'price-asc':
            sortedData.sort((a, b) => {
                if (a.priceBand === 'Not Issued') return 1;
                if (b.priceBand === 'Not Issued') return -1;
                return extractMaxPrice(a.priceBand) - extractMaxPrice(b.priceBand);
            });
            break;
            
        case 'price-desc':
            sortedData.sort((a, b) => {
                if (a.priceBand === 'Not Issued') return 1;
                if (b.priceBand === 'Not Issued') return -1;
                return extractMaxPrice(b.priceBand) - extractMaxPrice(a.priceBand);
            });
            break;
            
        case 'issue-size-asc':
            sortedData.sort((a, b) => {
                if (a.issueSize === 'Not Issued') return 1;
                if (b.issueSize === 'Not Issued') return -1;
                return extractIssueSize(a.issueSize) - extractIssueSize(b.issueSize);
            });
            break;
            
        case 'issue-size-desc':
            sortedData.sort((a, b) => {
                if (a.issueSize === 'Not Issued') return 1;
                if (b.issueSize === 'Not Issued') return -1;
                return extractIssueSize(b.issueSize) - extractIssueSize(a.issueSize);
            });
            break;
    }
    
    return sortedData;
}

// Render IPO cards to the DOM
function renderIPOCards(data) {
    const container = document.getElementById('ipo-listings');
    const template = document.getElementById('ipo-card-template');
    
    // Clear existing cards
    container.innerHTML = '';
    
    // Check if there are no results
    if (data.length === 0) {
        showEmptyState();
        return;
    }
    
    // Render each IPO card
    data.forEach((ipo, index) => {
        // Clone the template
        const card = document.importNode(template.content, true);
        
        // Set company logo and name
        card.querySelector('.company-logo').src = ipo.logo;
        card.querySelector('.company-name').textContent = ipo.name;
        
        // Set IPO details
        card.querySelector('.price-band').textContent = ipo.priceBand;
        card.querySelector('.open-date').textContent = formatDate(ipo.openDate);
        card.querySelector('.close-date').textContent = formatDate(ipo.closeDate);
        card.querySelector('.issue-size').textContent = ipo.issueSize;
        card.querySelector('.issue-type').textContent = ipo.issueType;
        card.querySelector('.listing-date').textContent = formatDate(ipo.listingDate);
        
        // Add animation delay based on index
        const cardElement = card.querySelector('.col-lg-4');
        cardElement.classList.add('fade-in');
        cardElement.style.animationDelay = `${index * 0.1}s`;
        
        // Append the card to the container
        container.appendChild(card);
    });
}

// Show loading state
function showLoadingState() {
    const container = document.getElementById('ipo-listings');
    container.innerHTML = `
        <div class="col-12 loading-spinner">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
}

// Hide loading state
function hideLoadingState() {
    // Loading state is automatically removed when cards are rendered
}

// Show empty state when no results are found
function showEmptyState() {
    const container = document.getElementById('ipo-listings');
    container.innerHTML = `
        <div class="col-12">
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h4>No IPOs Found</h4>
                <p class="text-muted">No IPOs match your current filter criteria. Try adjusting your filters.</p>
                <button class="btn btn-outline-primary mt-3" onclick="resetFilters()">Reset Filters</button>
            </div>
        </div>
    `;
}

// Reset all filters to default values
function resetFilters() {
    document.getElementById('issue-type').value = 'all';
    document.getElementById('price-range').value = 'all';
    document.getElementById('issue-size').value = 'all';
    document.getElementById('sort-by').value = 'open-date-asc';
    
    // Apply the reset filters
    applyFiltersAndSort();
}

// Helper function to extract maximum price from price band
function extractMaxPrice(priceBand) {
    if (priceBand === 'Not Issued') return -1;
    
    const matches = priceBand.match(/\d+/g);
    if (!matches || matches.length < 2) return -1;
    
    return parseInt(matches[1], 10);
}

// Helper function to extract issue size in crores
function extractIssueSize(issueSize) {
    if (issueSize === 'Not Issued') return -1;
    
    const matches = issueSize.match(/[\d,]+/);
    if (!matches) return -1;
    
    return parseFloat(matches[0].replace(/,/g, ''));
}

// Helper function to format date
function formatDate(dateStr) {
    if (dateStr === 'Not Issued') return dateStr;
    
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).replace(/\//g, '-');
}
