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
    print("[INFO] Tool called: list_categories")
    return _evaluator.categories


@server.tool()
def evaluate_single(story: str, category: str) -> dict:
    print(f"[INFO] Tool called: evaluate_single (category='{category}')")
    result = _evaluator.evaluate(story, category)
    print("[INFO] Response received from vLLM.")
    return result.to_dict()


@server.tool()
def evaluate_all(story: str) -> dict[str, dict]:
    print("[INFO] Tool called: evaluate_all")
    results = _evaluator.evaluate_all(story)
    print("[INFO] Response received from vLLM (all categories).")
    return {cat: res.to_dict() for cat, res in results.items()}


if __name__ == "__main__":
    server.run()
