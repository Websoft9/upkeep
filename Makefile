# UpKeep — developer tasks
SHELL := /bin/bash

# opencode CLI (override with: make opencode OPENCODE=/path/to/opencode)
OPENCODE ?= opencode

# Proxy variables commonly injected by the shell / container environment.
# opencode has no native proxy flag, so these are stripped before launching it.
PROXY_VARS := http_proxy https_proxy ftp_proxy all_proxy \
              HTTP_PROXY HTTPS_PROXY FTP_PROXY ALL_PROXY

# Builds: env -u http_proxy -u https_proxy ...
UNSET_PROXIES := $(foreach v,$(PROXY_VARS),-u $(v))

# Extra CLI args, e.g. make opencode ARGS="--model anthropic/claude-sonnet-4-5"
ARGS ?=

.DEFAULT_GOAL := help

.PHONY: help opencode api-install api-run api-seed docker-build docker-run

help: ## Show available targets
	@grep -hE '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

opencode: ## Launch opencode with all proxies disabled (noproxy)
	@echo "→ opencode (noproxy)"
	@env $(UNSET_PROXIES) NO_PROXY='*' no_proxy='*' $(OPENCODE) $(ARGS)

api-install: ## Create venv and install API dependencies
	python3 -m venv .venv
	.venv/bin/pip install -e .

api-run: ## Run the FastAPI development server
	.venv/bin/uvicorn app.main:app --reload

api-seed: ## Seed demo telemetry and recommendations
	.venv/bin/python -m app.seed

docker-build: ## Build the API container image
	docker build -t upkeep:dev .

docker-run: ## Run the API container on port 8000
	docker run --rm -p 8000:8000 upkeep:dev
