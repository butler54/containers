# Implementation Plan: Add Perf Utils Image

**Branch**: `001-add-perf-utils` | **Date**: 2026-09-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-add-perf-utils/spec.md`

## Summary

Add a `standard-quay/perf-utils` UBI 9 utility image that supplies `sysbench`, PostgreSQL server/client tools including `pgbench`, `fio`, and `stress-ng`. The image retains the full UBI shell, has no service entrypoint, and relies on users to explicitly initialize and start PostgreSQL. Extend the existing automated Quay build matrix, Dependabot coverage, and public documentation.

## Technical Context

**Language/Version**: Containerfile syntax; shell commands only for image build and validation

**Primary Dependencies**: Red Hat UBI 9 full base image; signed EPEL 9 package for `sysbench`; signed CentOS Stream 9 AppStream packages for `fio`, `stress-ng`, PostgreSQL server/client, and `pgbench`

**Storage**: No persistent application data. PostgreSQL data is created only when an operator explicitly initializes a local instance, optionally on an operator-provided volume.

**Testing**: Podman build; container smoke test for shell and utility version/help commands; process check confirming PostgreSQL is stopped by default; opt-in PostgreSQL initialization, start, readiness, and `pgbench` smoke test; Containerfile lint when available

**Target Platform**: Linux containers run with Podman-compatible runtimes; GitHub Actions hosted Linux runner for build and publication

**Project Type**: Container image definition and CI publication configuration

**Performance Goals**: Tools report version or help successfully in a freshly started image; an operator can begin a `pgbench` workload within 5 minutes after choosing a local or authorized external target

**Constraints**: Full UBI 9 image with a usable shell; PostgreSQL must not start automatically; no custom binary builds, embedded credentials, private endpoints, or prescribed runtime user; install only declared performance utilities and their required dependencies

**Scale/Scope**: One new `standard-quay` image, one existing build matrix update, one Dependabot directory entry, and README documentation; no database deployment, benchmark orchestration, or result storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status | Evidence / Decision |
|-----------|------|--------|---------------------|
| Utility-Focused Images | Include only the declared benchmarking and PostgreSQL utilities | PASS | Package list is limited to requested tools and dependencies; no development environment is added. |
| No Custom Binary Builds | Use packaged upstream software only | PASS | No source compilation. `sysbench` uses a signed EPEL RPM; `fio`, `stress-ng`, and PostgreSQL use signed CentOS Stream 9 RPMs. |
| Automated Builds and Publication | Build and publish through GitHub Actions | PASS | Add `perf-utils` to the existing `standard-quay` matrix, which publishes `quay.io/rh-ee-chbutler/perf-utils:latest`. Quay remains a documented existing category exception to the default GHCR registry. |
| Secure Red Hat Container Practices | Use a pinned Red Hat base; avoid embedded secrets and default privilege escalation | PASS | Use the established pinned UBI 9 base, DNF metadata cleanup, no `USER`, `CMD`, or `ENTRYPOINT`, and no credentials. The EPEL exception is limited and GPG-verified. |
| Public-Project Hygiene | Publish safe usage documentation | PASS | README documents registry location, interactive shell invocation, included tools, manual PostgreSQL startup, and external-target use. |

**Post-design re-check**: PASS. The plan adds no custom binaries, services that auto-start, secrets, or manual publication paths. The EPEL dependency is a documented exception necessary to supply the user-requested tools from packaged RPMs; package availability and signatures must be verified in the implementation build.

## Project Structure

### Documentation (this feature)

```text
specs/001-add-perf-utils/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
standard-quay/
└── perf-utils/
    └── Containerfile               # New full UBI 9 performance-utility image

.github/
└── workflows/
    └── standard-quay.yml           # Existing matrix extended with perf-utils

.github/dependabot.yml              # Existing Docker directory list extended
README.md                            # Existing category documentation extended
```

**Structure Decision**: Follow the existing `standard-quay/<image>/Containerfile` layout. Reuse its central build workflow rather than adding a separate workflow, because it already builds and publishes images from this category.

## Complexity Tracking

| Exception | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Signed EPEL 9 and CentOS Stream 9 RPM sources | Public UBI repositories do not provide all mandatory feature utilities. | Omitting the utilities fails the feature; compiling them from source violates the no-custom-binary-build principle. |
