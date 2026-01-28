# Vercel 环境变量检查清单

## 需要在 Vercel 中配置的环境变量

请访问 https://vercel.com/irisyshj/fanzha-dashboard-te7a/settings/environment-variables

添加以下环境变量：

```
FEISHU_APP_ID=cli_a9dcdfa0a9b89cee
FEISHU_APP_SECRET=FH80xNtndE2Z7WN0PR37hgUIvXXubmpB
BASE_ID=J3zVbwvx5axRX6s2OhqcHiyqnae
TABLE_ID=tblVM9GjX9lAWIPS
SECRET_KEY=your-random-secret-key-here
```

## 配置步骤

1. 打开 Vercel 项目设置页面
2. 进入 "Environment Variables"
3. 逐个添加上述变量
4. 选择适用的环境（Production, Preview, Development）
5. 保存后重新部署

## 快速验证

部署完成后，访问：
https://fanzha-dashboard-te7a.vercel.app/api/search

如果返回 JSON 数据而不是错误，说明环境变量配置正确。
