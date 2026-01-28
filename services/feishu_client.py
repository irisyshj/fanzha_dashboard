import time
import requests
from typing import Optional, List
from config import Config


class FeishuClient:
    """飞书 API 客户端"""

    def __init__(self):
        self.app_id = Config.FEISHU_APP_ID
        self.app_secret = Config.FEISHU_APP_SECRET
        self.base_url = Config.FEISHU_BASE_URL
        self.base_id = Config.BASE_ID
        self.table_id = Config.TABLE_ID
        self._tenant_access_token: Optional[str] = None
        self._token_expires_at: float = 0

    def _get_tenant_access_token(self) -> str:
        """获取 tenant_access_token"""
        # 检查 token 是否有效
        if self._tenant_access_token and time.time() < self._token_expires_at:
            return self._tenant_access_token

        url = f"{self.base_url}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != 0:
                raise Exception(f"Failed to get token: {data.get('msg')}")

            self._tenant_access_token = data.get("tenant_access_token")
            expire = data.get("expire", 7200)  # 默认2小时
            self._token_expires_at = time.time() + expire - 60  # 提前1分钟过期

            return self._tenant_access_token

        except requests.RequestException as e:
            raise Exception(f"Failed to request token: {str(e)}")

    def get_records(
        self,
        page_size: int = 100,
        page_token: Optional[str] = None,
    ) -> dict:
        """获取多维表格记录"""
        token = self._get_tenant_access_token()
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{self.base_id}/tables/{self.table_id}/records"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != 0:
                raise Exception(f"Failed to get records: {data.get('msg')}")

            return data.get("data", {})

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch records: {str(e)}")

    def get_all_records(self) -> List[dict]:
        """获取所有记录（自动分页）"""
        all_records = []
        page_token = None

        while True:
            data = self.get_records(page_size=100, page_token=page_token)
            all_records.extend(data.get("items", []))

            page_token = data.get("page_token")
            if not page_token or not data.get("has_more"):
                break

        return all_records

    def get_record(self, record_id: str) -> Optional[dict]:
        """获取单条记录"""
        token = self._get_tenant_access_token()
        url = f"{self.base_url}/open-apis/bitable/v1/apps/{self.base_id}/tables/{self.table_id}/records/{record_id}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != 0:
                return None

            return data.get("data")

        except requests.RequestException:
            return None
