from pathlib import Path

from setuptools import setup

here = Path(__file__).parent

about = {}

with open(here / "aioauth_fastapi" / "__version__.py", "r") as f:
    exec(f.read(), about)


with open("README.md") as readme_file:
    readme = readme_file.read()


require_dev = [
    "fastapi==0.70.1",
    "aioauth==1.3.0",
    "uvicorn==0.16.0",
    "wheel",
    "twine==3.7.1",
    "pydantic[dotenv]==1.8.2",
    "asyncpg==0.25.0",
    "SQLAlchemy[asyncio]==1.4.28",
    "orjson==3.6.5",
    "python-jose[pycryptodome]==3.3.0",
    "python-multipart==0.0.5",
    "alembic==1.7.5",
    "sqlmodel==0.0.5",
    "async-asgi-testclient==1.4.9",
    "pre-commit==2.16.0",
    "pytest==6.2.5",
    "pytest-asyncio==0.16.0",
    "pytest-cov==3.0.0",
    "pytest-env==0.6.2",
    "pytest-sugar==0.9.4",
    "testfixtures==6.18.3",
    "bump2version==1.0.1",
]

classifiers = [
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development",
    "Typing :: Typed",
    "Development Status :: 1 - Planning",
    "Environment :: Web Environment",
    "Framework :: AsyncIO",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Internet :: WWW/HTTP",
]


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    python_requires=">=3.6.0",
    classifiers=classifiers,
    extras_require={
        "dev": require_dev,
    },
    include_package_data=True,
    keywords="asyncio oauth2 oauth fastapi",
    packages=["aioauth_fastapi"],
    package_dir={"aioauth_fastapi": "aioauth_fastapi"},
    project_urls={"Source": about["__url__"]},
)
