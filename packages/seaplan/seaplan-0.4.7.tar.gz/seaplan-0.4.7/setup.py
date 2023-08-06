import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

version = {}
with open("seaplan/version.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="seaplan",
    version=version['__version__'],
    author="Wayne Crawford",
    author_email="crawford@ipgp.fr",
    description="Sea-going mission planning",
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    url="https://github.com/WayneCrawford/seaplan",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'numpy>=1.18',
          'scipy>=1.4',
          'matplotlib>=3.0',
          'cartopy>=0.16',
          'pyyaml>=3.0',
          'xarray>0.16',
          'jsonschema>=2.6',
          'docutils>=0.16',
          'jsonref>=0.2'
      ],
    entry_points={
         'console_scripts': [
             'seaplan=seaplan.sea_plan:main',
             'seaplan-validate=seaplan.validate_json:_console_script'
         ]
    },
    python_requires='>=3.7',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    keywords='oceanography, marine, OBS'
)
