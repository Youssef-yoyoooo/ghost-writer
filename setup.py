from setuptools import setup, find_packages

setup(
    name="ghost-writer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "typer",
        "gitpython",
        "langchain",
        "langchain-community",
        "docker",
        "rich",
        "pydantic",
        "python-dotenv",
        "questionary",
    ],
    entry_points={
        "console_scripts": [
            "ghost-writer=ghost_writer.cli:app",
        ],
    },
    author="Ghost-Writer Team",
    description="AI-generated code provenance tracking and risk assessment tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/user/ghost-writer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
