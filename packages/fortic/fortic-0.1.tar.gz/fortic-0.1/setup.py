from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='fortic',
    packages=['fortic'],
    version='0.1',
    license='apache-2.0',
    description='Fortinet SSLVPN command line interface',
    author='Juergen Schmid',
    author_email='jur.schmid@gmail.com',
    url='https://github.com/hacki11/fortic',
    keywords=['vpn', 'fortinet', 'sslvpn', 'cli'],
    install_requires=[
        'click',
        'keepasshttp'
    ],
    entry_points={
        'console_scripts': ['fortic=fortic.fortic:main'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows'
    ],
)