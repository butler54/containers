"""Generic offline image acceptance. No consuming workspace or credentials."""
from __future__ import annotations

import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import tempfile


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, check=False, capture_output=True, text=True, timeout=240)
    if result.returncode:
        raise RuntimeError(f"Command {args!r} failed ({result.returncode}):\n{result.stdout}\n{result.stderr}")
    return result.stdout + result.stderr


def main() -> None:
    if os.getuid() == 0:
        raise RuntimeError("Image smoke test must run as non-root")
    for package, version in {"zensical": "0.0.68", "compliance-trestle": "5.2.0"}.items():
        if importlib.metadata.version(package) != version:
            raise RuntimeError(f"Wrong {package} version")
    versions = {name: run(*command).splitlines()[0] for name, command in {
        "python": ("python3.12", "--version"), "node": ("node", "--version"),
        "d2": ("d2", "--version"), "pandoc": ("pandoc", "--version"),
        "xelatex": ("xelatex", "--version"), "rsvg": ("rsvg-convert", "--version"),
        "java": ("java", "-version"),
    }.items()}
    with tempfile.TemporaryDirectory(prefix="architecture-docs-") as directory:
        root = Path(directory)
        icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><path fill="#1473e6" d="M2 2h36v36H2z"/></svg>'
        (root / "icon.svg").write_text(icon)
        (root / "view.d2").write_text('service: Service {icon: ./icon.svg}\nuser: User\nuser -> service: Uses\n')
        run("d2", "--layout=elk", "--bundle=true", "view.d2", "view.svg", cwd=root)
        if not (root / "view.svg").is_file():
            raise RuntimeError("D2 did not produce a diagram")
        (root / "workspace.dsl").write_text('''workspace "Example" {
 model {
  user = person "User"
  app = softwareSystem "Application"
  user -> app "Uses"
 }
 views {
  systemContext app "Context" {
   include *
   autoLayout lr
  }
  styles {
   element "Software System" {
    icon "icon.svg"
   }
  }
 }
}''')
        run("structurizr", "validate", "-workspace", "workspace.dsl", cwd=root)
        run("structurizr", "export", "-workspace", "workspace.dsl", "-format", "svg", "-output", "c4", cwd=root)
        exports = list((root / "c4").glob("*.svg"))
        if not exports or not any("image" in p.read_text() for p in exports):
            raise RuntimeError("Structurizr SVG export lost the custom icon")
        run("rsvg-convert", "--format=pdf", "--output=view.pdf", "view.svg", cwd=root)
        (root / "book.md").write_text("# Generic architecture\n\n![Diagram](view.pdf)\n")
        run("pandoc", "book.md", "--standalone", "--pdf-engine=xelatex", "--output=book.pdf", cwd=root)
        if (root / "book.pdf").read_bytes()[:5] != b"%PDF-":
            raise RuntimeError("PDF build failed")
        run("pdftotext", "book.pdf", "book.txt", cwd=root)
        if "Generic architecture" not in (root / "book.txt").read_text():
            raise RuntimeError("PDF text missing")
        (root / "docs").mkdir()
        (root / "docs/index.md").write_text("# Generic architecture\n\nOffline image smoke test.\n")
        (root / "zensical.toml").write_text('[project]\nsite_name="Generic documentation"\ndocs_dir="docs"\nsite_dir="site"\n[project.theme]\nfont=false\n')
        run("zensical", "build", "--config-file", "zensical.toml", "--strict", cwd=root)
        if not (root / "site/index.html").is_file():
            raise RuntimeError("Static site build failed")
        workspace = root / "governance"
        workspace.mkdir()
        run("trestle", "init", "--govdocs", cwd=workspace)
    print(json.dumps({"uid": os.getuid(), "versions": versions, "offline_exports": "passed"}, indent=2))


if __name__ == "__main__":
    main()
