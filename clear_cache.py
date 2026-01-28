from app import app

with app.app_context():
    # 清除文章缓存
    app.cache.delete("all_articles")
    print("缓存已清除，请刷新页面")
