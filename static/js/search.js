// 搜索功能脚本

const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const searchResults = document.getElementById('searchResults');

let searchTimeout = null;

// 执行搜索
async function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
        searchResults.innerHTML = '<div class="search-hint"><p>输入关键词开始搜索</p></div>';
        return;
    }

    // 显示加载状态
    searchResults.innerHTML = '<div class="loading">搜索中...</div>';

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        displaySearchResults(data.articles, query);

        // 保存搜索历史
        saveSearchHistory(query);

    } catch (error) {
        searchResults.innerHTML = `
            <div class="error-message">
                <p>搜索出错: ${error.message}</p>
            </div>
        `;
    }
}

// 显示搜索结果
function displaySearchResults(articles, query) {
    if (articles.length === 0) {
        searchResults.innerHTML = `
            <div class="search-hint">
                <p>没有找到与 "${escapeHtml(query)}" 相关的文章</p>
            </div>
        `;
        return;
    }

    const html = articles.map(article => {
        const title = highlightText(article.title, query);
        const preview = highlightText(article.summary || '', query);

        return `
            <div class="search-result-item">
                <div class="search-result-title">
                    <a href="/article/${article.id}" target="_blank">${title}</a>
                </div>
                <div class="article-source">
                    <span class="source-icon">@</span>
                    <span>${escapeHtml(article.source || '未知来源')}</span>
                    <span class="article-date">${escapeHtml(article.date || '')}</span>
                </div>
                <div class="search-result-preview">${preview}</div>
            </div>
        `;
    }).join('');

    searchResults.innerHTML = `
        <div class="search-results-info">
            <p>找到 ${articles.length} 篇相关文章</p>
        </div>
        ${html}
    `;
}

// 高亮关键词
function highlightText(text, query) {
    if (!text) return '';
    const escaped = escapeHtml(text);
    const escapedQuery = escapeHtml(query);
    const regex = new RegExp(`(${escapedQuery})`, 'gi');
    return escaped.replace(regex, '<span class="search-highlight">$1</span>');
}

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 保存搜索历史
function saveSearchHistory(query) {
    let history = JSON.parse(localStorage.getItem('searchHistory') || '[]');

    // 移除重复项
    history = history.filter(item => item !== query);

    // 添加到开头
    history.unshift(query);

    // 限制历史记录数量
    if (history.length > 10) {
        history = history.slice(0, 10);
    }

    localStorage.setItem('searchHistory', JSON.stringify(history));
}

// 加载搜索历史
function loadSearchHistory() {
    const history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    return history;
}

// 事件监听
searchButton.addEventListener('click', performSearch);

searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

// 防抖搜索
let debounceTimer;
searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        if (searchInput.value.trim().length >= 2) {
            performSearch();
        }
    }, 500);
});

// 页面加载时聚焦搜索框
searchInput.focus();
