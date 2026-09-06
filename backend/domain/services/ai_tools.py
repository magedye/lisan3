import datetime
from collections.abc import Callable
from typing import Any


class ToolDispatcher:
    """
    Minimal in-process tool dispatcher for AI-assisted research.
    Exposes only truly available tools. Simulated tools are never reported as executed.
    """

    def __init__(self):
        self._tools: dict[str, dict[str, Any]] = {}
        self.invocation_log = []

    def register_tool(self, name: str, func: Callable, description: str):
        self._tools[name] = {"func": func, "description": description}

    def get_available_tools(self) -> dict[str, str]:
        return {name: meta["description"] for name, meta in self._tools.items()}

    def execute_tool(self, name: str, kwargs: dict[str, Any]) -> Any:
        if name not in self._tools:
            raise ValueError(f"Tool {name} is not available.")

        result = self._tools[name]["func"](**kwargs)

        self.invocation_log.append(
            {
                "tool_name": name,
                "input": kwargs,
                "status": "SUCCESS",
                "executed_at": datetime.datetime.utcnow().isoformat(),
            }
        )

        return result


# Singleton for simple DI in FastAPI. Tools are registered only by a real
# runtime adapter; an empty registry is an honest capability state.
tool_dispatcher = ToolDispatcher()
