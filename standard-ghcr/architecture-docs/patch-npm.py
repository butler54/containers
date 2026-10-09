"""Install verified npm distribution and two same-major vendored security fixes."""
import base64
import hashlib
import io
from pathlib import Path
import shutil
import tarfile
import urllib.request

ROOT = Path("/usr/local/lib/node_modules/npm")


def install(url: str, digest: str, destination: Path, algorithm: str = "sha256") -> None:
    with urllib.request.urlopen(url, timeout=120) as response:
        content = response.read()
    actual = hashlib.new(algorithm, content).digest()
    expected = bytes.fromhex(digest) if algorithm == "sha256" else base64.b64decode(digest)
    if actual != expected:
        raise RuntimeError(f"Checksum mismatch for {url}")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as archive:
        for member in archive.getmembers():
            path = Path(member.name)
            if not path.parts or path.parts[0] != "package":
                raise RuntimeError("Unexpected package archive prefix")
            if len(path.parts) == 1:
                continue
            member.name = str(Path(*path.parts[1:]))
            archive.extract(member, path=destination, filter="data")


install("https://registry.npmjs.org/npm/-/npm-11.19.1.tgz",
        "9f58bff01604cb1b14008fef14dceb14d836a49225e45c6c2e37de3be3e707f0", ROOT)
install("https://registry.npmjs.org/brace-expansion/-/brace-expansion-5.0.11.tgz",
        "awigjhi6cLTh90bdw6+QJ9CtmJmyYhEIi70iCbc8Rozn04Fw9FeQIBjv/E22FFGuCGx1bLJyUfB64x/szUSXUg==",
        ROOT / "node_modules/brace-expansion", "sha512")
install("https://registry.npmjs.org/undici/-/undici-6.28.1.tgz",
        "zWpdTVD54H48CIybL0rWQ3ukpb9d23wM7eH5RtfdmeP70cWHNjtfo7P4vZX+5CoDcO53J4Pu5uXp7lNfjc6DRA==",
        ROOT / "node_modules/undici", "sha512")
