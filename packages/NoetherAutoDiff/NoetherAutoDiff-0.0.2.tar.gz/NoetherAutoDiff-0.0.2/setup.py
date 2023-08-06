import pathlib
from setuptools import setup

# current dir
HERE = pathlib.Path(__file__).parent

# add readme
# # README = (HERE / "README.md").read_text()

setup(
    name='NoetherAutoDiff',
    packages=['NoetherAutoDiff'],
    version='0.0.2',
    license='MIT',
    description='A Python wrapper for an efficient C++ library that is used for Auto Differentiation',
    # long_descripti?on=README,
    #long_description_content_type='text/markdown',
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
