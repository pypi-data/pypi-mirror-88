from setuptools import setup

setup(
    name='chronotco',
    version='0.0.1',    
    description='Python3 decorator for tail call optimization via bytecode injection.',
    url='https://github.com/the-chronomancer/chronotco',
    author='Jacob Coleman',
    author_email='chronomancy.io@gmail.com',
    license='Copyleft',
    packages=['chronotco'],
    install_requires=['dis',],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
    ],
)