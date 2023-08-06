import setuptools


with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="xalglib",
    version="3.16.0",
    author="ALGLIB",
    description='ALGLIB is a cross-platform numerical analysis and data processing library',
    long_description=readme,
    license='GNU General Public License v3 (GPLv3)',
    python_requires='>=3.6',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	],
    include_package_data = True,
    packages = ['xalglib'],
    package_data={'xalglib': ['xalglib/alglib316_64free.dll', 'xalglib/alglib316_64free.so']},
)
