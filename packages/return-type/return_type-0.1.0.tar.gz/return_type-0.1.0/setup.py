from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="return_type",
    version="0.1.0",
    description="Generic type ReturnType and mypy checker plugin",
    author="Dimitri.WEI",
    author_email="dimitri.wei.lingfeng@gmail.com",
    url="https://github.com/wlf100220/return_type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["mypy"],
    python_requires=">=3.8",
)
