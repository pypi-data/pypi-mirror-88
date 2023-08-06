# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geovectorslib', 'geovectorslib.tests']

package_data = \
{'': ['*']}

install_requires = \
['geographiclib>=1.50,<2.0', 'numpy>=1.18.0,<2.0.0']

entry_points = \
{'console_scripts': ['GeoVectors = geovectorslib.cli:main']}

setup_kwargs = {
    'name': 'geovectorslib',
    'version': '1.2',
    'description': 'Vectorized geodesic calculations.',
    'long_description': "# Overview\n\n[![Unix Build Status](https://img.shields.io/travis/omdv/geovectors/master.svg?label=unix)](https://travis-ci.org/omdv/geovectors)\n![Testing](https://github.com/omdv/geovectors/workflows/Testing/badge.svg)\n[![Coverage Status](https://img.shields.io/coveralls/omdv/geovectors/master.svg)](https://coveralls.io/r/omdv/geovectors)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/omdv/geovectors.svg)](https://scrutinizer-ci.com/g/omdv/geovectors/?branch=master)\n[![PyPI Version](https://img.shields.io/pypi/v/geovectorslib.svg)](https://pypi.org/project/geovectorslib)\n[![PyPI License](https://img.shields.io/pypi/l/geovectorslib.svg)](https://pypi.org/project/geovectorslib)\n\nThis library provides vectorized direct and inverse geodesic methods.\n\nThe motivation was to have the accurate and fast vectorized geodesic routines for sailboat routing project. There are few python libraries, with [geographiclib](https://geographiclib.sourceforge.io/html/python/index.html) being the most accurate and reliable. Haversine method, which is widely used as an example of fast inverse method can be vectorized rather easily, however the errors are expected to be at [least 0.5%](https://en.wikipedia.org/wiki/Haversine_formula#Formulation). There are no vectorized AND accurate options.\n\nThis library is based on `numpy` and uses [Vincenty's formulae](https://en.wikipedia.org/wiki/Vincenty's_formulae). It is heavily based on the [Movable Type Scripts blog](https://www.movable-type.co.uk/scripts/latlong-vincenty.html) and Javascript [Geodesy](https://www.npmjs.com/package/geodesy) code.\n\nVincenty's inverse algorithm is accurate, but sensitive to [nearly antipodal points](https://en.wikipedia.org/wiki/Vincenty%27s_formulae#Nearly_antipodal_points). One approach would be to return `NaN` for such points, with the assumption that they are not frequently observed in practical applications, however as [this discussion](https://gis.stackexchange.com/questions/84885/difference-between-vincenty-and-great-circle-distance-calculations) nicely pointed out the package cannot be complete if it cannot handle these situations. I found that the issue can be solved by relaxing one of convergence criteria, but it results in errors up to 0.25% vs geographiclib for these points.\n\nSo, instead, this library uses the vectorized Vincenty's formulae with **geographiclib as a fallback** for unconverged points.\n\nSee [notebook](https://github.com/omdv/geovectors/blob/master/notebooks/demo.ipynb) for execution time comparisons vs geographiclib.\n\n```\nDirect method for 100,000 points\n\n94.9 ms ± 25 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)\nvs\n9.79 s ± 1.4 s per loop (mean ± std. dev. of 7 runs, 1 loop each)\n```\n\n```\nInverse method for 100,000 points\n\n1.5 s ± 504 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)\nvs\n24.2 s ± 3.91 s per loop (mean ± std. dev. of 7 runs, 1 loop each)\n```\n\n# Setup\n\n## Requirements\n\n* Python 3.7+\n* Numpy\n* Geographiclib\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\npip install geovectorslib\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> from geovectorslib import direct, inverse\n>>> direct(lats1, lon1, bearings, distances)\n>>> inverse(lats1, lons1, lats2, lons2)\n```\n\n```text\nLatitudes in decimal degrees [-90; +90].\nLongitudes in decimal degrees [-180; +180].\nBearings in decimal degrees [0; 360].\nDistances in meters.\n```\n\n# References\n\n[Movable Type Scripts](https://www.movable-type.co.uk/scripts/latlong-vincenty.html)\n\n[Geodesy](https://www.npmjs.com/package/geodesy)\n\n[Geopy](https://pypi.org/project/geopy/)\n\n[Geographiclib](https://geographiclib.sourceforge.io/html/python/index.html)\n\n[Stackoverflow discussion](https://gis.stackexchange.com/questions/84885/difference-between-vincenty-and-great-circle-distance-calculations)",
    'author': 'Oleg Medvedev',
    'author_email': 'omdv.public@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/geovectorslib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
