from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rwdq",
    version="0.1.2",
    author="Zhu Xiangju",
    author_email="zhuxiangjv@gmail.com",
    description="A tool for querying real-world graph database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zxj0302/rwdq",
    packages=find_packages(),
    install_requires=[
        'torch',
        'torch_geometric',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'graph_query=rwdq.main:main',
        ],
    },
)