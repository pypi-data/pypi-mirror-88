import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


# print(setuptools.find_packages('py_playlist'))
# print(setuptools.find_packages('src'))
# raise Exception()

setuptools.setup(
    name="py_playlist",
    version="0.0.3",
    author="Gustavo Henrique Spiess",
    author_email="gustavospiess@gmail.com",
    description="A playlist manager for terminal based players",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustavospiess/py-playlist",
    package_dir={'':'src'},
    # packages=setuptools.find_packages('py_playlist'),
    packages=['py_playlist'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    install_requires=['click>=7.1.2', 'click-aliases>=1.0.1'],
    entry_points={
        'console_scripts': [
            'py_playlist=py_playlist.__main__:main',
            'ppl=py_playlist.__main__:main',
        ],
    },
)
