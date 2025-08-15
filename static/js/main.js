const domains = [
    "https://kashmirobserver.net",
    "https://thekashmiriyat.co.uk",
    "https://kashmirnews.in",
    "https://kashmirdespatch.com",
    "https://kashmirlife.net",
    "https://risingkashmir.com",
    "https://greaterkashmir.com",
    "https://asiannewshub.com",
    "https://thekashmirmonitor.net",
    "https://kashmirreader.com",
    "https://kashmirtimes.com",
    "https://newsvibesofindia.com",
    "https://kashmirvision.in"
];

function createLink(rel, href, crossorigin = false) {
    const link = document.createElement("link");
    link.rel = rel;
    link.href = href;
    if (crossorigin) {
        link.crossOrigin = "anonymous";
    }
    document.head.appendChild(link);
}

// Preconnect to news domains for better performance
domains.forEach(domain => {
    createLink("preconnect", domain, true);
    createLink("dns-prefetch", domain);
});

// News API functionality
class NewsAPI {
    constructor() {
        this.baseURL = '/api/news';
        this.categoriesURL = '/api/news/categories';
        this.filterMap = {
            'hour': 'rf',
            'day': 'dn',
            'week': 'wn',
            'month': 'mn',
            'year': 'yn'
        };
        this.isLoading = {};
        this.cache = {};
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    async fetchNews(category) {
        if (this.isLoading[category]) {
            return null; // Already loading
        }

        // Check cache first
        const cached = this.getCachedNews(category);
        if (cached) {
            return cached;
        }

        this.isLoading[category] = true;

        try {
            const filter = this.filterMap[category];
            const response = await fetch(`${this.baseURL}?filter=${filter}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Cache the result
                this.cacheNews(category, data.data);
                return data.data;
            } else {
                throw new Error(data.message || 'Failed to fetch news');
            }
        } catch (error) {
            console.error(`Error fetching news for ${category}:`, error);
            throw error;
        } finally {
            this.isLoading[category] = false;
        }
    }

    async fetchAllCategories() {
        try {
            const response = await fetch(this.categoriesURL);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Cache all categories
                Object.keys(data.categories).forEach(category => {
                    this.cacheNews(category, data.categories[category].data);
                });
                return data.categories;
            } else {
                throw new Error(data.message || 'Failed to fetch news categories');
            }
        } catch (error) {
            console.error('Error fetching all categories:', error);
            throw error;
        }
    }

    cacheNews(category, data) {
        this.cache[category] = {
            data: data,
            timestamp: Date.now()
        };
    }

    getCachedNews(category) {
        const cached = this.cache[category];
        if (cached && (Date.now() - cached.timestamp) < this.cacheTimeout) {
            return cached.data;
        }
        return null;
    }

    clearCache(category = null) {
        if (category) {
            delete this.cache[category];
        } else {
            this.cache = {};
        }
    }

    isCached(category) {
        const cached = this.cache[category];
        return cached && (Date.now() - cached.timestamp) < this.cacheTimeout;
    }
}

// Initialize NewsAPI
const newsAPI = new NewsAPI();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NewsAPI, newsAPI };
}
