import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置类"""

    # 飞书应用配置
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
    FEISHU_BASE_URL = "https://open.feishu.cn"

    # 多维表格配置
    BASE_ID = os.getenv("BASE_ID")
    TABLE_ID = os.getenv("TABLE_ID")

    # Flask 配置
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("FLASK_ENV") == "development"

    # 缓存配置
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))  # 5分钟

    # 数据库配置 (评论功能)
    # Vercel 环境使用临时目录，本地开发使用 database 目录
    if os.getenv("VERCEL"):
        # Vercel 环境：使用 /tmp 目录
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/comments.db"
    else:
        # 本地开发环境
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'database', 'comments.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 飞书字段映射配置
    FIELD_MAPPING = {
        "title": "标题",
        "date": "日期",
        "summary": "摘要",
        "source": "账号",
        "address": "地址",
    }

    @staticmethod
    def validate_config():
        """验证必需的配置项"""
        required = [
            "FEISHU_APP_ID",
            "FEISHU_APP_SECRET",
            "BASE_ID",
            "TABLE_ID",
        ]
        missing = [key for key in required if not getattr(Config, key)]

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Please set these values in your .env file."
            )
