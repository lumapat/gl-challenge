.PHONY: e2e-test
e2e-test:
	@docker compose up --build -d
	@echo "Waiting for service to come up..."
	@until curl -s localhost:8000 > /dev/null; do sleep 1; echo "Service still unavailable..."; done
	@./e2e-tests.sh || true
	@docker compose down

unit-test:
	@python3 -m pytest tests/unit/*.py -v

run:
	@docker compose up --build -d

stop:
	@docker compose down