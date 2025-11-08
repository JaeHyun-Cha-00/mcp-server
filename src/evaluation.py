"""Story evaluation logic that communicates with the Wolverine (vLLM) model."""

import json
import re
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from clients import WolverineClient


# --------------------------- Prompts --------------------------- #

EVALUATION_SYSTEM_PROMPT = (
    "You are a literary critic. Always respond with JSON containing the keys "
    '"score" (an integer from 1 to 10) and "explanation" (a short justification).'
)

def build_user_prompt(story: str, category: str) -> str:
    """Build the user prompt sent to the model."""
    return f"Evaluate the following story focusing strictly on the category: {category}.\n\nStory:\n{story}"


# --------------------------- Categories --------------------------- #

STORY_EVALUATION_CATEGORIES = [
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


# --------------------------- Data Model --------------------------- #

@dataclass
class EvaluationResult:
    """Normalized representation of an evaluation response."""

    category: str
    score: float | None
    explanation: str
    raw_response: str

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "score": self.score,
            "explanation": self.explanation,
            "raw_response": self.raw_response,
        }


# --------------------------- Main Evaluator --------------------------- #

class StoryEvaluator:
    """Evaluate stories for multiple quality categories using Wolverine."""

    def __init__(self, client: WolverineClient, *, categories=STORY_EVALUATION_CATEGORIES):
        self._client = client
        self._categories = list(categories)

    @property
    def categories(self) -> list[str]:
        return self._categories

    def evaluate(self, story: str, category: str) -> EvaluationResult:
        """Evaluate a story for a single category."""
        if category not in self._categories:
            raise ValueError(f"Unknown category '{category}'")

        user_prompt = build_user_prompt(story, category)
        raw_response = self._client.chat(
            system_prompt=EVALUATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        score, explanation = _parse_response(raw_response)
        return EvaluationResult(category, score, explanation, raw_response)

    def evaluate_all(self, story: str) -> dict[str, EvaluationResult]:
        """Evaluate a story across every configured category (in parallel)."""
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda c: (c, self.evaluate(story, c)), self._categories))
        return dict(results)


# --------------------------- Response Parsing --------------------------- #

def _parse_response(response: str) -> tuple[float | None, str]:
    """Parse the model's response into a numeric score and explanation."""
    response = response.strip()
    if not response:
        return None, ""

    # Try structured JSON response
    try:
        payload = json.loads(response)
        score = float(payload.get("score")) if "score" in payload else None
        explanation = str(payload.get("explanation", "")).strip()
        return score, explanation
    except json.JSONDecodeError:
        pass

    # Fallback: extract numeric score from text
    match = re.search(r"(?<!\d)(10|[1-9])(?!\d)", response)
    score = float(match.group(1)) if match else None
    explanation = response if not match else response.replace(match.group(0), "", 1).strip()
    return score, explanation