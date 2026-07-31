"""Compatibility entrypoint for the handbook static-site build."""

from pathlib import Path

from handbook_builder import build_site


if __name__ == "__main__":
    repository_root = Path(__file__).resolve().parent
    build_site(repository_root, repository_root / "site")
