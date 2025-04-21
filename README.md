# Example of Open-WebUI's MCPO 

## Overview of MCPO
### What's MCPO?
**MCPO** is a tool to integrate MCP tools into OpenAPI-based workflow (e.g., LLM agents using HTTP).
MCPO is a compatibility layer that unlocks MCP for broader tooling ecosystems. For example:
- An A2A system could use MCPO to let agents access MCP tools via HTTP.
- An MCP-based tool can reach non-MCP clients (e.g., web apps) via MCPO.

### Difference between MCP and A2A
- Use MCP: For direct, high-performance communication between AI models/tools. 
- Use A2A: For multi-agent systems where agents need to collaborate dynamically.
- Use MCPO: For integrating MCP tools into OpenAPI-based workflows, allowing for broader compatibility and interoperability.

## Install and Run MCPO
I recommend using uv for lightning-fast startup and zero config.
```bash
uvx mcpo --port 8000 --api-key "top-secret" -- your_mcp_server_command
```

If using python:
```bash
pip install mcpo
mcpo --port 8000 --api-key "top-secret" -- your_mcp_server_command
```

## Run this example project
```bash
uvx mcpo --config config.json
```


