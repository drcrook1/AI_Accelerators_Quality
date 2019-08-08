from setuptools import setup, find_packages
import io
import os
import sys

NAME = "ai_acc_quality"
AUTHOR = "Microsoft Corporation"
AUTHOR_EMAIL = "dacrook@microsoft.com"
DESCRIPTION = "DO LATER"
PROJECT_URL = "PRIVATE"
LICENSE = "Restricted"
version = "0.0.0"

if sys.version_info <= (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
    sys.exit(1)

if("--version" in sys.argv):
    idx = sys.argv.index("--version")
    arg_name = sys.argv.pop(idx)
    version = sys.argv.pop(idx)
print(version)

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name = NAME,
    version = version,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    description = DESCRIPTION,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[
          'python-dateutil',
          'scikit-learn==0.20.3',
          'torch==1.1.0',
          'joblib',
      ]
)
