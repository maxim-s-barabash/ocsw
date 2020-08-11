"""Setup script."""

try:
    from setuptools import setup as _setup
except ImportError:
    from distutils.core import setup as _setup
else:
    setup = _setup

from os import path

NAME = "ocsw"
ME = "Barabash Maxim"
ME_EMAIL = "maxim.s.barabash@gmail.com"
VERSION = None
CWD = path.abspath(path.dirname(__file__))

with open(path.join(CWD, NAME, "version.py")) as f:
    exec(f.read())

with open(path.join(CWD, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(CWD, "requirements.txt"), encoding="utf-8") as f:
    install_requires = [r.strip() for r in f if r and not r.startswith("#")]

setup(
    name=NAME,
    version=VERSION,
    zip_safe=True,
    description="Octave Cloud IoT Command Line Interface (CLI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=ME,
    author_email=ME_EMAIL,
    maintainer=ME,
    maintainer_email=ME_EMAIL,
    url="https://github.com/maxim-s-barabash/ocsw",
    project_urls={
        "Source": "https://github.com/maxim-s-barabash/ocsw",
        "Tracker": "https://github.com/maxim-s-barabash/ocsw/issues",
    },
    license="MIT License",
    keywords=["IoT", "octave", "cloud", "cli"],
    packages=[NAME],
    platforms=["Independent"],
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["ocsw-cli = ocsw.cli:main"]},
)
