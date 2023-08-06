# Veeam Enterprise Manager REST API Client ``veeam-em``

[![CI][build-img]](https://gitlab-ee.eis.utoronto.ca/eis/veeam/veeam-em/commits/master)
[![Coverage][coverage-img]](https://gitlab-ee.eis.utoronto.ca/eis/veeam/veeam-em/commits/master)
[![PyPI][pypi-img]](https://pypi.python.org/pypi/veeam-em)
[![PyPI version][pyver-img]](https://pypi.python.org/pypi/veeam-em)
[![Docker Image Pulls][docker-pulls-img]][docker-image]
[![Docker Image Layers][docker-layer-img]][docker-image]
[![Docker Image Version][docker-version-img]][docker-image]

   
## Documentation

TBW.

## Installation

The fastest way to install Veeam EM is to use [pip][pip]:

```bash
pip install veeam-em
```

If you have Veeam EM installed and want to upgrade to the latest version you can run:

```bash
pip install --upgrade veeam-em
```

This will install Veeam EM as well as all dependencies. 

You can also just [download the tarball][download the tarball]. Once you have the `veeam-em` directory structure on your workstation, you can just run:

```bash
cd <path_to_veeam-em>
pip install .
```


## Docker

For more information refer to the [Docker](docker/README.md) section.

Use
===

## Getting Help

We use GitLab issues for tracking bugs, enhancements and feature requests.
If it turns out that you may have found a bug, please [open a new issue][open a new issue].

## Versioning

The API versions are tagged based on [Semantic Versioning](https://semver.org/). Versions available in the 
[tags section](https://gitlab-ee.eis.utoronto.ca/eis/veeam/veeam-em/tags).

## Contributing

Refer to the [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process of 
submitting code to the repository.

[docs]: https://eis.utoronto.ca/~vss/eeam-em/
[download the tarball]: https://pypi.python.org/pypi/eeam-em
[Click]: http://click.pocoo.org/6/
[Python Releases for Windows]: https://www.python.org/downloads/windows/
[pip]: http://www.pip-installer.org/en/latest/
[open a new issue]: https://gitlab-ee.eis.utoronto.ca/eis/veeam/veeam-em/issues/new
[Alpine Linux]: https://hub.docker.com/_/alpine/
[PyVSS]: https://pypi.python.org/pypi/eeam-em
[build-img]: https://gitlab-ee.eis.utoronto.ca/eis/veeam/veeam-em/badges/master/pipeline.svg
[coverage-img]: https://gitlab-ee.eis.utoronto.ca/eis/veeam/veeam-em/badges/master/coverage.svg
[pypi-img]: https://img.shields.io/pypi/dm/veeam-em.svg
[pyver-img]: https://img.shields.io/pypi/pyversions/veeam-em.svg
[docker-pulls-img]:  https://img.shields.io/docker/pulls/uofteis/veeam-em.svg
[docker-layer-img]: https://images.microbadger.com/badges/image/uofteis/veeam-em.svg
[docker-version-img]: https://images.microbadger.com/badges/version/uofteis/veeam-em.svg
[docker-image]: https://hub.docker.com/r/uofteis/veeam-em/
[Python 3.7 for Mac]: https://www.python.org/downloads/mac-osx/
[Python 3.5 for Linux]: https://www.python.org/downloads/source/
