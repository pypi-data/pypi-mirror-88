from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ProductDetailFinder',
    version='1.0.0',
    description='Amazon Flipkart product detail finder',
    url='',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Manoj Sitapara',
    author_email='manojsitapara@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Amazon Flipkart',
    packages=find_packages(),
    install_requires=[
        'tldextract>=3.1.0',
        'python-amazon-paapi>=3.3.1',
    ]
)