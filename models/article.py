from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import re


@dataclass
class ArticleAnalysis:
    """文章分析结果"""
    scam_type: str = ""  # 诈骗类型
    location: str = ""  # 案件地点
    key_features: list[str] = field(default_factory=list)  # 案件核心特点
    anti_fraud_tech: list[str] = field(default_factory=list)  # 反诈关键技术


@dataclass
class Article:
    """文章数据模型"""

    id: str  # 飞书记录 ID
    title: str  # 标题
    date: str  # 日期
    summary: str  # 摘要
    content: Optional[str] = None  # 完整内容（如有）
    source: str = ""  # 账号/信息来源
    address: str = ""  # 原文地址 URL
    created_at: datetime = None  # 缓存时间
    _analysis: Optional[ArticleAnalysis] = field(default=None, repr=False)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self._analysis is None:
            self._analysis = self._analyze_content()

    def _analyze_content(self) -> ArticleAnalysis:
        """分析文章内容，提取关键信息"""
        text = self.summary or ""
        analysis = ArticleAnalysis()

        # 提取诈骗类型
        scam_types = [
            "刷单", "杀猪盘", "虚假投资", "冒充公检法", "贷款诈骗",
            "客服诈骗", "中奖诈骗", "虚假征信", "网络博彩", "游戏充值",
            "裸聊敲诈", "兼职诈骗", "电商退款", "冒充客服"
        ]
        for scam_type in scam_types:
            if scam_type in text:
                analysis.scam_type = scam_type
                break

        # 提取地点
        location_patterns = [
            r"(?:在|位于|地点|地址)([^\s，。]{2,6}?)(?:市|区|县|省|镇|乡|村)",
            r"([\u4e00-\u9fa5]{2,6}?)(?:省|市|区|县|镇|派出所|公安局)",
        ]
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                analysis.location = matches[0]
                break

        # 提取案件特点 - 查找关键词句
        feature_patterns = [
            r"([^\s]{4,30}?)(?:诈骗|陷阱|套路|手段|方式)",
            r"特点[：:](.{4,50}?)(?:[\n\r]|。)",
        ]
        for pattern in feature_patterns:
            matches = re.findall(pattern, text)
            if matches:
                analysis.key_features.extend(matches[:3])

        # 提取反诈技术
        tech_keywords = ["预警", "劝阻", "拦截", "封堵", "止付", "冻结",
                        "研判", "溯源", "侦查", "抓捕", "反制"]
        found_techs = []
        for keyword in tech_keywords:
            if keyword in text:
                found_techs.append(keyword)
        analysis.anti_fraud_tech = found_techs

        return analysis

    @property
    def preview(self) -> str:
        """获取文章预览（前100字）"""
        content = self.content or self.summary
        if len(content) > 100:
            return content[:100] + "..."
        return content

    @property
    def scam_type(self) -> str:
        """诈骗类型"""
        return self._analysis.scam_type if self._analysis else ""

    @property
    def location(self) -> str:
        """案件地点"""
        return self._analysis.location if self._analysis else ""

    @property
    def key_features(self) -> list[str]:
        """案件核心特点"""
        return self._analysis.key_features if self._analysis else []

    @property
    def anti_fraud_tech(self) -> list[str]:
        """反诈关键技术"""
        return self._analysis.anti_fraud_tech if self._analysis else []

    def to_dict(self) -> dict:
        """转换为字典（用于缓存，不包含计算属性）"""
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "summary": self.summary,
            "content": self.content,
            "source": self.source,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_feishu_record(cls, record: dict, field_mapping: dict) -> "Article":
        """从飞书记录创建文章对象"""
        fields = record.get("fields", {})

        # 根据字段映射提取数据
        title = fields.get(field_mapping.get("title", "标题"), "")
        date = fields.get(field_mapping.get("date", "日期"), "")
        summary = fields.get(field_mapping.get("summary", "摘要"), "")
        source = fields.get(field_mapping.get("source", "账号"), "")

        # 获取地址字段（可能是链接类型）
        address_field = field_mapping.get("address", "地址")
        address = fields.get(address_field, "")
        # 如果地址是链接类型，提取 URL
        if isinstance(address, dict) and "link" in address:
            address = address["link"]

        return cls(
            id=record.get("record_id", ""),
            title=title,
            date=date,
            summary=summary,
            source=source,
            address=address,
        )
