import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='func_adl_uproot',
                 version='1.0',
                 description=('Functional Analysis Description Language'
                              + ' uproot backend for accessing flat ROOT ntuples'),
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(exclude=['tests']),
                 python_requires=('>=2.7, '
                                  '!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <3.10'),
                 install_requires=['awkward>=1',
                                   'numpy',
                                   'qastle>=0.10',
                                   'uproot>=4'],
                 author='Mason Proffitt',
                 author_email='masonlp@uw.edu',
                 url='https://github.com/iris-hep/func_adl_uproot')
