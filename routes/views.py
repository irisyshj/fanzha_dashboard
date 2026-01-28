from flask import render_template, current_app
from routes import views_bp
from services.cache import get_all_articles, get_article


@views_bp.route("/")
def index():
    """首页 - 文章列表"""
    try:
        articles = get_all_articles()
        print(f"[DEBUG] Index: Found {len(articles)} articles")
        if articles:
            print(f"[DEBUG] First article: {articles[0].title}")
        return render_template("index.html", articles=articles)
    except Exception as e:
        print(f"[DEBUG] Index error: {str(e)}")
        import traceback
        traceback.print_exc()
        current_app.logger.error(f"Index page error: {str(e)}")
        return render_template("index.html", articles=[], error=str(e))


@views_bp.route("/article/<article_id>")
def article_detail(article_id):
    """文章详情页"""
    try:
        article = get_article(article_id)
        if not article:
            return render_template("detail.html", article=None, error="文章不存在")
        return render_template("detail.html", article=article)
    except Exception as e:
        current_app.logger.error(f"Article detail error: {str(e)}")
        return render_template("detail.html", article=None, error=str(e))


@views_bp.route("/search")
def search():
    """搜索页面"""
    return render_template("search.html")
