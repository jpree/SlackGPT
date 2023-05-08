import re
from unittest.mock import Mock
from chat_module.utils import get_purpose, process_message, extract_and_add_reaction

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

def test_extract_and_add_reaction():
    app = Mock()
    text = "Hello! [smile]"

    result = extract_and_add_reaction(app, text, "C123456789", "123456789.123456")
    assert result == "Hello!"
    app.client.reactions_add.assert_called_once_with(
        channel="C123456789", timestamp="123456789.123456", name="smile"
    )
