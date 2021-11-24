import setuptools

setuptools.setup(
    name="pytest_agent",
    description="",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=["click", "fastapi", "uvicorn", "sqlalchemy"],
    entry_points={"console_scripts": ["pytest-agent=pytest_agent.__main__:cli"]},
)
