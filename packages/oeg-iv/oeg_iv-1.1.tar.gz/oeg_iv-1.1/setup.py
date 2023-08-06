"""
For pypi.org upload
"""
import setuptools


LONG = """
# oeg.iv

Python package for communication with OrgEnergoGaz InspectionViewer app
"""

setuptools.setup(
  name='oeg_iv',
  version='1.1',
  author='Vitaly Bogomolov',
  author_email='mail@vitaly-bogomolov.ru',
  description='Python package for communication with OrgEnergoGaz InspectionViewer app',
  long_description=LONG,
  long_description_content_type="text/markdown",
  url='https://github.com/vb64/oeg.iv',
  packages=['oeg_iv', 'oeg_iv.csvfile'],
  download_url='https://github.com/vb64/oeg.iv/archive/v1.1.tar.gz',
  keywords=['python', 'OrgEnergoGaz', 'InspectionViewer', 'csv'],
  classifiers=[
    "Programming Language :: Python",
    # https://autopilot-docs.readthedocs.io/en/latest/license_list.html
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
  ],
)
