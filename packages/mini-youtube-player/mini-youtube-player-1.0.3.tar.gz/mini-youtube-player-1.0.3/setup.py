import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="mini-youtube-player",
    version="1.0.3",
    description="CLI youtube video search and play",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tobip/mini-youtube-player",
    author="Tobias Paar",
    author_email="tobip@users.noreply.github.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=["src"],
    # py_modules=['miniyoutubeplayer'],
    # packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["youtube-search-python", "termcolor", "pyperclip"],
    entry_points={
        "console_scripts": [
            "mini-youtube-player=src.__main__:main",
        ]
    },
    python_requires='>=3.4',
)
