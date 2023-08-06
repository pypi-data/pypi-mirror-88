from pathlib import Path
from setuptools import setup,find_packages

ROOT = Path(__file__).parent

README = (ROOT/'wdgaf/README.md').read_text()

setup(
        name = "WDGAF",
        version = "1.0.7",
        description = "We Do Give a Figure",
        long_description = README,
        long_description_content_type = "text/markdown",
        url = "https://github.com/rajp152k/Compilers-II",
        author = "WDGAF",
        author_email = "rajp152k@gmail.com",
        license = "MIT",
        classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.8",
            ],
        packages = find_packages(where='.',exclude=('tests','docs')),
        include_package_data=True,
        install_requires=["matplotlib","numpy","lark-parser"],
        entry_points={
            "console_scripts":[
                "gaf=wdgaf.__main__:main"
                ]
            },
        )
