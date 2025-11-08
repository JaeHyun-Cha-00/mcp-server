# 🧠 MCP Story Evaluator Server

This project implements a **Model Context Protocol (MCP)** server that exposes AI-powered tools for story evaluation.  
It connects to a **Wolverine vLLM instance** (an OpenAI-compatible API server) and provides structured literary feedback with numerical scores and short explanations.

---

## 🚀 Features

- **Claude Integration (MCP):** Works as a local MCP tool provider for Claude Desktop.  
- **AI-Powered Evaluation:** Uses large language models hosted on a Wolverine server.  
- **Multi-Criteria Assessment:** Evaluates stories across 14 distinct writing-quality categories.
- **JSON-Structured Results:** Returns normalized, machine-readable results with score and explanation fields.  

---

## 🧩 Project Structure

```
mcp-server/
└── src/
    ├── main.py          # MCP entry point (tool registration)
    ├── clients.py       # Handles communication with the Wolverine API
    ├── evaluation.py    # Core logic for story evaluation
    └── config.py        # Configuration (model, base URL)
```

---

## ⚙️ Installation

### 1️⃣ Create virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies
```bash
pip install fastmcp openai datasets
```

---

## 🧠 Configuration

All connection and model settings are defined directly in **`config.py`**.  
You don’t need to set any environment variables manually.

Example configuration inside `config.py`:
```python
BASE_URL = "http://localhost:8000/v1"
MODEL = "LLM_MODEL"
```

---

## 🧰 Running the MCP Server

Run the server directly with Python:
```bash
python main.py
```

Once running, the server exposes three MCP tools:

| Tool | Description |
|------|--------------|
| `list_categories` | Returns all available evaluation categories |
| `evaluate_single` | Evaluates one story for a single category |
| `evaluate_all` | Evaluates one story across all categories |

---

## 💬 Using with Claude Desktop

### Step 1. Download Claude Desktop

### Step 2. Add your MCP Server  
1. Open **Claude Desktop**  
2. Go to **Settings → Developer → Add**  

After adding, Claude will automatically detect and use the `story-evaluator` MCP server.

---

## 🧪 Example Usage

**Claude prompt:**
> Use the `story-evaluator` tool to evaluate the following story across all categories:  
>  
> *Once upon a time, a robot dreamed of writing poetry.*

**Response Example:**
```json
{
  "category": "Clarity and understandability",
  "score": 8,
  "explanation": "The story is concise, clear, and easy to follow."
}
```

---

## How It Works

1. Claude calls an MCP tool (`evaluate_single` / `evaluate_all`).  
2. The MCP server (`main.py`) forwards the request to the evaluation logic (`evaluation.py`).  
3. `evaluation.py` builds a structured prompt and sends it to Wolverine via the OpenAI SDK (`clients.py`).  
4. The vLLM model processes the story and returns a JSON response.  
5. The result is sent back to Claude for display.  

```
Claude → FastMCP (main.py) → StoryEvaluator → Wolverine (vLLM)
```
