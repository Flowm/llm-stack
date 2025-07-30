# LLM Stack

An all-in-one Docker Compose config for providing access to local and external LLMs with multiple chat interfaces.

## Components

* [Caddy](https://github.com/caddyserver/caddy): Acts as central entrypoint for the whole stack
* [Ollama](https://github.com/ollama/ollama): Provides access to local LLM models
* [LiteLLM](https://github.com/BerriAI/litellm): OpenAI compatible API proxy for local Ollama provided models and upstream models
* Multiple ChatGPT-style web interfaces for interacting with the LLM models

### Models

* Local (via [Ollama](https://ollama.com/search))
    * local-google-gemma3
    * local-llama3-8b
    * local-qwen3-30b
* [OpenAI](https://platform.openai.com/docs/models)
    * openai-gpt-4-turbo
    * openai-gpt-4o
    * openai-o3
    * openai-o4-mini
* [Google](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versioning)
    * google-gemini-1.5-pro
* [Anthropic](https://docs.anthropic.com/claude/docs/models-overview)
    * anthropic-claude-3-7-sonnet
    * anthropic-claude-4-0-sonnet
* [Groq](https://console.groq.com/docs/models)
    * groq-llama-3.3-70b
    * groq-llama-4-maverick

### Chat Frontends

* [Open WebUI](https://github.com/open-webui/open-webui)
* [NextChat](https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web)
* [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm)

## Getting Started

### Prerequisites

* Docker
* Docker Compose
* Git

### Setup

1. Clone this repository
1. Copy the default config `cp env.default .env` and `cp anythingllm.env.default .anythingllm.env`
1. Edit `.env` and add the relevant API keys
1. Start the Docker Compose configuration: `docker-compose up`
1. Access the Caddy webserver at `http://localhost:3000`
