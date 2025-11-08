"""Entry point for the MCP story evaluation server."""

from fastmcp import FastMCP
from clients import WolverineClient
from evaluation import StoryEvaluator

# Initialize MCP server and evaluation components
server = FastMCP("story-evaluator")
_client = WolverineClient()
_evaluator = StoryEvaluator(_client)


@server.tool()
def list_categories() -> list[str]:
    """Return all supported evaluation categories."""
    return _evaluator.categories


@server.tool()
def evaluate_single(story: str, category: str) -> dict:
    """Evaluate a single story for a given category (1–10 scale)."""
    return _evaluator.evaluate(story, category).to_dict()


@server.tool()
def evaluate_all(story: str) -> dict[str, dict]:
    """Evaluate the given story across all predefined categories."""
    results = _evaluator.evaluate_all(story)
    return {cat: res.to_dict() for cat, res in results.items()}


if __name__ == "__main__":
    server.run()
