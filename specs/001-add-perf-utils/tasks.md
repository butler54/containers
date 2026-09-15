---

description: "Task list for Add Perf Utils Image"
---

# Tasks: Add Perf Utils Image

**Input**: Design documents from `specs/001-add-perf-utils/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/image-usage.md`, and `quickstart.md`

**Tests**: No automated test suite was requested. Each story includes the directly executable Podman validation required by the specification.

**Organization**: Tasks are grouped by user story so each deliverable can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the required trusted package sources before image definition work.

- [X] T001 Verify public UBI 9 package availability and verify signed EPEL 9 availability for `sysbench` plus signed CentOS Stream 9 AppStream availability for `fio`, `stress-ng`, PostgreSQL server/client, and `pgbench` before recording the package transaction in `standard-quay/perf-utils/Containerfile`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the shared, secure base image definition required by both user stories.

- [X] T002 Create `standard-quay/perf-utils/Containerfile` with the established pinned full UBI 9 base, only the verified signed package sources, DNF metadata cleanup, and no `USER`, `CMD`, or `ENTRYPOINT`

**Checkpoint**: The base image definition is ready for story-specific utilities; no user-story validation begins until its package sources and startup behavior are reviewable.

---

## Phase 3: User Story 1 - Run Performance Diagnostics (Priority: P1) MVP

**Goal**: Provide an interactive full-UBI shell containing the requested system, storage, and stress diagnostic utilities.

**Independent Test**: Build `standard-quay/perf-utils/Containerfile`, start `bash`, and confirm that `sysbench`, `fio`, and `stress-ng` each return version or help output successfully.

- [X] T003 [US1] Add the verified `sysbench`, `fio`, and `stress-ng` packages to `standard-quay/perf-utils/Containerfile` without adding unrelated tooling
- [X] T004 [US1] Build `standard-quay/perf-utils/Containerfile` with Podman and validate `bash`, `sysbench --version`, `fio --version`, and `stress-ng --version` as described in `specs/001-add-perf-utils/quickstart.md`

**Checkpoint**: The image supplies a usable shell and all non-database diagnostic utilities, independently satisfying User Story 1.

---

## Phase 4: User Story 2 - Benchmark PostgreSQL (Priority: P2)

**Goal**: Add PostgreSQL server, client, and `pgbench` capabilities while keeping the server stopped until an operator deliberately starts it.

**Independent Test**: Build the image, confirm PostgreSQL commands are available and no PostgreSQL process is running in a fresh container, then explicitly initialize and start a temporary local instance and run a minimal `pgbench` workload.

- [X] T005 [US2] Add the verified PostgreSQL server, client, and `pgbench` provider packages to `standard-quay/perf-utils/Containerfile` without initialization or service-start build steps
- [X] T006 [US2] Validate PostgreSQL command availability and confirm a fresh container from `standard-quay/perf-utils/Containerfile` has no `postgres` process using the `/proc` check in `specs/001-add-perf-utils/quickstart.md`
- [X] T007 [US2] Validate explicit temporary PostgreSQL initialization, direct startup, readiness, `psql` connection, and a minimal `pgbench` workload using the procedure in `specs/001-add-perf-utils/quickstart.md`

**Checkpoint**: PostgreSQL and `pgbench` are usable only after operator action, independently satisfying User Story 2.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Publish the image through the existing category workflow, maintain update coverage, document safe use, and complete release validation.

- [X] T008 [P] Add `perf-utils` to the build matrix in `.github/workflows/standard-quay.yml` so GitHub Actions builds and publishes `quay.io/rh-ee-chbutler/perf-utils:latest`
- [X] T009 [P] Add `/standard-quay/perf-utils` to the Docker update directories in `.github/dependabot.yml` for pinned-base updates
- [X] T010 Update `README.md` with the `perf-utils` registry reference, interactive Podman invocation, included utilities, explicit PostgreSQL startup behavior, and external-target `pgbench` guidance
- [X] T011 Run Containerfile linting when available and resolve findings in `standard-quay/perf-utils/Containerfile`
- [ ] T012 Run the complete local and published-image validation scenarios in `specs/001-add-perf-utils/quickstart.md` and record any required documentation corrections in `README.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately and determines trustworthy package availability.
- **Foundational (Phase 2)**: Depends on T001 and blocks both user stories.
- **User Story 1 (Phase 3)**: Depends on T002 and is the MVP.
- **User Story 2 (Phase 4)**: Depends on T002 and can be completed independently of User Story 1, although both modify the same Containerfile and should be sequenced to avoid conflicts.
- **Polish (Phase 5)**: T008 and T009 can begin after the image path is established; T010 follows the final runtime behavior; T011 and T012 follow both stories.

### User Story Dependencies

- **User Story 1 (P1)**: T002 -> T003 -> T004.
- **User Story 2 (P2)**: T002 -> T005 -> T006 -> T007.

## Parallel Opportunities

- T008 and T009 can run in parallel because they modify separate automation files.
- T003 and T005 have no functional dependency, but both modify `standard-quay/perf-utils/Containerfile`; sequence them unless one contributor owns the combined edit.
- T010 can be drafted while image implementation proceeds, then verified after T007.

## Parallel Example: Publication Preparation

```text
Task: "Add perf-utils to the build matrix in .github/workflows/standard-quay.yml"
Task: "Add /standard-quay/perf-utils to the Docker update directories in .github/dependabot.yml"
```

## Implementation Strategy

### MVP First

1. Complete T001 and T002 to establish a secure, reproducible base definition.
2. Complete T003 and T004 for User Story 1.
3. Stop and validate the shell plus system, storage, and stress utilities independently.

### Incremental Delivery

1. Add User Story 2 through T005-T007 without introducing automatic PostgreSQL startup.
2. Add workflow, update monitoring, documentation, linting, and end-to-end validation through T008-T012.
3. Confirm the published image matches the local validation result.
