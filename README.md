# Building AI Agents for Biomedical Research
### ISMB 2026 Tutorial

A hands-on tutorial series for computational biologists who want to build, customize, and orchestrate AI agents — from no-code visual tools to production-ready multi-agent pipelines. All examples are grounded in real biomedical tasks: literature search, pharmacogenomics, and scientific paper review.

---

## Learning Goals

By the end of this tutorial you will be able to:

- Build AI agents using visual GUI tools (no code required) and understand when to graduate to code
- Call LLMs programmatically using the Anthropic, OpenAI, and LangChain Python SDKs
- Extend agents with custom tools via the Model Context Protocol (MCP)
- Implement the ReAct (Reasoning + Acting) loop for multi-step tool use
- Apply the reflection pattern to improve LLM outputs against authoritative external sources
- Design and run multi-agent pipelines with a supervisor orchestrator

---

## Setup

### Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

### Install dependencies

```bash
# from the repo root
uv sync
```

Or install directly:

```bash
pip install anthropic openai langchain langgraph langchain-anthropic langchain-openai mcp fastmcp biopython pydantic redlines deepagents langchain_mcp_adapters openai-agents
```

### API keys

Create a `.env` file in this directory (a template is provided):

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
NCBI_EMAIL=your-email@example.com   # for PubMed/Entrez access
```

The notebooks load `.env` automatically with `python-dotenv`.

### Launch notebooks

```bash
jupyter lab
```

---

## Notebook Contents

| # | Notebook | Description | Key Topics |
|---|----------|-------------|------------|
| 01 | [GUI Agent Builders](01_gui_agent_builders.ipynb) | Explore three no-code platforms for building AI agents side-by-side, with a hands-on first agent in each | N8N visual workflows, Flowise RAG pipelines, AutoGen Studio multi-agent teams; comparison table; when to move to code |
| 02 | [Python Client SDKs](02_python_client_sdk.ipynb) | A "with vs. without" walkthrough of eight core agentic concepts across the Anthropic, OpenAI, and LangChain SDKs | Model tiers, system prompts, tool/function calling, in-context vs. checkpointer memory, streaming, structured output with Pydantic |
| 03 | [MCP Agents](03_mcp_agents.ipynb) | Bind Model Context Protocol servers to LLM agents so tools are discovered at runtime; includes building a custom PubMed MCP server | MCP architecture (stdio vs. HTTP), FastMCP server authoring, three binding patterns: Anthropic beta API, manual `ClientSession`, LangChain `MultiServerMCPClient` |
| 04 | [ReAct Agents](04_react_agents.ipynb) | Implement the ReAct loop (Thought → Action → Observation) for multi-step biomedical tool use, both with LangGraph's prebuilt agent and a raw SDK implementation | `create_react_agent`, `@tool` with Pydantic schemas, streaming intermediate steps, parallel tool calls, manual Anthropic tool-use message cycle |
| 05 | [Reflection — PGx Use Case](05_reflection_cpic_pgx.ipynb) | Apply the reflection pattern to pharmacogenomics drug dosing: generate a draft, retrieve CPIC guidelines, then refine — implemented in both LangChain LCEL and direct Anthropic SDK | CPIC diplotype → phenotype → recommendation pipeline, LCEL chains, V1→V2 diff with `redlines`, batch evaluation across 19 genes |
| 06 | [Multi-Agent Orchestration](06_multiagent_orchestration.ipynb) | Build a three-agent supervisor pipeline (Literature Summary → Critic → Supervisor) for automated scientific paper review, in three different SDKs | OpenAI Agents SDK `as_tool()`, Anthropic SDK tool-use loop, LangGraph `StateGraph`; SDK tradeoff comparison table |

---

## Supporting Files

| File | Purpose |
|------|---------|
| `server_pubmed.py` | Custom FastMCP server exposing PubMed search, abstract fetch, and full-text retrieval as MCP tools. Run with `python server_pubmed.py` (stdio transport). |
| `.env.example` | API key configuration (not committed — create your own .env from the example). |

---

## Contacts

For any suggestions and feedback to improve the tutorial, please feel free to submit a GitHub issue.

Should you have any further questions, feel free to reach out to Binglan Li (<bignlan.li@cshs.org>), Philip Freda (<Philip.Freda@csmc.edu>), or Jason H. Moore (<Jason.Moore@csmc.edu>).
