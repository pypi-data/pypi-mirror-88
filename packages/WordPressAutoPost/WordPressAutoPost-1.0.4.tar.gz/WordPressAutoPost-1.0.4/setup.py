from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='WordPressAutoPost',
    version='1.0.4',
    description='WordPress auto post package',
    url='',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Manoj Sitapara',
    author_email='manojsitapara@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='WordPress',
    packages=find_packages(),
    install_requires=[
        'ProductDetailFinder>=1.0.1',
        'tldextract>=3.1.0',
        'affiliatelinkconverter>=1.0.6',
        'python-wordpress-xmlrpc>=2.3',
    ]
)