from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='EncodeURL',
    version='1.0.0',
    description='Encode url',
    url='',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Manoj Sitapara',
    author_email='manojsitapara@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Encode',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ]
)