import pytest
from models.article import Article
from datetime import datetime


class TestArticle:
    def test_article_creation(self):
        article = Article(
            id="1",
            title="测试标题",
            date="2024-01-01",
            summary="测试摘要",
            source="测试来源"
        )

        assert article.id == "1"
        assert article.title == "测试标题"
        assert article.date == "2024-01-01"
        assert article.summary == "测试摘要"
        assert article.source == "测试来源"
        assert article.created_at is not None

    def test_preview_property(self):
        article = Article(
            id="1",
            title="测试",
            date="2024-01-01",
            summary="这是一段很长的摘要内容，超过了100个字符的限制，所以应该被截断并显示省略号",
            source="测试"
        )

        preview = article.preview
        assert len(preview) == 103  # 100 + "..."
        assert preview.endswith("...")

    def test_to_dict(self):
        article = Article(
            id="1",
            title="测试",
            date="2024-01-01",
            summary="摘要",
            source="来源"
        )

        data = article.to_dict()

        assert data["id"] == "1"
        assert data["title"] == "测试"
        assert "created_at" in data

    def test_from_feishu_record(self):
        record = {
            "record_id": "rec123",
            "fields": {
                "标题": "飞书标题",
                "日期": "2024-01-01",
                "摘要": "飞书摘要",
                "账号": "飞书账号"
            }
        }

        field_mapping = {
            "title": "标题",
            "date": "日期",
            "summary": "摘要",
            "source": "账号"
        }

        article = Article.from_feishu_record(record, field_mapping)

        assert article.id == "rec123"
        assert article.title == "飞书标题"
        assert article.date == "2024-01-01"
        assert article.summary == "飞书摘要"
        assert article.source == "飞书账号"
