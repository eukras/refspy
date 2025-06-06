# PUBLISH

To publish a set of changes, check: 

```
pytest
pdoc refspy/ -d google -o docs
python demo.py
```

Review `/docs` and `demo/{LOCALE}.html`.

Screenshot `demo/{LOCALE}.html` and save to `media/refspy-demo-{LOCALE}.png`.

If all OK, update version numbers in config and docs:

```
vim pyproject.toml README.md
git commit pyproject.toml README.md -m "Version {VERSION_NUMBER}"
git push
```

Push to Github and PyPI.

```
python -m build
twine upload dist/refspy-{VERSION_NUMBER}*
```
