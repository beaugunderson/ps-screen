from setuptools import setup

setup(
    name='ps-screen',
    version='1.0.3',
    author='Beau Gunderson',
    author_email='beau@beaugunderson.com',
    url='https://github.com/beaugunderson/ps-screen',
    description="List screen and tmux sessions and what's running in them.",
    long_description=open('README.rst').read(),
    license='BSD',
    keywords='utility ps screen tmux',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    py_modules=['ps_screen'],
    entry_points={
        'console_scripts': [
            'ps-screen = ps_screen:ps_screen',
        ]
    },
    install_requires=[
        'click>=3.3',
        'psutil>=2.1.3',
        'tabulate>=0.7.3',
    ]
)
