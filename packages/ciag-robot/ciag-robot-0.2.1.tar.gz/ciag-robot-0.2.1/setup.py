import os

from setuptools import setup, find_packages

__version__ = '0.2.1'


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


def read_requirements(file_name):
    lines = filter(None, read(file_name).splitlines())
    for line in lines:
        if line.startswith('#'):
            continue
        if line.startswith('-'):
            continue
        if ';' in line:
            line, _ = line.split(';', 1)
        yield line


requirements = read_requirements('requirements.txt')
requirements_dev = read_requirements('requirements-dev.txt')

setup(
    name='ciag-robot',
    version=__version__,
    description='Python Library to Build Web Robots',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/OpenCIAg/py-robot',
    download_url='https://github.com/OpenCIAg/py-robot/tree/%s/' % __version__,
    license='CLOSED',
    author='Éttore Leandro Tognoli',
    author_email='ettore.tognoli@ciag.org.br',
    data_files=[
        'requirements.txt',
        'requirements-dev.txt',
    ],
    packages=find_packages(
        './src/main/python/',
    ),
    package_dir={'': 'src/main/python'},
    include_package_data=True,
    keywords=['Robot', 'Web Crawler'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=list(requirements),
    tests_require=list(requirements_dev),
)
