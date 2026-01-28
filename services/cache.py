from flask import current_app
from models.article import Article
from services.feishu_client import FeishuClient
from config import Config


def get_all_articles() -> list[Article]:
    """获取所有文章（带缓存）"""
    cache = current_app.cache

    # 尝试从缓存获取
    cached_articles = cache.get("all_articles")
    if cached_articles:
        return [Article(**article) for article in cached_articles]

    # 从飞书获取数据
    try:
        client = FeishuClient()
        records = client.get_all_records()

        # 转换为文章对象
        articles = [
            Article.from_feishu_record(record, Config.FIELD_MAPPING)
            for record in records
        ]

        # 缓存数据
        cache_data = [article.to_dict() for article in articles]
        cache.set("all_articles", cache_data, timeout=Config.CACHE_DEFAULT_TIMEOUT)

        return articles

    except Exception as e:
        current_app.logger.error(f"Failed to fetch articles: {str(e)}")
        return []


def get_article(article_id: str) -> Article | None:
    """获取单篇文章"""
    articles = get_all_articles()

    for article in articles:
        if article.id == article_id:
            return article

    return None


def clear_articles_cache():
    """清除文章缓存"""
    cache = current_app.cache
    cache.delete("all_articles")
