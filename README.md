# HCN (Healthcare Cost Navigator)

Basic, functional web service that enables patients to search for hospitals offering MS-DRG procedures, view estimated prices & quality ratings, and interact with an AI assistant for natural language queries.

## Development Environment

To get your development environment setup, head to [Development Environment](./docs/development_environment.md).

## Run locally

If you want to get started quickly with `podman` (or `docker`) and `podman-compose` (or `docker-compose`) without installing anything else on your machine, run:

> If you are using `docker` over `podman`, replace all `podman` instances with `docker`. The commands are compatible!

```shell
podman compose -f compose.yaml up
```

And to completely clean up:

```shell
podman compose down --volumes --rmi all
```

If you wish to load the most recent ETL data (make sure you've setup your [Development Environment](./docs/development_environment.md)):

```shell
mise run 'migrate'
```
