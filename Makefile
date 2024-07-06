build:
	python -m build

demo:
	python demo.py > demo.html

docs:
	pdoc refspy/ -d google -o docs

init:
	pip install -r requirements.txt

publish:
	twine upload dist/*

test:
	python -m pytest tests
