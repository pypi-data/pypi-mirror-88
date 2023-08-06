from setuptools import setup, find_packages

setup(
    name='tsquery',
    version='0.1.1',

    author='Greg Werbin',
    author_email='software@me.gregwerbin.com',
    license='GPL-3.0-or-later',

    url='https://sr.ht/~wintershadows/tsquery',
    description='Run Tree Sitter queries from the command line',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={'console_scripts': ['tsquery = tsquery.__main__:cli']},

    # Use MANIFEST.in to include "py.typed" file
    include_package_data=True,
    zip_safe=False,

    python_requires='>=3.9',
    install_requires=[
        'attrs >= 20',
        'click >= 7',
        'tree_sitter >= 0.2.0',
    ],
)
