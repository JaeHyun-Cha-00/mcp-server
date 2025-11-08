"""Story evaluation logic that communicates with Wolverine."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping

from clients import WolverineClient


EVALUATION_SYSTEM_PROMPT = (
    "You are a precise literary critic. Always respond with JSON containing the keys "
    '"score" (an integer from 1 to 10) and "explanation" (a short justification).'
)


def build_user_prompt(story: str, category: str) -> str:
    """Build the user prompt sent to the Wolverine endpoint."""

    return (
        "Evaluate the following story focusing strictly on the category: "
        f"{category}.\n\nStory:\n{story}"
    )


STORY_EVALUATION_CATEGORIES: List[str] = [
    # Language Quality
    "Grammar, spelling, and punctuation quality",
    "Sentence pattern variety",
    "Avoidance of clichés and overused phrases",
    # Clarity & Logic
    "Clarity and understandability",
    "Logical connection between events and ideas",
    "Internal consistency within the story's context",
    # Narrative Construction
    "Scene construction and purpose",
    "Avoidance of predictable narrative tropes",
    "Ability to hold reader interest",
    # Character Realism
    "Character consistency",
    "Character motivation and actions making sense",
    "Natural dialogue",
    "Character depth and dimensionality",
    "Realistic character interactions",
]


@dataclass
class EvaluationResult:
    """Normalized representation of an evaluation response."""

    category: str
    score: float | None
    explanation: str
    raw_response: str

    def to_dict(self) -> Dict[str, object]:
        """Serialize the result to a dictionary that can be returned from MCP tools."""

        return {
            "category": self.category,
            "score": self.score,
            "explanation": self.explanation,
            "raw_response": self.raw_response,
        }


class StoryEvaluator:
    """Evaluate stories for multiple quality categories using Wolverine."""

    def __init__(
        self,
        client: WolverineClient,
        *,
        categories: Iterable[str] = STORY_EVALUATION_CATEGORIES,
    ) -> None:
        self._client = client
        self._categories = list(categories)

    @property
    def categories(self) -> List[str]:
        """All supported evaluation categories."""

        return list(self._categories)

    def evaluate(self, story: str, category: str) -> EvaluationResult:
        """Evaluate a story for a single category."""

        if category not in self._categories:
            raise ValueError(
                f"Unknown category '{category}'. Available categories: {self._categories}"
            )

        user_prompt = build_user_prompt(story, category)
        raw_response = self._client.chat(
            system_prompt=EVALUATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        score, explanation = _parse_response(raw_response)
        return EvaluationResult(category, score, explanation, raw_response)

    def evaluate_all(self, story: str) -> Mapping[str, EvaluationResult]:
        """Evaluate a story across every configured category."""

        return {category: self.evaluate(story, category) for category in self._categories}


def _parse_response(response: str) -> tuple[float | None, str]:
    """Parse the Wolverine response into a score and explanation."""

    response = response.strip()
    if not response:
        return None, ""

    try:
        payload = json.loads(response)
        score = float(payload.get("score")) if "score" in payload else None
        explanation = str(payload.get("explanation", "")).strip()
        return score, explanation
    except json.JSONDecodeError:
        pass

    score_match = re.search(r"\b(10|[1-9])\b", response)
    score = float(score_match.group(1)) if score_match else None
    explanation = response if score_match is None else response.replace(score_match.group(0), "", 1).strip()
    return score, explanation

