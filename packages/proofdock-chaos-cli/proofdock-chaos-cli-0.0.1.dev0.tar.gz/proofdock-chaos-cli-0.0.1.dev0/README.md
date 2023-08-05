# Proofdock Chaos CLI
The Proofdock Chaos CLI is a command line tool to execute attacks and scenarios defined in the Azure DevOps. 


## Project description

This project is part of the Proofdock Chaos Platform that helps you to write, run, store and analyze chaos attacks in your Azure DevOps environment.

For more information visit our official [website][proofdock] or [documentation][proofdock_docs]. Feel free to ask for support for this package on [GitHub][proofdock_support].


## Getting started

To get started check out our official [guide][proofdock_docs_get_started].


## Install

This package requires Python 3.5+

```
$ pip install -U proofdock-chaos-cli
```


## Configuration

The Proofdock Chaos CLI expects that you have a proper API token that allows you to authenticate against the Proofdock cloud. Learn more about the API token generation [here][proofdock_docs_project_settings].

Set the API token using an environment variable ``PROOFDOCK_API_TOKEN``.

``` bash
export PROOFDOCK_API_TOKEN=<API token>
```

### Run
You use the `pd run` command to run an attack and upload its results to the Proofdock cloud.

``` bash
pd run [OPTIONS] <attack ID>
```

[proofdock]: https://proofdock.io/
[proofdock_docs]: https://docs.proofdock.io/
[proofdock_support]: https://github.com/proofdock/chaos-support/


[chaosengineeringplatform]: https://proofdock.io
[chaostoolkit]: https://chaostoolkit.org
[proofdock_docs_get_started]: https://docs.proofdock.io/chaos/guide
[proofdock_docs_project_settings]: https://docs.proofdock.io/chaos/devops/settings/#project-settings