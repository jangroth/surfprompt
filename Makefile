.PHONY: help install-dependencies test

help: ## This help
	@grep -E -h "^[a-zA-Z_-]+:.*?## " $(MAKEFILE_LIST) \
	  | sort \
	  | awk -v width=36 'BEGIN {FS = ":.*?## "} {printf "\033[36m%-*s\033[0m %s\n", width, $$1, $$2}'

install-dependencies: ## Install pipenv and dependencies
	pip3 install pipenv
	pipenv install --dev

check: ## Run linters
	black --check --diff --color .
	yamllint -f parsable .
	@echo '*** all checks passing ***'

test: check ## Run tests
	PYTHONPATH=.:./src pytest --cov=src --cov-branch --cov-report term-missing ./tests
	@echo '*** all tests passing ***'
