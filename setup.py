from pathlib import Path

import setuptools

here = Path(__file__).parent


def read_requirements(path):
    try:
        with path.open(mode="rt", encoding="utf-8") as fp:
            return list(filter(bool, (line.split("#")[0].strip() for line in fp)))
    except IndexError:
        raise RuntimeError(f"{path} is broken")


requirements_base = read_requirements(here / "requirements" / "base.txt")
requirements_dev = read_requirements(here / "requirements" / "dev.txt")


setuptools.setup(
    name="aioauth_fastapi",
    version="0.0.1",
    author="Ali Aliyev",
    author_email="shamkir@gmail.com",
    description="aioauth FastAPI example",
    url="https://github.com/aliev/Async_API_sprint_1",
    package_dir={"aioauth_fastapi": "aioauth_fastapi"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements_base,
    extras_require={
        "dev": requirements_base + requirements_dev,
    },
)
