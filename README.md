# containers

Utility container builds for personal use.
All are un-versioned.

## Categories

Each category has a build workflow under `.github/workflows/`; each image lives in
`<category>/<image>/Containerfile`.

| Category   | Registry                    | Workflow        | Notes                          |
|------------|-----------------------------|-----------------|--------------------------------|
| `micro`    | `quay.io/rh-ee-chbutler`    | `micro.yml`     | Minimal single-purpose images  |
| `standard` | `quay.io/rh-ee-chbutler`    | `standard.yml`  | UBI-based utility images        |
| `sandbox`  | `ghcr.io/butler54`          | `sandbox.yml`   | openshell/sandboxctl images     |

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
