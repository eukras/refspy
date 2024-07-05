demo:
	python demo.py > demo.html

docs:
	pdoc refspy/ -d google -o docs

init:
	pip install -r requirements.txt

test:
	python -m pytest tests
