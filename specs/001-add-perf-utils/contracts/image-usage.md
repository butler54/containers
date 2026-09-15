# Image Usage Contract

## Published Image

| Property | Contract |
|----------|----------|
| Registry reference | `quay.io/rh-ee-chbutler/perf-utils:latest` |
| Invocation | `podman run --rm -it quay.io/rh-ee-chbutler/perf-utils:latest bash` |
| Default process | An interactive shell when supplied by the operator; no service is started by image configuration. |
| Runtime identity | Selected by the calling environment; no fixed image user is required. |

## Included Commands

The image must expose these commands or their standard PostgreSQL equivalents:

- `sysbench`
- `fio`
- `stress-ng`
- `psql`
- `pgbench`
- PostgreSQL server and initialization utilities

## PostgreSQL Behavior

- PostgreSQL is installed but not initialized or started automatically.
- Operators explicitly choose local temporary or persistent storage, initialize a local instance, and start it when needed.
- Operators may instead connect `psql` and `pgbench` to an authorized external service.
- The image never contains a database endpoint, password, or other credential.

## Validation Contract

- `bash`, every included utility, and the PostgreSQL server command report usable version or help output in a fresh container.
- A fresh container has no running PostgreSQL server process.
- After explicit initialization and start, the local server accepts a readiness probe and a minimal `pgbench` operation.
