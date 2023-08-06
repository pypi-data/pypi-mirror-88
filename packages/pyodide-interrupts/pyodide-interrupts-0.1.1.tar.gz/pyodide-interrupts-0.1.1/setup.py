from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyodide-interrupts",
    version="0.1.1",
    author="Hood Chatham",
    author_email="roberthoodchatham@gmail.com",
    description="Interrupt handling for pyodide.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SpectralSequences/pyodide_interrupts/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pyodide_interrupts"],
    ext_modules=[Extension("pyodide_interrupts._pyodide_interrupts", ["pyodide_interrupts/pyodide_interrupts.c"])]
    # python_requires='>=3.6',
)
