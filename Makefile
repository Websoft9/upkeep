# UpKeep — developer tasks
SHELL := /bin/bash

# --- Configuration -----------------------------------------------------------

# opencode CLI (override with: make opencode OPENCODE=/path/to/opencode)
OPENCODE ?= opencode

# Directory used by link-cli to expose the CLI on PATH.
BIN_DIR ?= /usr/local/bin

# Extra CLI args, e.g. make opencode ARGS="--model anthropic/claude-sonnet-4-5"
ARGS ?=

# Ports used by the run targets. Override any single service with PORT, e.g.
#   make api-run PORT=8001
# or set a per-service default, e.g. make web-run WEB_PORT=4000.
PORT ?=
API_PORT ?= 8000
WEB_PORT ?= 3000
DOCS_PORT ?= 3000

# Resolve the port for a service: explicit PORT wins, otherwise the default.
api_port = $(or $(PORT),$(API_PORT))
web_port = $(or $(PORT),$(WEB_PORT))
docs_port = $(or $(PORT),$(DOCS_PORT))

# Proxy variables commonly injected by the shell / container environment.
# opencode has no native proxy flag, so these are stripped before launching it.
PROXY_VARS := http_proxy https_proxy ftp_proxy all_proxy \
              HTTP_PROXY HTTPS_PROXY FTP_PROXY ALL_PROXY

# Builds: env -u http_proxy -u https_proxy ...
UNSET_PROXIES := $(foreach v,$(PROXY_VARS),-u $(v))

.DEFAULT_GOAL := help

.PHONY: help stop api web docs \
        api-install api-run api-seed \
        cli link-cli unlink-cli \
        docs-install docs-run docs-build \
        web-install web-run web-build \
        docker-build docker-run \
        opencode

# --- Targets -----------------------------------------------------------------

##@ General

help: ## Show this help
	@printf '\n  \033[1mUpKeep\033[0m — developer tasks\n\n'
	@printf '  Usage: \033[36mmake\033[0m <target> [\033[36mPORT\033[0m=<port>] [\033[36mARGS\033[0m="..."]\n'
	@awk 'BEGIN {FS = ":.*## *"} /^##@ / { printf "\n  \033[1;36m%s\033[0m\n", substr($$0, 5); next } /^[a-zA-Z0-9_-]+:.*## / { printf "    \033[36m%-16s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@printf '\n'

##@ Lifecycle

# `make stop` stops every dev server; `make stop api` stops just one.
stop: ## Stop dev servers: make stop [api|web|docs]
	@services="$(filter-out stop,$(MAKECMDGOALS))"; \
	if [ -z "$$services" ]; then services="api docs web"; fi; \
	for svc in $$services; do \
		case "$$svc" in \
			api)  port=$(api_port)  ;; \
			web)  port=$(web_port)  ;; \
			docs) port=$(docs_port) ;; \
			*) echo "unknown service: $$svc (expected api, web, or docs)"; exit 1 ;; \
		esac; \
		pids=$$(lsof -ti tcp:$$port 2>/dev/null); \
		if [ -n "$$pids" ]; then \
			echo "  stopping $$svc on port $$port: $$pids"; \
			kill $$pids 2>/dev/null || true; \
			sleep 1; \
			kill -9 $$pids 2>/dev/null || true; \
		else \
			echo "  $$svc: nothing listening on port $$port"; \
		fi; \
	done

# Argument carriers for `make stop api|web|docs`; no-op when stop is a goal.
api web docs:
	@if [ -z "$(filter stop,$(MAKECMDGOALS))" ]; then echo "hint: use 'make stop $@'"; exit 1; fi

##@ API

api-install: ## Create venv and install API dependencies
	python3 -m venv .venv
	.venv/bin/pip install -e .

api-run: ## Run the FastAPI dev server (default port 8000)
	.venv/bin/uvicorn app.main:app --reload --port $(api_port)

api-seed: ## Seed demo telemetry and recommendations
	.venv/bin/upkeep seed

##@ CLI

cli: ## Run the UpKeep CLI (e.g. make cli ARGS="robots list")
	@test -x .venv/bin/upkeep || $(MAKE) --no-print-directory api-install
	@.venv/bin/upkeep $(ARGS)

link-cli: ## Symlink upkeep/uk onto PATH (default BIN_DIR=/usr/local/bin)
	@test -x .venv/bin/upkeep || $(MAKE) --no-print-directory api-install
	@ln -sf "$(CURDIR)/.venv/bin/upkeep" "$(BIN_DIR)/upkeep"
	@ln -sf "$(CURDIR)/.venv/bin/uk" "$(BIN_DIR)/uk"
	@echo "linked: $(BIN_DIR)/upkeep -> $(CURDIR)/.venv/bin/upkeep"
	@echo "linked: $(BIN_DIR)/uk -> $(CURDIR)/.venv/bin/uk"

unlink-cli: ## Remove the upkeep/uk symlinks from PATH
	@rm -f "$(BIN_DIR)/upkeep" "$(BIN_DIR)/uk"
	@echo "removed: $(BIN_DIR)/upkeep, $(BIN_DIR)/uk"

##@ Documentation

docs-install: ## Install documentation dependencies (Docusaurus)
	npm --prefix docs install

docs-run: ## Run the docs dev server (default port 3000)
	npm --prefix docs run start -- --port $(docs_port)

docs-build: ## Build the static documentation site
	npm --prefix docs run build

##@ Web

web-install: ## Install Next.js frontend dependencies
	cd web && npm install

web-run: ## Run the Next.js frontend (default port 3000)
	cd web && npm run dev -- -p $(web_port)

web-build: ## Build the Next.js frontend
	cd web && npm run build

##@ Docker

docker-build: ## Build the API container image
	docker build -f docker/Dockerfile -t upkeep:dev .

docker-run: ## Run the API container (default port 8000)
	docker run --rm -p $(api_port):8000 upkeep:dev

##@ Development

opencode: ## Launch opencode with all proxies disabled (noproxy)
	@echo "→ opencode (noproxy)"
	@env $(UNSET_PROXIES) NO_PROXY='*' no_proxy='*' $(OPENCODE) $(ARGS)
