run_docker:
	docker-compose up

create_test_env_windows:
	python.exe -m venv venv
	venv\Scripts\python.exe -m pip install -r requirements.txt && venv\Scripts\python.exe test.py

freeze:
	pip freeze > requirements.txt 

backend:
	python.exe .\backend\server.py

.PHONY: backend freeze create_test_env_windows
