# Wargery

Create a war artifact from a Grails project and rename it in the format:
`<project name>-<date>-<build number>.war`.

## Install

### Requirements

Wargery uses the `subprocess:run` function which was added in Python 3.5 (see
the [documentation](https://docs.python.org/3/library/subprocess.html)). If you
want to use it with a previous version of Python, you will need to modify
`wargery/app.py` and possibly `setup.py` accordingly.

Note that in Ubuntu 18.04 (and probably other distros), the `python` command
points to a Python 2.7 install, and `pip` points to its package manager. If that
is the case, you need to install wargery with `pip3` to make sure it is using
your `python3` package.

### On Linux (or WSL)

To install for a single user, clone this repository then:

```
$ cd /path/to/wargery
$ pip install . -- user
```

This will install wargery to `~/.local/bin/`, just make sure it's in your path
and you're good to go.

### On Mac or Windows

I don't own a Mac and I use WSL on Windows, so I haven't had a chance to play
with it. However, this package uses `setuptools` which support both, so I
believe it should be pretty straightforward. Have a look at the documentation
[https://pypi.org/project/setuptools/](https://pypi.org/project/setuptools/).

## Usage

Wargery takes no arguments, once installed simply:

```
$ cd /path/to/grails/project
$ wargery
```

## Is this on PyPI?

Nope.

Frankly the use case for Wargery is so specific, you probably want to modify it
so that it meets your specific requirements. For example, maybe you want to
rename the war arifact to `<project name>-<commit hash>.war`. Have a look at
the `wargery.app:get_target_name` function, modify it as you see fit, and then
install Wargery.