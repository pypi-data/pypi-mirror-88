import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xmrig-auto-throttler",  # Replace with your own username
    version="0.0.1",
    author="Dino Hensen",
    author_email="dino.hensen+xmrigthrottle@gmail.com",
    description="Program that switches between xmrig profiles according to your computer usage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhensen/xmrig-auto-idle-throttler",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "pylint",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "xmrig-auto-throttler = xmrig_auto_throttler.__main__:main"
        ],
    },
)
