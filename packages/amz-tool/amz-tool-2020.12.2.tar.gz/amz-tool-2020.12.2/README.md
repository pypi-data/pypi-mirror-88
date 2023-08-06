# amz Tool

## Functionality

Awesome tool for setting things up

## Build Instructions

### Prerequisites

```bash
make setup
```

### Build `.deb` package (and remove unnecessary files)

```bash
make buildclean
```

Below is not the preferred way - doesn't clean the mess

```bash
make build
```

### Build `.deb` package and install

```bash
make buildinstall
```

### Install `.deb` package

```bash
make install
```

To install specific version from `/install/` dir (if it exists)

```bash
make install VERSION='2020.XX.XX'
```

## QnA

**What's going on with the version?? Is it meant to indicate the date of release??**

Initially meant to reflect date of release (`yyyy.mm.dd`). Mainly limited by the versioning guidelines of ppa launchpad which requires us to update the version for every upload. To automate it, we retain the (`yyyy.mm`) part of the versioning and `dd` is replaced by incremental number which can be bumped whenever being pushed to ppa - `make bumpver`. (Only works if git WD is clean and is on master)
