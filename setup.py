from setuptools import setup, find_packages, Extension

setup(
    name = 'mykmeanssp',
    version = '0.0.1',
    author = 'Ben_&_Ofek',
    author_email = 'email',
    description = 'connectin kmeans.c to python program',
    packages = find_packages(),
    license = 'none',

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programing Language :: Python :: 3 :: only',
        'Programing Language :: Python :: Implementaion :: CPython',
    ],
    ext_modules=[
        Extension(
            'mykmeanssp',
            ['kmeans.c'],
        ),
    ]
)