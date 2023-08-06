import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gisansexplorer", # Replace with your own username
    version="0.0.10",
    #scripts=['pippo.bat', 'pippo.py', 'pippo'],
    #scripts=['pippo.py', 'pippo'],
    #console=['pippo'],
    author="Juan M. Carmona Loaiza",
    author_email="j.carmona.loaiza@fz-juelich.de",
    description="Nicos data reduction and visualisation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juanmcloaiza/gisansexplorer",
    #packages=setuptools.find_packages(),
    packages=['gisansexplorer'],
    package_dir={'gisansexplorer': 'gisansexplorer'},
    package_data={'gisansexplorer': ['resources/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
    'console_scripts':
        ['pippo=gisansexplorer:entry_point']
                },
    python_requires='>=3.6',
    #data_files=[('resources', ['resources/Icon.png', 'resources/show_test_map.npy'])]#,
                #('test_data', ['notToVersion/Archive/*.dat'])],
    #package_data={
    #    'gisansexplorer': ['gisansexplorer/resources/show_test_map.npy'],
    #}
)