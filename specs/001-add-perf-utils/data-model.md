# Data Model: Add Perf Utils Image

This feature has no application data model or persistent service. Its relevant configuration entities are documented for validation and maintenance.

## Image Definition

| Field | Description | Validation |
|-------|-------------|------------|
| Image name | Public image name | Must be `perf-utils`. |
| Base image | Full Red Hat UBI 9 source image | Must use a pinned UBI 9 digest. |
| Installed utilities | System, storage, stress, and PostgreSQL tooling | Must include `sysbench`, `fio`, `stress-ng`, PostgreSQL server/client utilities, and `pgbench`. |
| Startup behavior | Process state at image start | PostgreSQL must be stopped until explicitly started by an operator. |
| Runtime user | User selected by deployment environment | The image must not prescribe a fixed runtime user. |

## Package Source

| Field | Description | Validation |
|-------|-------------|------------|
| Source class | UBI repository or approved signed external RPM source | UBI is preferred; EPEL and CentOS Stream 9 AppStream are permitted only for unavailable requested utilities. |
| Signature verification | Package authenticity requirement | External RPM packages must retain repository signature verification. |
| Package scope | Installed package purpose | Each installed package must support a requested utility or required runtime dependency. |

## Local PostgreSQL Instance

| Field | Description | Validation |
|-------|-------------|------------|
| Data directory | Operator-selected initialized storage location | Created only by explicit operator action. |
| Service state | Stopped, initialized, running, stopped | New containers begin stopped; transitions occur only through explicit operator commands. |
| Benchmark target | Local initialized instance or authorized external PostgreSQL service | No target endpoint or credential is embedded in the image. |
