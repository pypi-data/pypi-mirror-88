import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='py2sqlite-ehortl',
    packages=['py2sqlite'],
    version='0.0.3',
    license='mit',
    description='Package to work with SQLite',
    author='Yaroslav Haidai, Yehor Polishchuk',
    author_email='e-dp@ukr.net',
    url='https://github.com/ehorTL/py2sqlite',
    keywords=['py2sqlite', 'SQLite', 'Py2SQL', 'SQL'],
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
