from setuptools import setup, find_packages

setup(
    name="speedtest-pypy",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
    ],
    entry_points={
        'console_scripts': [
            'speedtest++=speedtest-pypy.cli:main',
        ],
    },
    author="cociweb",
    description="Python implementation of SpeedTest++",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cociweb/speedtest-pypy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)