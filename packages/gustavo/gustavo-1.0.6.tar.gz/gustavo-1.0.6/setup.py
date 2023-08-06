import setuptools

with open(".github/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gustavo",
    version="1.0.6",
    author="Anthony Slater",
    author_email="slaterslater@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slaterslater/gustavo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["gus", "gus.args", "gus.const", "gus.out", "gus.urls"],
    install_requires=["requests", "progress"],
    entry_points={
        "console_scripts": [
            "gus = gus.__main__:main",
        ]
    },
)
