
VENV=.venv
BIN=$(VENV)/bin

help:
	...

$(VENV):
	virtualenv $(VENV) -p python3
	make install

install:
	$(BIN)/pip install -r requirements/dev.txt

clean: $(VENV)
	$(BIN)/autoflake --remove-all-unused-imports --ignore-init-module-imports --in-place -r pytest_agent/
	$(BIN)/isort pytest_agent/
	$(BIN)/black pytest_agent/

lint: $(VENV)
	$(BIN)/pylint pytest_agent/

serve: $(VENV)
	$(BIN)/uvicorn pytest_agent.api:api --host 0.0.0.0 --reload
