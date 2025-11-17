build: 
	python -m build

demo:
	python demo.py

docs: refspy/
	pdoc refspy/ -d google -o docs

init: requirements.txt
	pip install -r requirements.txt

publish: dist/
	twine upload dist/*

test: tests/
	python -m pytest tests

cloc: refspy/
	cloc *.py *.toml *.md refspy tests
