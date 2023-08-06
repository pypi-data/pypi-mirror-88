import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="mini-youtube-player",
    version="1.0.2",
    description="Search and play audio or video from youtube in cli",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/mini-youtube-player/",
    author="Tobias Paar",
    author_email="mini-youtube-player@pato.at",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=["miniyoutubeplayer"],
    # py_modules=['miniyoutubeplayer'],
    # packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["youtube-search-python", "termcolor"],
    entry_points={
        "console_scripts": [
            "miniyoutubeplayer=miniyoutubeplayer.__main__:main",
        ]
    },
    python_requires='>=3.4',
)
