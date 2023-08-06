import os
import io
import setuptools


name = "tmg-etl-pipeline"
description = "TMG ETL pipeline"
version = "0.0.5"
dependencies = [
    "google-cloud-secret-manager==1.0.0",
    "PyYAML==5.3.1"
]

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()


setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author='TMG Data Platform team',
    author_email="data.platform@telegraph.co.uk",
    license="Apache 2.0",
    url='https://github.com/telegraph/tmg-etl-pipeline',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    python_requires='>=3.6',
)
