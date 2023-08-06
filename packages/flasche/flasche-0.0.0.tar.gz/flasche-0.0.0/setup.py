from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='flasche',
    version='0.0.0',
    description='flasche extends flask by prometheus-flask-exporter and swagger',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/deepshore/flasche',
    author='deepshore',
    author_email='github@deephore.de',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='flask, web',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'flasche=flasche.cli:main'
        ],
    }
)