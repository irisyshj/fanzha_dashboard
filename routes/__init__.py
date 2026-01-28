from flask import Blueprint

# 创建蓝图
views_bp = Blueprint("views", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")

from routes import views, api
