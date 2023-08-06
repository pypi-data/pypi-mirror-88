import os
import sys
import codecs
from setuptools import setup

if sys.version_info < (3, 6, 0):
    raise RuntimeError('Python 3.6 or higher is required')

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='bpmscan',
    version='0.1.2',
    description='Measures heart rate of multiple person realtime from Webcamera, IPCamera and also from from Uploaded video',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['bpmscan'],
    url='https://github.com/coderganesh/heartpi',
    author='Ganesh Kumar T K',
    author_email='ganeshkumartk@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='rPPG heartbeat webcam',
    entry_points={
        'console_scripts': [
            'bpmscan=bpmscan.app:main',
        ]
    },
    package_data={'bpmscan': ['data/*.xml']},
    install_requires=[
        'PyQt5', 'PyQtChart', 'numpy', 'eventkit', 'scipy', 'opencv-python'],
)
