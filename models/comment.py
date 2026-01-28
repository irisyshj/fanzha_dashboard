from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Comment(db.Model):
    """评论数据模型"""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.String(100), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="approved", nullable=False)  # pending, approved
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "article_id": self.article_id,
            "author": self.author,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def get_approved_by_article(cls, article_id: str) -> list["Comment"]:
        """获取文章的已审核评论"""
        return cls.query.filter_by(
            article_id=article_id, status="approved"
        ).order_by(cls.created_at.desc()).all()

    @classmethod
    def count_by_article(cls, article_id: str) -> int:
        """统计文章评论数"""
        return cls.query.filter_by(
            article_id=article_id, status="approved"
        ).count()
