import pytest
from unittest.mock import Mock, patch
from services.feishu_client import FeishuClient


class TestFeishuClient:
    @pytest.fixture
    def client(self):
        return FeishuClient()

    def test_init(self, client):
        assert client.app_id is not None
        assert client.app_secret is not None
        assert client.base_id is not None
        assert client.table_id is not None

    @patch('services.feishu_client.requests.post')
    def test_get_tenant_access_token(self, mock_post, client):
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "tenant_access_token": "test_token",
            "expire": 7200
        }
        mock_post.return_value = mock_response

        token = client._get_tenant_access_token()

        assert token == "test_token"
        assert client._tenant_access_token == "test_token"

    @patch('services.feishu_client.requests.get')
    def test_get_records(self, mock_get, client):
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {
                "items": [{"record_id": "1", "fields": {}}],
                "has_more": False,
                "page_token": None
            }
        }
        mock_get.return_value = mock_response

        records = client.get_records()

        assert "items" in records
        assert len(records["items"]) == 1
