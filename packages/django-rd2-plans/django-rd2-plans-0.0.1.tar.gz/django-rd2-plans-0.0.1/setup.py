import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-rd2-plans',
    version='0.0.1',
    author='Alessandra Carneiro',
    author_email='alessandra@rd2.ventures',
    description='Base de modelos de planos usados na RD2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alessandrak/django-rd2-plans',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 3.1',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
