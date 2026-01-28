// 评论功能脚本

const commentForm = document.getElementById('commentForm');
const commentsList = document.getElementById('commentsList');
const commentAuthor = document.getElementById('commentAuthor');
const commentContent = document.getElementById('commentContent');

// 加载评论
async function loadComments() {
    if (!ARTICLE_ID) return;

    try {
        const response = await fetch(`/api/articles/${ARTICLE_ID}/comments`);
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        displayComments(data.comments);

    } catch (error) {
        commentsList.innerHTML = `
            <div class="error-message">
                <p>加载评论失败: ${error.message}</p>
            </div>
        `;
    }
}

// 显示评论列表
function displayComments(comments) {
    if (comments.length === 0) {
        commentsList.innerHTML = `
            <div class="empty-state">
                <p>暂无评论，快来抢沙发吧~</p>
            </div>
        `;
        return;
    }

    const html = comments.map(comment => `
        <div class="comment-item">
            <div class="comment-header">
                <span class="comment-author">${escapeHtml(comment.author)}</span>
                <span class="comment-date">${formatCommentDate(comment.created_at)}</span>
            </div>
            <div class="comment-content">${escapeHtml(comment.content)}</div>
        </div>
    `).join('');

    commentsList.innerHTML = html;
}

// 提交评论
commentForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const author = commentAuthor.value.trim();
    const content = commentContent.value.trim();

    if (!author || !content) {
        alert('请填写昵称和评论内容');
        return;
    }

    // 禁用提交按钮
    const submitButton = commentForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.textContent = '提交中...';

    try {
        const response = await fetch(`/api/articles/${ARTICLE_ID}/comments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ author, content })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // 清空表单
        commentContent.value = '';

        // 重新加载评论
        await loadComments();

        // 显示成功提示
        alert('评论发表成功！');

    } catch (error) {
        alert(`评论失败: ${error.message}`);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = '发表评论';
    }
});

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 格式化评论日期
function formatCommentDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;

    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// 页面加载时获取评论
loadComments();
