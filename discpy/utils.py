from pathlib import PurePosixPath


def generate_deterministic_url_path(*segments: str) -> str:
    return PurePosixPath(*map(lambda x: x.lstrip('/'), segments)).as_posix()
