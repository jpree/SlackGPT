import re
from unittest.mock import Mock
from chat_module.utils import get_purpose, process_message

def test_get_purpose(chatbot):
    app = Mock()
    app.client.conversations_info.return_value = {
        "ok": True,
        "channel": {
            "purpose": {
                "value": ";persona;Sample Persona"
            }
        }
    }

    result = get_purpose(chatbot, app, "C123456789", "U123456789")
    assert result == "Sample Persona"

def test_process_message(chatbot):
    app = Mock()
    chatbot.chat = Mock(side_effect=[Mock(content="Hello!")])

    result = process_message(chatbot, app, "Hi there!", "C123456789", "U123456789")
    assert result == "Hello!"
