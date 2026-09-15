# Quickstart: Validate Perf Utils

## Prerequisites

- Podman installed and able to build and run local images.
- Network access to the configured, signed package repositories during the build.
- A PostgreSQL target only when validating remote benchmarking.

## Build

From the repository root:

```sh
podman build -t perf-utils -f standard-quay/perf-utils/Containerfile .
```

Expected outcome: the build completes using the pinned UBI 9 base and installs only the utilities described in [data-model.md](data-model.md).

## Verify Shell And Tools

```sh
podman run --rm perf-utils bash -lc '
  sysbench --version &&
  fio --version &&
  stress-ng --version &&
  psql --version &&
  pgbench --version &&
  postgres --version
'
```

Expected outcome: every command succeeds. Start an interactive session with `podman run --rm -it perf-utils bash`.

## Verify PostgreSQL Does Not Auto-Start

```sh
podman run --rm perf-utils bash -lc '
  for process in /proc/[0-9]*; do
    read -r command < "$process/comm" 2>/dev/null || continue
    [ "$command" = postgres ] && exit 1
  done
'
```

Expected outcome: the command succeeds, proving that a new container has no PostgreSQL server process.

## Verify Explicit Local PostgreSQL

Run PostgreSQL as its packaged operating-system user. This explicitly initializes a temporary data directory, starts the server with a writable socket directory, runs a minimal benchmark, then stops the server when the container exits:

```sh
podman run --rm --user postgres perf-utils bash -lc '
  initdb -D /tmp/pgdata || exit 1
  postgres -D /tmp/pgdata -k /tmp >/tmp/postgres.log 2>&1 &
  postgres_pid=$!
  for attempt in $(seq 1 10); do pg_isready -h /tmp && break; sleep 1; done
  pg_isready -h /tmp &&
  pgbench -h /tmp -i postgres &&
  pgbench -h /tmp -c 1 -j 1 -t 1 postgres
  status=$?
  kill "$postgres_pid"
  wait "$postgres_pid"
  exit "$status"
'
```

Expected outcome: the server starts only after the operator's explicit action and accepts the basic benchmark. See [contracts/image-usage.md](contracts/image-usage.md) for the runtime contract.

## Verify Published Image

After the GitHub Actions workflow succeeds, repeat the shell and tool checks against `quay.io/rh-ee-chbutler/perf-utils:latest`.

Expected outcome: the public image provides the same commands and startup behavior as the local build.
