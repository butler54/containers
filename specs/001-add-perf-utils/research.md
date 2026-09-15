# Research: Add Perf Utils Image

## Package Sources

**Decision**: Install `sysbench` from signed EPEL 9. Install `fio`, `stress-ng`, `postgresql-server`, and `postgresql-contrib` from signed CentOS Stream 9 AppStream. Use the pinned UBI 9 image as the base.

**Rationale**: The requested feature requires all five utilities while the project prohibits custom binary builds. Public UBI repositories supply neither `fio` nor `stress-ng`, and EPEL 9 supplies `sysbench` but not the other required utilities. Both external sources are narrowly scoped, public RPM-source exceptions with signature verification retained.

**Alternatives considered**: Omitting unavailable tools fails the specification. Building from source violates the constitution. A subscription-only package source would make a public image less reproducible.

## Base Image And Build Hygiene

**Decision**: Use the existing pinned full UBI 9 image reference used by `standard-quay` images. Install only required packages, clean DNF metadata in the same build layer, and do not add an entrypoint, command, or fixed runtime user.

**Rationale**: This preserves the requested usable shell and aligns with the existing category, Dependabot digest updates, and least-privilege runtime requirement.

**Alternatives considered**: A minimal base would not provide the requested full UBI shell. A floating base tag weakens reproducibility and update tracking.

## PostgreSQL Runtime Behavior

**Decision**: Include server and client packages, but leave PostgreSQL stopped. Documentation must describe intentional initialization and startup by the operator.

**Rationale**: The clarified specification requires local PostgreSQL capability without an automatically started service, background process, or initialization side effect.

**Alternatives considered**: An automatic service entrypoint conflicts with the specification. Client-only PostgreSQL support was explicitly rejected during clarification.

## Publishing And Documentation

**Decision**: Add `perf-utils` to the existing `standard-quay` build matrix, Dependabot Docker-directory list, and README category documentation.

**Rationale**: Existing `standard-quay` images are built by GitHub Actions and published as `quay.io/rh-ee-chbutler/<image>:latest`. This is the established category convention.

**Alternatives considered**: A separate workflow duplicates an existing release mechanism. Moving the image to GHCR would diverge from its UBI-based category without a feature requirement.

## Validation Strategy

**Decision**: Validate a local Podman build, shell access, all requested executables, an absent PostgreSQL process at startup, and an explicitly initialized PostgreSQL instance that accepts a basic `pgbench` workload.

**Rationale**: These tests directly prove the functional requirements and distinguish installation from automatic server startup.

**Alternatives considered**: Version-only checks cannot prove the server can be intentionally started. Running benchmark workloads against shared services would introduce credentials and non-deterministic external dependencies.
