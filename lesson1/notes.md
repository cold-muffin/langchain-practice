# Advanced Agents

## Vocab
### MCP (Model Context Protocol)
An open-source protocol standardizing how a model connects with the tools and data sources it uses. In short, it is a standard way to transfer data between two sources.

**Problem:**
```
ChatGPT -> OpenAI database integration
Claude  -> Anthropic database intergration
Gemini  -> Google database integration
```

**Solution:**
```
ChatGPT \
Claude  |-> MCP Server -> Database integration
Gemini  /
```