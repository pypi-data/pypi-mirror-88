import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-visualizer-JavierRodriguezPosada",
    version="0.0.2",
    author="Javier Rodriguez Posada",
    author_email="javiropos@gmail.com",
    description="App for data visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://javiropos.visualstudio.com/DataVisualizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy==1.19.3",
        "xlrd==1.2.0",
        "pandas==1.1.4",
        "dash==1.17.0"
    ],
    python_requires='>=3.9',
)