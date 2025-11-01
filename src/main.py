from fastmcp import MCPServer
from datasets import load_dataset
from langchain_community.llms import VLLM

# --------------------------------------
# Initialize MCP Server
# --------------------------------------
server = MCPServer("story-evaluator")

# --------------------------------------
# Initialize the LLM model (same as before)
# --------------------------------------
llm = VLLM(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    trust_remote_code=True,
    max_new_tokens=256,
    top_k=10,
    top_p=0.95,
    temperature=0.7,
)

# llm = VLLM(
#     model="meta-llama/Meta-Llama-3-8B-Instruct",
#     trust_remote_code=True,
#     max_new_tokens=256,
#     top_k=10,
#     top_p=0.9,
#     temperature=0.6,
# )

# llm = VLLM(
#     model="swiss-ai/Apertus-8B-Instruct-2509",
#     trust_remote_code=True,
#     max_new_tokens=256,
#     top_k=10,
#     top_p=0.9,
#     temperature=0.6,
# )

# llm = VLLM(
#     model="google/gemma-3-12b-it",
#     trust_remote_code=True,
#     max_new_tokens=256,
#     top_k=10,
#     top_p=0.9,
#     temperature=0.6,
# )

# llm = VLLM(
#     model="nvidia/Llama-3.1-Nemotron-Nano-8B-v1",
#     trust_remote_code=True,
#     max_new_tokens=256,
#     top_k=10,
#     top_p=0.9,
#     temperature=0.6,
# )

# llm = VLLM(
#     model="microsoft/Phi-4-mini-instruct",
#     trust_remote_code=True,
#     max_new_tokens=256,
#     top_k=10,
#     top_p=0.9,
#     temperature=0.6,
# )

# --------------------------------------
# Dataset Loader Tool
# --------------------------------------
@server.tool()
def load_dataset_tool(dataset_name: str, split: str = "train", text_column: str = "text") -> list:
    """
    Load a dataset from Hugging Face and return up to 10 text samples.
    Example: load_dataset_tool("imdb", "train", "text")
    """
    dataset = load_dataset(dataset_name, split=split)
    if text_column not in dataset.column_names:
        raise ValueError(
            f"Column '{text_column}' not found in dataset '{dataset_name}'. "
            f"Available columns: {dataset.column_names}"
        )
    return dataset[text_column][:10]  # Limit for testing


# --------------------------------------
# Shared evaluation function
# --------------------------------------
def evaluate_story(response: str, category: str) -> str:
    """
    Evaluate one aspect of story quality using the vLLM model.
    """
    prompt = f"""
    You are a story evaluator.
    Evaluate the following story on the category "{category}".
    Give a score from 1 to 10.

    Story:
    {response}
    """
    return llm(prompt)


# --------------------------------------
# Story evaluation categories
# --------------------------------------
CATEGORIES = [
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

# --------------------------------------
# Individual Evaluation Tool
# --------------------------------------
@server.tool()
def evaluate_single(story: str, category: str) -> str:
    """
    Evaluate a single story for a given category (1–10 scale).
    Example: evaluate_single("Once upon a time...", "Clarity and understandability")
    """
    return evaluate_story(story, category)


# --------------------------------------
# Full Multi-Category Evaluation Tool
# --------------------------------------
@server.tool()
def evaluate_all(story: str) -> dict:
    """
    Evaluate the given story across all predefined categories.
    Returns a dictionary of category → score.
    """
    results = {}
    for category in CATEGORIES:
        score = evaluate_story(story, category)
        results[category] = score
    return results


# --------------------------------------
# Batch Evaluation for Dataset
# --------------------------------------
@server.tool()
def evaluate_dataset(dataset_name: str, split: str = "train", text_column: str = "text", limit: int = 5) -> list:
    """
    Load a dataset from Hugging Face and evaluate the first N samples across all categories.
    Returns a list of dictionaries (story + scores).
    """
    dataset = load_dataset(dataset_name, split=split)
    if text_column not in dataset.column_names:
        raise ValueError(f"Column '{text_column}' not found. Available: {dataset.column_names}")

    stories = dataset[text_column][:limit]
    evaluations = []

    for story in stories:
        scores = evaluate_all(story)
        evaluations.append({"story": story, "scores": scores})

    return evaluations


# --------------------------------------
# Run the MCP Server
# --------------------------------------
if __name__ == "__main__":
    server.run()
