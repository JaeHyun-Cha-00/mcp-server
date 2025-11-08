"""Entry point for the MCP story evaluation server."""

from __future__ import annotations

from typing import Dict, List

from datasets import load_dataset
from fastmcp import MCPServer

from clients import WolverineClient
from evaluation import StoryEvaluator


server = MCPServer("story-evaluator")

# Instantiate the Wolverine OpenAI-compatible client and story evaluator once so that
# the same connection details are reused across tool invocations.
_wolverine_client = WolverineClient()
_story_evaluator = StoryEvaluator(_wolverine_client)


@server.tool()
def load_dataset_tool(
    dataset_name: str, split: str = "train", text_column: str = "text"
) -> List[str]:
    """Load a dataset from Hugging Face and return up to 10 text samples."""

    dataset = load_dataset(dataset_name, split=split)
    if text_column not in dataset.column_names:
        raise ValueError(
            f"Column '{text_column}' not found in dataset '{dataset_name}'. "
            f"Available columns: {dataset.column_names}"
        )
    return dataset[text_column][:10]


@server.tool()
def list_categories() -> List[str]:
    """Return all supported evaluation categories."""

    return _story_evaluator.categories


@server.tool()
def evaluate_single(story: str, category: str) -> Dict[str, object]:
    """Evaluate a single story for a given category (1–10 scale)."""

    result = _story_evaluator.evaluate(story, category)
    return result.to_dict()


@server.tool()
def evaluate_all(story: str) -> Dict[str, Dict[str, object]]:
    """Evaluate the given story across all predefined categories."""

    evaluations = _story_evaluator.evaluate_all(story)
    return {category: result.to_dict() for category, result in evaluations.items()}


@server.tool()
def evaluate_dataset(
    dataset_name: str,
    split: str = "train",
    text_column: str = "text",
    limit: int = 5,
) -> List[Dict[str, object]]:
    """Evaluate the first ``limit`` samples from a dataset across all categories."""

    dataset = load_dataset(dataset_name, split=split)
    if text_column not in dataset.column_names:
        raise ValueError(
            f"Column '{text_column}' not found. Available columns: {dataset.column_names}"
        )

    stories = dataset[text_column][:limit]
    evaluations: List[Dict[str, object]] = []
    for story in stories:
        per_category = _story_evaluator.evaluate_all(story)
        evaluations.append(
            {
                "story": story,
                "evaluations": {
                    category: result.to_dict() for category, result in per_category.items()
                },
            }
        )

    return evaluations


if __name__ == "__main__":
    server.run()

