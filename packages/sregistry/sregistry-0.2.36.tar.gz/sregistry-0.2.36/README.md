# Singularity Global Client

[![https://img.shields.io/badge/software%20checklist-100%25-59BF40](https://img.shields.io/badge/software%20checklist-100%25-59BF40)](https://stanford-rc.github.io//rse-services/docs/tools/software-checklist/badge?label=100%25&color=#59BF40&ids=r1,r2,r3,r4,r5,r6,d1,d2,d3,d4,d5,d6,d7,a1,a2,a3,ci1,ci2&title=singularityhub/sregistry-cli)
[![GitHub actions status](https://github.com/singularityhub/sregistry-cli/workflows/sregistry-ci/badge.svg?branch=master)](https://github.com/singularityhub/sregistry-cli/actions?query=branch%3Amaster+workflow%3Asregistry-ci)

Hi Friends! Are your containers lonely? Singularity containers thrive in happiness when they are shared. This means that wherever you might have them in these cloudy places, they are easy to find and move around.

## What is this?

Singularity Global Client is an interface to interact with Singularity containers in many different storage locations. We are able to use modern APIs by way of providing and using the software within a Singularity container! For older architectures, we provide a [Singularity container](Singularity) for you to use instead. You can build it from this repository, or use the provided container on [Singularity Hub](https://www.singularity-hub.org/collections/379).

If used for the Singularity Registry client, Python 3 is required. See our [installation guide](https://singularityhub.github.io/sregistry-cli/install) to get started. For more details, please refer to our [documentation](docs).

## Installation instructions

With pip:

```bash
pip install sregistry[all]
```

With conda:

```bash
conda install -c conda-forge sregistry
```

More detailed instructions can be found [here](https://singularityhub.github.io/sregistry-cli/install)

## Python Versions Under 3

If you are looking for a version that works with Python 2.* see [this branch](https://github.com/singularityhub/sregistry-cli/releases/tag/v0.1.41), or all releases / branches prior to 0.2.0.

## Building the RPM

The file [sregistry-cli.spec](sregistry-cli.spec) is provided to build an rpm for a specified version,
typcailly the current release on pypi, and was discussed [here](https://github.com/singularityhub/sregistry-cli/issues/138#issuecomment-413323717).
You should do the following:

 1. Update the version to be the current in pypi specified in [sregistry/version.py](sregistry/version.py).

```bash
Version:        0.0.89
```

 2. Create a [new release](https://github.com/singularityhub/sregistry-cli/releases/new) on Github with the version spec file added.
 3. Download the .tar.gz file from the release

```bash
VERSION=0.0.92
wget https://github.com/singularityhub/sregistry-cli/archive/sregistry-cli-${VERSION}.tar.gz
```

 4. Use rpmbuild to build it.

```bash
rpmbuild -ta sregistry-cli-$VERSION.tar.gz
```

You should get an srpm which that can be distributed and anyone can be rebuilt:

```bash
rpmbuild --rebuild sregistry-cli.srpm
```

## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
