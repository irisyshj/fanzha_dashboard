import os
import re
from flask import Flask, render_template
from flask_caching import Cache
from config import Config
from models.comment import db as comment_db

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化缓存
cache = Cache()
cache.init_app(app)
# 将缓存设置为 app 属性，便于通过 current_app.cache 访问
app.cache = cache

# 初始化评论数据库
comment_db.init_app(app)
# 将数据库设置为 app 属性
app.db = comment_db


# 自定义过滤器：格式化文章内容
def format_article_text(text):
    """格式化文章内容，添加适当的换行和分段"""
    if not text:
        return ""

    # 移除 markdown 语法
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 移除图片
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # 转换 markdown 链接为纯文本

    # 清理多余的空白字符
    text = re.sub(r'\n{3,}', '\n\n', text)  # 多个换行压缩为两个
    text = re.sub(r'[ \t]+', ' ', text)  # 多个空格压缩为一个

    # 在特定标点后添加换行
    text = re.sub(r'([。！？])([^\n])', r'\1\n\2', text)  # 句号后换行
    text = re.sub(r'([：;；])\s*', r'\1 ', text)  # 冒号后保留一个空格

    # 分段处理 - 按照关键词分段
    section_keywords = ['案情回顾', '案件特点', '诈骗手法', '反诈提醒', '警方提示', '防范建议', '温馨提示', '相关链接']
    for keyword in section_keywords:
        text = re.sub(r'([^\n])(' + keyword + ')', r'\1\n\n**\2**', text)

    # 处理粗体标记
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    # 将换行转换为段落
    paragraphs = text.split('\n\n')
    formatted = []
    for para in paragraphs:
        para = para.strip()
        if para:
            # 如果段落太长，尝试在适当位置分割
            if len(para) > 300 and '**' not in para:
                sentences = re.split(r'([。！？])', para)
                current = ''
                for i in range(0, len(sentences) - 1, 2):
                    if sentences[i]:
                        sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else '')
                        if current:
                            formatted.append(f'<p>{current}</p>')
                            current = sentence
                        else:
                            current = sentence
                        if len(current) > 200:
                            formatted.append(f'<p>{current}</p>')
                            current = ''
                if current:
                    formatted.append(f'<p>{current}</p>')
            else:
                formatted.append(f'<p>{para}</p>')

    return '\n'.join(formatted)


# 注册过滤器
app.jinja_env.filters['format_article'] = format_article_text

# 创建数据库表（只在本地环境）
if not os.getenv("VERCEL"):
    # 本地环境：确保 database 目录存在并创建表
    database_dir = os.path.join(os.path.dirname(__file__), "database")
    os.makedirs(database_dir, exist_ok=True)
    with app.app_context():
        comment_db.create_all()
else:
    # Vercel 环境：在请求处理时按需创建表
    @app.before_request
    def create_tables():
        comment_db.create_all()

# 注册蓝图
from routes import views_bp, api_bp
app.register_blueprint(views_bp)
app.register_blueprint(api_bp)


# Vercel 环境：显式处理静态文件
if os.getenv("VERCEL"):
    from flask import send_from_directory, jsonify

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """显式处理静态文件请求"""
        try:
            return send_from_directory('static', filename)
        except Exception as e:
            return jsonify({"error": f"Static file not found: {str(e)}"}), 404

# 验证配置
try:
    Config.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your .env file.")


@app.errorhandler(404)
def not_found(error):
    """404 错误页面"""
    return render_template("404.html"), 404


@app.route("/api/health")
def api_health():
    """API 健康检查（用于调试）"""
    try:
        from routes.api import health_check
        return health_check()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "config": {
                "feishu_app_id": bool(Config.FEISHU_APP_ID),
                "feishu_app_secret": bool(Config.FEISHU_APP_SECRET),
                "base_id": bool(Config.BASE_ID),
                "table_id": bool(Config.TABLE_ID),
            }
        }), 500


@app.errorhandler(500)
def internal_error(error):
    """500 错误页面"""
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
