from setuptools import setup, find_packages

__version__ = "0.0.2"

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name = "onnxds",
    version = __version__,
    description = "Create datasets using onnx and serialize tensorflow_datasets in onnx datasets.",
    long_description = readme(),
    long_description_content_type ="text/markdown",
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords = "",
    url = "https://github.com/mingkaic/onnxds",
    author = "Ming Kai Chen",
    author_email = "mingkaichen2009@gmail.com",
    license = "MIT",
    packages = find_packages(),
    install_requires = ['tensorflow', 'tensorflow_datasets'],
    test_suite = "",
    tests_require = [],
    zip_safe = False,
    python_requires = '>=3.6',
)
