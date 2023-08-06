# git pull
# test hbar.py using command I
# update README.md
# update version number in setuptools.setup
# python setup.py sdist bdist_wheel
# twine upload dist/* -u diego51
# rm -r build dist *.egg-info
# pip install hbar -U
# test module in nteract
# git commit and push
# https://pypi.org/project/hbar
# https://github.com/dw61/hbar

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="electronvolt",
    version="0.0.1",
    author_email="lw7jz@virginia.edu",
    description="A physical quantity calculator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dw61/hbar",
    py_modules=["hbar"],
    python_requires='>=3.6',
)
