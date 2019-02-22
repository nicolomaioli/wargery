# Wargery

Create a war artifact from a Grails project and rename it to something
sensible. Out of the box you get:

- `<project-name>-<commit hash>.war` (default);
- `<project name>-<date>-<build number>.war` (with options).

## Install

### Requirements

Wargery is compatible with Python 3.3+.

### On Linux (or WSL)

To install for a single user, clone this repository then:

```
$ cd /path/to/wargery
$ pip install . --user
```

This will create a `wargery` command to `~/.local/bin/`, just make sure it's in
your path and you're good to go.

### On Mac or Windows

This package uses `setuptools` Have a look at the documentation
[https://pypi.org/project/setuptools/](https://pypi.org/project/setuptools/).

## Usage

Check out `wargery -h` for a list of CLI options.

For an example of a package using `wargery` as a dependency, check out
[Sarnieploy](https://github.com/nicolomaioli/sarnieploy).

## Is this on PyPI?

Nope.

Frankly the use case for Wargery is so specific, you probably want to modify it
so that it meets your specific requirements. Have a look at
`wargery.utils:get_target_name`, modify it as you see fit, and then install
Wargery.
