# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crystal',
 'data',
 'fileio',
 'fileio.loaders',
 'instrument',
 'loaders',
 'lsfit',
 'neutronpy',
 'neutronpy.crystal',
 'neutronpy.data',
 'neutronpy.fileio',
 'neutronpy.fileio.loaders',
 'neutronpy.instrument',
 'neutronpy.lsfit',
 'neutronpy.scattering',
 'scattering']

package_data = \
{'': ['*'], 'neutronpy': ['database/*', 'ui/*']}

install_requires = \
['h5py>=3.1.0,<4.0.0',
 'lmfit>=0.9.5,<0.10.0',
 'matplotlib>=2.0,<3.0',
 'numpy>=1.10,<2.0',
 'scipy>=1.0,<2.0']

entry_points = \
{'console_scripts': ['neutronpy = neutronpy.gui:launch']}

setup_kwargs = {
    'name': 'neutronpy',
    'version': '2.0.0',
    'description': 'NeutronPy is a collection of commonly used tools aimed at facilitating the analysis of neutron scattering data. NeutronPy is built primarily using the numpy and scipy python libraries, with a translation of ResLib 3.4c (MatLab) routines for Instrument resolution calculations.',
    'long_description': 'NeutronPy\n=========\n\nNeutronPy is a python library with commonly used tools for neutron scattering measurements, primarily for Triple Axis Spectrometer data, but easily applied to other types of data, including some *reduced* Time of Flight data. Below is a non-exhaustive list of Neutronpy\'s features:\n\n    * Triple Axis Spectrometer resolution function calculation (Translated from ResLib), including\n        * Resolution ellipses\n        * Instrument visualization\n        * Convolution\n    * Time of Flight Spectrometer resolution function calculation (based on Violini et al `doi:10.1016/j.nima.2013.10.042 <https://doi.org/10.1016/j.nima.2013.10.042>`_ ), including\n        * Resolution ellipses\n    * Structure factor calculation, including\n        * Structure factors with support for\n            * Mass Normalization\n            * Debye-Waller factor\n            * Unit cell visualization\n        * Single-ion magnetic form factor calculation\n    * Least-Squares fitting (custom interface for scipy.optimize.leastsq using lmfit features), including\n        * Built-in physical models\n    * Basic data operations\n        * Binning\n        * Normalization (time/monitor)\n        * Calculated peak integrated intensity, position, and width\n        * Plotting\n        * Slicing\n    * Loading from common TAS file types, including\n        * SPICE\n        * ICE\n        * ICP\n        * MAD\n\n\nSee `Roadmap <https://github.com/neutronpy/neutronpy/wiki/Roadmap>`_ for panned future features.\n\nDavid M Fobes started development of NeutronPy while in the `Neutron Scattering Group <http://neutrons.phy.bnl.gov/>`_, part of the Condensed Matter Physics & Materials Science Department (CMPMSD) at `Brookhaven National Laboratory <http://www.bnl.gov/>`_, and has continued within the `MPA-CMMS <http://www.lanl.gov/org/padste/adeps/materials-physics-applications/condensed-matter-magnet-science>`_ and A-1 groups of `Los Alamos National Laboratory <http://www.lanl.gov/>`_. Both are `US Department of Energy, Office of Basic Energy Sciences <http://science.energy.gov/bes/>`_ funded laboratories.\n\nNeutronPy is a work-in-progress (see the `Roadmap <https://github.com/neutronpy/neutronpy/wiki/Roadmap>`_ in the wiki for indications of new upcoming features) and as such, still has many bugs, so use at your own risk; see Disclaimer. To report bugs or suggest features see Contributions.\n\nRequirements\n------------\nThe following packages are required to install this library:\n\n* ``Python >= 3.6``\n* ``numpy >= 1.10.0``\n* ``scipy >= 1.0.0``\n* ``lmfit >= 0.9.5``\n* ``matplotlib >= 2.0.0``\n* ``h5py``\n\nThe following package is required to use the ``neutronpy`` entry-point gui optional feature\n\n* ``pyqt5 >= 5.4.1``\n\nThe following packages are required to test this library:\n\n* ``pytest >= 3``\n* ``mock``\n\n\nInstallation\n------------\nIt is recommended that you use `anaconda <https://www.continuum.io/downloads>`_ or ``pip`` to install NeutronPy::\n\n    conda install -c neutronpy neutronpy\n\nor::\n\n    pip install neutronpy\n\nSee Installation for more detailed instructions.\n\nDocumentation\n-------------\nDocumentation is available at `neutronpy.github.io <https://neutronpy.github.io/>`_, or can be built using sphinx by navigating to the doc/ folder and executing ``make html``; results will be in the ``doc/_build/`` folder.\n\nTo ask questions you may either `request access <http://goo.gl/forms/odTeCYQQEc>`_ to the `Neutronpy Slack Team <http://neutronpy.slack.com>`_, or create a `Github issue <https://github.com/neutronpy/neutronpy/issues/new>`_.\n\nBuilding documentation requires the following additional packages:\n\n* ``sphinx>=1.4``\n* ``releases>=1.5.0``\n* ``numpydoc>=0.8.0``\n* ``neutronpy_rtd_sphinx_theme``\n\nContributions\n-------------\nContributions may be made by submitting a pull-request for review using the fork-and-pull method on GitHub. Feature requests and bug reports can be made using the GitHub issues interface. Please read the `development guide <https://neutronpy.github.io/development.html>`_ for details on how to best contribute.\n\nTo discuss development you may `request access <http://goo.gl/forms/odTeCYQQEc>`_ to the `Neutronpy Slack Team <http://neutronpy.slack.com>`_.\n\nCopyright & Licensing\n---------------------\nCopyright (c) 2014-2018, David M. Fobes, Released under terms in LICENSE.\n\nThe source for the Triple Axis Spectrometer resolution calculations was translated in part from the `ResLib <http://www.neutron.ethz.ch/research/resources/reslib>`_ 3.4c (2009) library released under the terms in LICENSE.RESLIB, originally developed by Andrey Zheludev at Brookhaven National Laboratory, Oak Ridge National Laboratory and ETH Zuerich. email: zhelud@ethz.ch.\n\nDisclaimer\n----------\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'David M Fobes',
    'author_email': 'dfobes@lanl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
