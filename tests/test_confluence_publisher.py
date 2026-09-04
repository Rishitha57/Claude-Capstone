import base64
import json
from io import BytesIO
from unittest.mock import patch

import pytest

from app.confluence_publisher import (
    ConfluenceConfig,
    ConfluenceConfigurationError,
    ConfluenceClient,
)


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def config() -> ConfluenceConfig:
    return ConfluenceConfig(
        base_url="https://example.atlassian.net",
        space_key="FIN",
        email="advisor@example.com",
        api_token="test-token",
        parent_page_id="42",
    )


def test_publish_page_creates_page_with_parent_and_basic_auth():
    responses = [FakeResponse({"results": []}), FakeResponse({"id": "100"})]

    with patch("app.confluence_publisher.urlopen", side_effect=responses) as open_url:
        result = ConfluenceClient(config()).publish_page("Requirements", "<h1>US-001</h1>")

    assert result == {"id": "100"}
    request = open_url.call_args_list[1].args[0]
    assert request.full_url.endswith("/wiki/rest/api/content")
    assert json.loads(request.data) == {
        "type": "page",
        "title": "Requirements",
        "space": {"key": "FIN"},
        "body": {"storage": {"value": "<h1>US-001</h1>", "representation": "storage"}},
        "ancestors": [{"id": "42"}],
    }
    expected_auth = base64.b64encode(b"advisor@example.com:test-token").decode()
    assert request.get_header("Authorization") == f"Basic {expected_auth}"


def test_publish_page_updates_existing_page_version():
    responses = [
        FakeResponse({"results": [{"id": "100", "version": {"number": 3}}]}),
        FakeResponse({"id": "100", "version": {"number": 4}}),
    ]

    with patch("app.confluence_publisher.urlopen", side_effect=responses) as open_url:
        ConfluenceClient(config()).publish_page("Requirements", "<p>updated</p>")

    request = open_url.call_args_list[1].args[0]
    assert request.get_method() == "PUT"
    assert request.full_url.endswith("/wiki/rest/api/content/100")
    assert json.loads(request.data)["version"] == {"number": 4}


def test_publish_page_can_override_default_parent_for_child_pages():
    responses = [FakeResponse({"results": []}), FakeResponse({"id": "child-100"})]

    with patch("app.confluence_publisher.urlopen", side_effect=responses) as open_url:
        ConfluenceClient(config()).publish_page("Requirements", "<p>story</p>", parent_page_id="root-10")

    request = open_url.call_args_list[1].args[0]
    assert json.loads(request.data)["ancestors"] == [{"id": "root-10"}]


def test_config_requires_all_connection_values(monkeypatch):
    for name in ("CONFLUENCE_BASE_URL", "CONFLUENCE_SPACE_KEY", "CONFLUENCE_EMAIL", "CONFLUENCE_API_TOKEN"):
        monkeypatch.delenv(name, raising=False)

    with patch("app.confluence_publisher._load_dotenv"):
        with pytest.raises(ConfluenceConfigurationError):
            ConfluenceConfig.from_environment()
