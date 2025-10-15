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

