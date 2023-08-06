import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def local_scheme(version):
    return ""

setuptools.setup(
    name='summa-testing-framework-summasolutions',
    # version='0.1.16',
    author='Summa Solutions',
    author_email='coreteam@summasoutions.net',
    description='Summa Solutions Testing Framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/summasolutions/summa-testing-framework",
    py_modules=['stf'],
    use_scm_version={
        "local_scheme": local_scheme,
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'Click',
        'click_help_colors',
        'colorama',
        'pyunitreport',
        'PyYAML',
        'selenium',
        'Faker',
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points='''
        [console_scripts]
        stf=stf.cli:cli
    ''',
    python_requires='>=3.6',
)
