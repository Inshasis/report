from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in report/__init__.py
from report import __version__ as version

setup(
	name="report",
	version=version,
	description="Report",
	author="hidayat",
	author_email="hidayat@inshasis.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
