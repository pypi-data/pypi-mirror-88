import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pricelist-parser',
    version='0.2',
    author='Artem Kiselev',
    author_email='artem.kiselev@gmail.com',
    description='Pricelist parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wondersell/pricelist-parser',
    packages=setuptools.find_packages(),
    install_requires=[
        'price-parser >= 0.3.3',
        'xlrd',
        'openpyxl',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
