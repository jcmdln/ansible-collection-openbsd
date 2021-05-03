from __future__ import annotations

from setuptools import find_packages, setup


def Open(target: str) -> str:
    with open(target) as f:
        return f.read()


setup(
    name="openbsd-run",
    version="0.1.0",
    description="",
    long_description=Open("README.md"),
    license=Open("LICENSE.md"),
    author="Johnathan C. Maudlin",
    author_email="jcmdln@gmail.com",
    url="https://github.com/jcmdln/openbsd.run",
    # Dependencies
    install_requires=Open("requirements.txt").splitlines(),
    extras_require={"devel": Open("requirements-devel.txt").splitlines()},
    # Package info
    packages=find_packages(include=["openbsd_run", "openbsd_run.*"]),
    package_data={"openbsd_run": ["*"]},
    include_package_data=True,
    entry_points={"console_scripts": ["openbsd-run=openbsd_run.main:cli"]},
)
