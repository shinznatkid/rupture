from setuptools import setup, find_packages

version = '1.0.0'

packages = find_packages()

setup(
    name='rupture',
    version=version,
    description='A simple wrapper from requests and beautifulsoup.',
    author='Shinz Natkid',
    author_email='shinznatkid@gmail.com',
    url='http://readthedocs.org/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'requests>=1.0.0',
        'beautifulsoup4>=4.0.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
