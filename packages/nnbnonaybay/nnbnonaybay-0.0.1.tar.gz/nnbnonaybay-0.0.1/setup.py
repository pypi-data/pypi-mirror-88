import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nnbnonaybay',
    version='0.0.1',
    author='nonaybay',
    author_email='rafaelvenancio@protonmail.com',
    description='Basicão',
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
)
