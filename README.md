# MCP Server

## Install Requirements

```bash
brew install uv
```

```bash
uv init .
```

```bash
uv add "mcp[cli]"
```

## Run the MCP Server

```bash
uv run mcp
```

The server exposes several MCP tools that proxy requests to a Wolverine instance
running an OpenAI-compatible API. Configure the connection with the following
environment variables (defaults shown):

| Variable | Description | Default |
| --- | --- | --- |
| `WOLVERINE_BASE_URL` | Base URL of the Wolverine OpenAI-compatible endpoint | `http://127.0.0.1:11434/v1` |
| `WOLVERINE_API_KEY` | API key used to authenticate to Wolverine | `not-required` |
| `WOLVERINE_MODEL` | Model identifier served by Wolverine | `mistralai/Mistral-7B-Instruct-v0.2` |
| `WOLVERINE_TEMPERATURE` | Sampling temperature applied to evaluations | `0.7` |
| `WOLVERINE_TOP_P` | Nucleus sampling parameter | `0.95` |
| `WOLVERINE_MAX_NEW_TOKENS` | Maximum number of tokens generated per evaluation | `256` |
| `WOLVERINE_REQUEST_TIMEOUT` | Timeout (seconds) for Wolverine API requests | `120` |

## Download Claude Desktop
https://claude.ai/download

## Using with Claude Desktop
1. Open Claude Desktop
2. Go to Settings -> Developer -> Add
3. Command : /opt/homebrew/bin/uv
4. Args : run --with mcp[cli] mcp run /Users/<username>/Documents/GitHub/mcp-server/examples/snippets/clients/demo.py

## Running Server
```bash
uv run mcp install demo.py
```

