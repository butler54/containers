# Feature Specification: Add Perf Utils Image

**Feature Branch**: `001-add-perf-utils`

**Created**: 2026-09-15

**Status**: Draft

**Input**: User description: "A container image to be built called perf-utils based on ubi9 that contains sysbench, postgresql, pg-bench, fio and stress-ng. Based on a full UBI image (e.g. contains a shell)"

## Clarifications

### Session 2026-09-15

- Q: Should `perf-utils` include a running PostgreSQL server, or only PostgreSQL client and benchmark tools? -> A: Include the PostgreSQL server, but do not start it automatically.
- Q: Should `perf-utils` run as a non-root user by default? -> A: Keep the image user unspecified.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run Performance Diagnostics (Priority: P1)

As a performance engineer, I want a single ready-to-run image with common system and storage benchmark utilities so that I can perform diagnostics without installing tools on the target environment.

**Why this priority**: This is the image's core purpose and delivers immediate value for system performance investigation.

**Independent Test**: Start the image and run each supplied system and storage benchmark utility's version or help command; each command completes successfully and identifies the utility.

**Acceptance Scenarios**:

1. **Given** the published `perf-utils` image, **When** an engineer starts an interactive shell, **Then** a usable command shell is available.
2. **Given** a running `perf-utils` image, **When** an engineer invokes `sysbench`, `fio`, or `stress-ng`, **Then** each utility is available to run.

---

### User Story 2 - Benchmark PostgreSQL (Priority: P2)

As a database performance engineer, I want PostgreSQL server, command-line, and benchmarking utilities in the same image so that I can either start a local database intentionally or connect to an authorized PostgreSQL service and run database benchmarks.

**Why this priority**: Database benchmarking is explicitly required and supports either an intentionally started local service or an authorized external service.

**Independent Test**: Start the image and confirm that the PostgreSQL server, command-line utility, and `pgbench` can display their version or help information without a database service starting automatically.

**Acceptance Scenarios**:

1. **Given** a running `perf-utils` image, **When** an engineer invokes the PostgreSQL command-line utility, **Then** the utility is available to connect to a PostgreSQL service.
2. **Given** a running `perf-utils` image, **When** an engineer invokes `pgbench`, **Then** the utility is available to initialize or execute a benchmark against an authorized PostgreSQL service.
3. **Given** a newly started `perf-utils` image, **When** an engineer has not explicitly started PostgreSQL, **Then** no PostgreSQL server process is running.

### Edge Cases

- When a benchmark requires a database service that is unreachable or rejects credentials, the image must return the utility's error without storing credentials in the image.
- When a benchmark requires elevated host access that is not granted, the image must fail safely and must not request extra privileges automatically.
- When an engineer needs a tool not listed in this specification, the image must not claim to provide it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST provide a publicly publishable container image named `perf-utils` for performance diagnostics and benchmarking.
- **FR-002**: The image MUST be based on Red Hat Universal Base Image 9 and include an interactive command shell.
- **FR-003**: The image MUST make `sysbench`, `fio`, and `stress-ng` available for execution.
- **FR-004**: The image MUST make PostgreSQL server and command-line utilities, including `pgbench`, available for execution.
- **FR-004a**: The image MUST NOT start the PostgreSQL server automatically; an engineer must explicitly start it when needed.
- **FR-005**: The image MUST not include embedded credentials, personal configuration, or private endpoints.
- **FR-006**: The image MUST not prescribe a default runtime user; users may opt into only the additional runtime permissions required by their selected benchmark.
- **FR-007**: The project MUST build and publish the image through its automated release process.
- **FR-008**: The image documentation MUST state its purpose, public registry location, intended invocation, included utilities, and that PostgreSQL benchmarking targets an external authorized service.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An engineer can start an interactive shell in the published image in one command.
- **SC-002**: All five requested utilities or utility families (`sysbench`, PostgreSQL utilities, `pgbench`, `fio`, and `stress-ng`) report version or help information successfully in a freshly started image.
- **SC-003**: An engineer can confirm that PostgreSQL is not running in a freshly started image, then intentionally start it or connect to an authorized PostgreSQL service and begin a `pgbench` workload within 5 minutes.
- **SC-004**: The published image contains no credentials, private endpoints, or user-specific configuration.
- **SC-005**: The image is available from its documented public registry location after a successful automated release.

## Assumptions

- The image includes PostgreSQL server software for intentional local use, but it does not start or manage the server automatically.
- `pg-bench` in the feature request refers to PostgreSQL's `pgbench` utility.
- Engineers supply target endpoints, test data, and any runtime permissions needed for their selected benchmark.
- The deployment environment selects the image's runtime user and grants any benchmark-specific permissions.
- The existing project conventions will determine the image's directory layout, workflow placement, tags, and documentation location.
