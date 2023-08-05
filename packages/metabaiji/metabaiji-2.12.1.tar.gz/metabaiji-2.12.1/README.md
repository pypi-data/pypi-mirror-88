baiji
=====

[![pip install](https://img.shields.io/badge/pip%20install-metabaiji-f441b8?style=flat-square)][pypi]
[![version](https://img.shields.io/pypi/v/metabaiji?style=flat-square)][pypi]
[![python versions](https://img.shields.io/pypi/pyversions/metabaiji?style=flat-square)][pypi]
[![build status](https://img.shields.io/circleci/project/github/metabolize/baiji/master.svg?style=flat-square)][circle]
[![last commit](https://img.shields.io/github/last-commit/metabolize/baiji?style=flat-square)][commits]
[![open pull requests](https://img.shields.io/github/issues-pr/metabolize/baiji?style=flat-square)][pull requests]

This is an active fork of [baiji][upstream], a high-level Python abstraction
layer for Amazon S3:

1. An [`open`][open]-like context handler which allows using S3 keys and
   local files interchangeably.
     - When reading S3, contents are first written to a temporary local
       file.
     - When writing S3, contents are written to a temporary local file,
       and uploaded on close.
2. An `s3` CLI for listing, copying, syncing, and other common activities.

The fork's goals are modest:

- Keep the library working in current versions of Python and other tools.
- Make bug fixes.
- Provide API stability and backward compatibility with the upstream version.
- Respond to community contributions.

It's used by related forks such as [lace][].

[upstream]: https://github.com/bodylabs/baiji
[circle]: https://circleci.com/gh/metabolize/baiji
[pypi]: https://pypi.org/project/metabaiji/
[pull requests]: https://github.com/metabolize/baiji/pulls
[commits]: https://github.com/metabolize/baiji/commits/master
[lace]: https://github.com/metabolize/lace


Features
--------

- Works without an S3 connection (with local files).
- Supports multiprocess parallelism for copying lots of files.
- Supports Python 2.7 and uses boto2.
- Supports OS X, Linux, and Windows.
- Tested and production-hardened.

[open]: https://docs.python.org/2/library/functions.html#open


Examples
--------

```py
with s3.open('s3://example/info.txt', 'w') as f:
    f.write('hello')

with s3.open('file:///home/me/info.txt', 'w') as f:
    f.write('hello')

with s3.open('s3://example/info.txt', 'r') as f:
    contents = f.readlines()

with s3.open('file:///home/me/info.txt', 'r') as f:
    contents = f.readlines()
```

```sh
s3 cp foo.txt s3://example/bar.txt
s3 cp s3://example/bar.txt s3://another-example/bazinga.txt
s3 rm s3://example/bar.txt
```


Development
-----------

```sh
pip install -r requirements_dev.txt
rake test
rake lint
```


TODO
----

1. Migrate credentials to `~/.aws/credentials` or env, and deprecate AWS
   credential support in `~/.bodylabs`.
2. Move `baiji.util.parallel` into a separate library.
3. Upgrade to boto3.


Contribute
----------

- Issue Tracker: github.com/bodylabs/baiji/issues
- Source Code: github.com/bodylabs/baiji

Pull requests welcome!


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the Apache license, version 2.0.
