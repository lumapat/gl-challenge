.PHONY: test
test:
	@docker compose up -d
	@echo "Waiting for service to come up..."
	@until curl -s localhost:8000 > /dev/null; do sleep 1; echo "Service still unavailable..."; done
	@./tests.sh || true
	@docker compose down