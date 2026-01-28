from flask import jsonify, request, current_app
from routes import api_bp
from services.cache import get_all_articles
from models.comment import Comment
from models.comment import db as comment_db


@api_bp.route("/search")
def search_articles():
    """搜索文章 API"""
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"articles": [], "total": 0})

    try:
        articles = get_all_articles()
        query_lower = query.lower()

        # 搜索标题、摘要、账号
        results = [
            article.to_dict()
            for article in articles
            if (
                query_lower in article.title.lower()
                or query_lower in article.summary.lower()
                or query_lower in article.source.lower()
            )
        ]

        return jsonify({"articles": results, "total": len(results)})

    except Exception as e:
        current_app.logger.error(f"Search error: {str(e)}")
        return jsonify({"error": str(e), "articles": [], "total": 0}), 500


@api_bp.route("/articles/<article_id>/comments", methods=["GET"])
def get_comments(article_id):
    """获取文章评论"""
    try:
        comments = Comment.get_approved_by_article(article_id)
        return jsonify({
            "comments": [comment.to_dict() for comment in comments],
            "total": len(comments)
        })
    except Exception as e:
        current_app.logger.error(f"Get comments error: {str(e)}")
        return jsonify({"error": str(e), "comments": [], "total": 0}), 500


@api_bp.route("/articles/<article_id>/comments", methods=["POST"])
def create_comment(article_id):
    """创建评论"""
    try:
        data = request.get_json()

        author = data.get("author", "").strip()
        content = data.get("content", "").strip()

        if not author or not content:
            return jsonify({"error": "昵称和内容不能为空"}), 400

        if len(author) > 100:
            return jsonify({"error": "昵称不能超过100个字符"}), 400

        if len(content) > 1000:
            return jsonify({"error": "评论内容不能超过1000个字符"}), 400

        comment = Comment(
            article_id=article_id,
            author=author,
            content=content,
            status="approved"  # 默认直接审核通过，可后续改为手动审核
        )

        comment_db.session.add(comment)
        comment_db.session.commit()

        return jsonify({
            "message": "评论成功",
            "comment": comment.to_dict()
        }), 201

    except Exception as e:
        comment_db.session.rollback()
        current_app.logger.error(f"Create comment error: {str(e)}")
        return jsonify({"error": str(e)}), 500
