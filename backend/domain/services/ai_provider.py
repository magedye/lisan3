import os

from pydantic_ai.models.test import TestModel

_model_instance = None
_model_name = "test-model"


def get_ai_model():
    """
    Factory function to retrieve the configured AI model.
    Uses TestModel if no OPENAI_API_KEY is found (TESTED_WITH_FAKE_PROVIDER).
    """
    global _model_instance, _model_name
    if _model_instance is None:
        if os.environ.get("OPENAI_API_KEY"):
            _model_instance = "openai:gpt-4o"
            _model_name = "openai:gpt-4o"
        else:
            _model_instance = TestModel()
            _model_name = "pydantic_ai:test"
    return _model_instance


def get_provider_name() -> str:
    return _model_name
