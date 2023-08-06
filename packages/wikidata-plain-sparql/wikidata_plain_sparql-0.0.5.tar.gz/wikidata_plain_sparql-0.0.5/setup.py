import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='wikidata_plain_sparql',
    version='0.0.5',
    author='Jelle Schutter',
    author_email='jelle@schutter.xyz',
    description='Query WikiData in plain SPARQL and display the result as a map or data frame',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jelleschutter/wikidata-plain-sparql',
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'bokeh'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
