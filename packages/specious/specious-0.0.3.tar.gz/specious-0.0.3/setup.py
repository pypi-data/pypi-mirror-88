import sys

from setuptools import setup
from pathlib import Path


assert sys.version_info >= (3, 8, 0), "specious requires Python 3.8+"

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))


def readme() -> str:
    return (CURRENT_DIR / "README.md").read_text(encoding="utf8")


setup(
    name="specious",
    packages=["specious"],
    version="0.0.3",
    author="aquichita",
    author_email="chaochao.wu@outlook.com",
    description="Just screenshot allure report and send.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=[
        "webdriver-manager",
        "keyring",
        "yagmail",
        "selenium",
    ],
    url="https://github.com/aquichita/specious",
    include_package_data=True,
    tests_require=["pytest", "pytest-cov", "pytest-sugar"],
    python_requires=">=3.8",
)
