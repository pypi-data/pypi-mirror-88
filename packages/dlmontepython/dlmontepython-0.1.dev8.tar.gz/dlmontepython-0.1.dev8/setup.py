
from setuptools import setup, find_packages

# Use contents of README as the long_description for release
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(name = 'dlmontepython',
      version = '0.1.dev8',
      description = 'Tools associated with the Monte Carlo simulation program DL_MONTE',
      long_description = long_description,
      long_description_content_type='text/markdown',
      url = "https://gitlab.com/dl_monte/dlmontepython",
      license = "BSD License (BSD-3-Clause)",
      install_requires = ['numpy', 'matplotlib', 'scipy', 'pyyaml'],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering"
      ],
      include_package_data = True,
      packages = find_packages()
)
