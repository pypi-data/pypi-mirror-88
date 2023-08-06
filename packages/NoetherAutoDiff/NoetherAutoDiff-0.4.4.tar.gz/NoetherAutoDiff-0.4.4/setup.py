import pathlib
from setuptools import setup, find_packages, Extension
import os
import sys

# current dir
#curr_dir = parent_dir = os.path.dirname(os.path.realpath(__file__))
##parent_dir = os.path.dirname(curr_dir)
#src_dir = parent_dir + os.sep + "src"
#main_cpp_file = src_dir + os.sep + "Python" + os.sep + "NoetherADPy.cpp"

# add readme
# readme_file = curr_dir + os.sep + "README.md"
# README = (readme_file).read_text()

# extension = Extension("NoetherAutoDiff.ext_lib", ["src/Python/NoetherADPy.cpp"], include_dirs=["src"])

setup(
    name='NoetherAutoDiff',
    packages=['NoetherAutoDiff'],
    # ext_modules=[extension],
    version='0.4.4',
    license='MIT',
    description='A Python wrapper for an efficient C++ library that is used for Auto Differentiation',
    # long_description=README,
    # long_description_content_type='text/markdown',
    author='Sam Negassi',
    author_email='samson.s.negassi@gmail.com',
    url='https://github.com/cs107-noether/cs107-FinalProject',
    download_url='https://github.com/cs107-noether/cs107-FinalProject/archive/v0.1.tar.gz',
    keywords=['Auto', 'Differentiation', 'AutoDiff', 'Jacobian', 'Derivation'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

