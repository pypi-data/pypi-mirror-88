import os
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 7, 0):
    sys.exit("Python 3.7.0 is the minimum required version")

PROJECT_ROOT = os.path.dirname(__file__)

about = {}
with open(os.path.join(PROJECT_ROOT, "src", "quart", "__about__.py")) as file_:
    exec(file_.read(), about)

with open(os.path.join(PROJECT_ROOT, "README.rst")) as file_:
    long_description = file_.read()

INSTALL_REQUIRES = [
    "aiofiles",
    "blinker",
    "click",
    "hypercorn >= 0.7.0",
    "itsdangerous",
    "jinja2",
    "toml",
    "typing_extensions; python_version < '3.8'",
    "werkzeug >= 1.0.0",
]

setup(
    name="Quart",
    version=about["__version__"],
    python_requires=">=3.7.0",
    description="A Python ASGI web microframework with the same API as Flask",
    long_description=long_description,
    url="https://gitlab.com/pgjones/quart/",
    author="P G Jones",
    author_email="philip.graham.jones@googlemail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=["quart"],
    install_requires=INSTALL_REQUIRES,
    tests_require=INSTALL_REQUIRES + ["hypothesis", "mock", "pytest", "pytest-asyncio"],
    extras_require={"dotenv": ["python-dotenv"]},
    entry_points={"console_scripts": ["quart=quart.cli:main"]},
    include_package_data=True,
)
