flake8:
	flake8 --doctest papersurfer/*.py papersurfer/ui/*.py tests/*.py

pylint:
	pylint papersurfer/*.py papersurfer/ui/*.py tests/*.py

pycodestyle:
	pycodestyle papersurfer/* papersurfer/ui/* tests/*

pydocstyle:
	pydocstyle papersurfer/* papersurfer/ui/* tests/*

pip-prepare:
	- rm -r dist
	python setup.py sdist
	tar tzf dist/papersurfer*.tar.gz
	twine check dist/*

pip-test: pip-prepare
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pip: pip-prepare
	twine upload dist/*

lint: flake8 pylint pycodestyle pydocstyle mypy

test:
	python -m pytest --doctest-modules -vv

coverage:
	python -m pytest --doctest-modules --cov=papersurfer --cov-branch

mypy:
	mypy --strict-optional --strict .

tox:
	tox