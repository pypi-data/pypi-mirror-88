# Unimake

The `unimatrix.ext.model` package declares bases classes to implement
all conceptual models of the Unimatrix Framework.

Install `unimatrix.ext.model`:

```
$ pip install unimatrix.ext.model
```

Make sure that your local environment satisfies the [specified prequisites](#prequisites).

Head over to the  [development section](#developing) if you plan to contribute
to this project.


## Prequisites

The following Python version(s) are compatible with the `unimatrix.ext.model` package:

- 3.5 (deprecated)
- 3.6 (deprecated)
- 3.7
- 3.8
- 3.9

To install or upgrade Python, visit https://www.python.org/downloads/ and
choose one of the supported releases.

## Developing ##

Clone the source code repository:

```
$ git clone git@gitlab.com:unimatrixone/libraries/python-unimatrix/model.git
```

- Run `make env` to set up the local development environment.
- Run `make console` to start a Python interpreter.
- If new requirements are added to the project (see `git log requirements.txt`),
  run `make depsrebuild`.
- Export the environment variables to a file with `make .env`. Use this command
  when integrating with third-party IDEs such as Eclipse or VSCode. Do not check
  in this file to the version control system - it is local to your environment
  only.
- Build the technical documentation with `make documentation`.
- Additional targets may be specified in [`config.mk`](./config.mk).

## License

Proprietary

[Click or tap here for licensing requests](mailto:cochise.ruhulessin@unimatrixone.io).

## Author information

This Python package was created by **Cochise Ruhulessin** for the
[Unimatrix One](https://cloud.unimatrixone.io) project.

- [Send me an email](mailto:cochise.ruhulessin@unimatrixone.io)
- [GitLab](https://gitlab.com/unimatrixone)
- [GitHub](https://github.com/cochiseruhulessin)
- [LinkedIn](https://www.linkedin.com/in/cochise-ruhulessin-0b48358a/)
- [Twitter](https://twitter.com/magicalcochise)
