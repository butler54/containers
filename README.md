# containers

Utility container builds for personal use.
Images generally track `latest`; standard GHCR builds also publish commit-addressed tags for digest-pinned consumption.

## Categories

Each category has a build workflow under `.github/workflows/`; each image lives in
`<category>/<image>/Containerfile`.

| Category         | Registry                    | Workflow             | Notes                                    |
|------------------|------------------------------|----------------------|-------------------------------------------|
| `micro-quay`     | `quay.io/rh-ee-chbutler`    | `micro-quay.yml`     | Minimal single-purpose images             |
| `standard-quay`  | `quay.io/rh-ee-chbutler`    | `standard-quay.yml`  | UBI-based utility images                  |
| `standard-ghcr`  | `ghcr.io/butler54`          | `standard-ghcr.yml`  | Red Hat Hardened Image (`hi/*`) based utility images |
| `sandbox`        | `ghcr.io/butler54`          | `sandbox.yml`        | openshell/sandboxctl images                |

## `standard-quay` - UBI utility images

Full UBI 9 utility images built and published through GitHub Actions to Quay.

| Image dir | Published tag | Notes |
|-----------|---------------|-------|
| `standard-quay/perf-utils` | `quay.io/rh-ee-chbutler/perf-utils:latest` | Performance diagnostics with `sysbench`, PostgreSQL server/client and `pgbench`, `fio`, and `stress-ng`. Start an interactive shell with `podman run --rm -it quay.io/rh-ee-chbutler/perf-utils:latest bash`. PostgreSQL is installed but never starts automatically; explicitly initialize and start it for local testing, or use `psql` and `pgbench` with an authorized external service. |

## `standard-ghcr` — hardened multi-arch utility images

UBI-style utility images built on [Red Hat Hardened Images](https://images.redhat.com/)
(`registry.access.redhat.com/hi/*`), published to **GitHub Container Registry**
(GitHub-hosted CI + registry, using the built-in `GITHUB_TOKEN` — no external registry
secret needed). Multi-arch (`linux/amd64` + `linux/arm64`), built on native GitHub
runners and merged into a manifest list with `podman`, same pattern as `sandbox/`.

| Image dir           | Published tag                          | Notes                                                      |
|----------------------|-----------------------------------------|-------------------------------------------------------------|
| `standard-ghcr/qmp`  | `ghcr.io/butler54/qmp:latest`          | `qemu.qmp[tui]` (`qmp-tui`, `qmp-shell`, `qmp-shell-wrap`) on the RH Hardened `hi/python` image; no entrypoint, run e.g. `podman run --rm -it ghcr.io/butler54/qmp:latest qmp-tui <host> <port>` |
| `standard-ghcr/architecture-docs` | `ghcr.io/butler54/architecture-docs:sha-<commit>` | Generic non-root Python 3.12.15/Node 24.21.0, Zensical, Trestle, D2, Structurizr with offline Chromium, Pandoc, XeLaTeX, librsvg and PDF inspection tools. Fedora is an explicitly approved base exception for the native graphics/TeX stack. GitHub Actions must pass offline exports before publication; consumers pin the manifest digest. No workspace, credentials or project-specific content is included. |

The standard GHCR workflow can dispatch one selected image. All builds publish a
commit-addressed multi-architecture tag; only `main` updates `latest`. Fedora/RPM
updates are recorded in the image's package inventory, and explicit downloaded
tool releases are checksum-verified. The documentation image's source and runtime
dependencies remain generic; publication never copies a consuming repository.

The documentation image uses a maintained CLI-only Structurizr variant compiled
from upstream commit `f828a297dc693e08115b7e5b51dba4a83d8148c2` (2026.09.19).
Only `validate` and `export` are exposed; the unused Spring web server, cloud
publishers, and optional scripting-language runtimes are not packaged. Its Maven
dependency overrides are in `standard-ghcr/architecture-docs/structurizr-cli/pom.xml`;
the image records dependency checksums. Chromium/Playwright assets remain pinned
to the matching upstream image. npm 11.19.1 includes checksum-verified,
same-major vendored fixes for brace-expansion 5.0.11 and undici 6.28.1, recorded in
`standard-ghcr/architecture-docs/patch-npm.py`. These variants must pass the same
offline smoke tests and vulnerability gate as the rest of the toolchain.

## `sandbox` — openshell/sandboxctl images

Images consumed by the `sandboxctl` / `openshell` toolchain, published to **GitHub
Container Registry** (GitHub-hosted CI + registry, using the built-in `GITHUB_TOKEN` —
no external registry secret needed):

| Image dir              | Published tag                                             |
|------------------------|----------------------------------------------------------|
| `sandbox/base`         | `ghcr.io/butler54/openshell-sandbox-base:latest`         |
| `sandbox/standard`     | `ghcr.io/butler54/openshell-sandbox:latest`              |
| `sandbox/docs`         | `ghcr.io/butler54/openshell-sandbox-docs:latest`         |
| `sandbox/speckit`      | `ghcr.io/butler54/openshell-sandbox-speckit:latest`      |
| `sandbox/speckit-docs` | `ghcr.io/butler54/openshell-sandbox-speckit-docs:latest` |

- **Multi-arch** (`linux/amd64` + `linux/arm64`), built on native GitHub runners
  (`ubuntu-latest` + `ubuntu-24.04-arm`), base first, then the thin layers `FROM` it.
- **`base`** carries all heavy tooling (gcloud, Go, `oc`/`kubectl`, helm, `glab`, bun,
  Playwright Chromium, SpecKit, GSD, claude-mem, docling + CPU PyTorch, draw.io).
  MLflow tracing plugins are not baked into the image or enabled by default.
  Arch-specific downloads are parameterized by buildx `$TARGETARCH`.
- **No user-specific config** is baked in. Git identity is injected at sandbox creation
  by `sandboxctl` (from its `[identity]` config); the `GIT_USER_NAME` / `GIT_USER_EMAIL`
  build ARGs are an optional local-build override only.
- **GSD** defaults to the `adaptive` model profile; the opus (high-end) tier is patched
  to `claude-opus-4-8[1m]` (Opus 4.8, 1M context) in the base catalog.
- **Pinning / updates:** the upstream base is pinned by manifest-list digest and bumped
  by **Dependabot** (`docker` + `github-actions` ecosystems). Raw `curl`-downloaded tools
  in the base (Go, `oc`, helm, `yq`, `glab`, draw.io) track "latest" and are refreshed by
  the **weekly scheduled rebuild**, not Dependabot.
