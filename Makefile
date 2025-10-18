backend:
	venv/Scripts/activate && python.exe 


freeze:
	pip freeze -r > requirements.txt 