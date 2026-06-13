#!/usr/bin/env python3
"""
Mirror the site's training videos into Cloudflare R2.

Run from the repo root with credentials supplied via environment variables:

  R2_ENDPOINT=https://...r2.cloudflarestorage.com
  R2_ACCESS_KEY_ID=...
  R2_SECRET_ACCESS_KEY=...
  python Scripts/sync_r2_videos.py

The script pulls current video targets from the HTML pages in this repo,
resolves their legacy source files from cte-auto.net, converts non-MP4
sources into H.264/AAC MP4s, and uploads each file to the R2 bucket using
the same object key the site expects.
"""

from __future__ import annotations

import concurrent.futures as futures
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlparse

import boto3
from botocore.config import Config
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[1]
OLD_SITE = "https://www.cte-auto.net/"
DEFAULT_BUCKET = "bulldog-garage-videos"
DEFAULT_WORKERS = 4

TARGET_RE = re.compile(r"player\.html\?v=([^\"'&]+)")
MEDIA_RE = re.compile(r"""(?:href|src)=["']([^"'#]+)["']""", re.IGNORECASE)
VIDEO_EXTS = [
    ".mp4",
    ".MP4",
    ".m4v",
    ".M4V",
    ".mov",
    ".MOV",
    ".avi",
    ".AVI",
    ".wmv",
    ".WMV",
    ".flv",
    ".FLV",
    ".mpg",
    ".MPG",
    ".mpeg",
    ".MPEG",
]
PACKAGED_VIDEO_EXTS = {".mp4", ".m4v"}


def decode_path(value: str) -> str:
    return unquote(value)


def normalize_stem(path_value: str) -> str:
    return Path(path_value).with_suffix("").as_posix().lower().lstrip("/")


def build_s3_client():
    endpoint = os.environ.get("R2_ENDPOINT", "").strip()
    account_id = os.environ.get("R2_ACCOUNT_ID", "").strip()
    if not endpoint and account_id:
        endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
    if not endpoint:
        raise SystemExit("Set R2_ENDPOINT or R2_ACCOUNT_ID before running this script.")

    access_key = os.environ.get("R2_ACCESS_KEY_ID", "").strip()
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY", "").strip()
    if not access_key or not secret_key:
        raise SystemExit("Set R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY before running this script.")

    region = os.environ.get("R2_REGION", "auto").strip() or "auto"
    session = boto3.session.Session()
    return session.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            retries={"max_attempts": 10, "mode": "standard"},
        ),
    )


def collect_current_targets() -> list[str]:
    targets = set()
    for html_path in ROOT.rglob("*.html"):
        try:
            html = html_path.read_text(errors="ignore")
        except Exception:
            continue
        for match in TARGET_RE.finditer(html):
            targets.add(decode_path(match.group(1)))
    return sorted(targets)


def fetch_text(url: str) -> str:
    result = subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--retry",
            "3",
            "--retry-delay",
            "2",
            url,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def build_legacy_map() -> dict[str, str]:
    pages = [
        "intro.html",
        "maintenance.html",
        "brakes.html",
        "ss.html",
        "electrical.html",
        "fun-page1.html",
        "JobSearch.html",
    ]
    lookup: dict[str, str] = {}
    for page in pages:
        page_url = urljoin(OLD_SITE, page)
        try:
            html = fetch_text(page_url)
        except subprocess.CalledProcessError as exc:
            print(f"[warn] Could not fetch legacy page {page_url}: {exc}")
            continue

        for raw_ref in MEDIA_RE.findall(html):
            abs_url = urljoin(page_url, raw_ref)
            parsed = urlparse(abs_url)
            path = unquote(parsed.path)
            if Path(path).suffix.lower() not in {
                ".mp4",
                ".m4v",
                ".mov",
                ".avi",
                ".wmv",
                ".flv",
                ".mpg",
                ".mpeg",
            }:
                continue
            lookup.setdefault(normalize_stem(path), abs_url)
    return lookup


def candidate_sources(target_key: str, legacy_map: dict[str, str]) -> list[str]:
    candidates: list[str] = []
    stem = normalize_stem(target_key)

    if stem in legacy_map:
        candidates.append(legacy_map[stem])

    encoded_exact = quote(target_key, safe="/")
    candidates.append(urljoin(OLD_SITE, encoded_exact))

    base_stem = Path(target_key).with_suffix("").as_posix()
    for ext in VIDEO_EXTS:
        candidates.append(urljoin(OLD_SITE, quote(base_stem + ext, safe="/")))

    deduped: list[str] = []
    seen = set()
    for url in candidates:
        if url not in seen:
            seen.add(url)
            deduped.append(url)
    return deduped


def download_url(url: str, destination: Path) -> None:
    result = subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--retry",
            "3",
            "--retry-delay",
            "2",
            "--output",
            str(destination),
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.args)


def transcode_to_mp4(source: Path, destination: Path) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    if source.suffix.lower() in PACKAGED_VIDEO_EXTS:
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(source),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(destination),
            ],
            check=True,
        )
        return

    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-vf",
            "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "22",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            str(destination),
        ],
        check=True,
    )


def upload_file(client, bucket: str, key: str, file_path: Path) -> None:
    client.upload_file(
        str(file_path),
        bucket,
        key,
        ExtraArgs={
            "ContentType": "video/mp4",
            "CacheControl": "public, max-age=31536000, immutable",
        },
    )


def process_target(target_key: str, legacy_map: dict[str, str], bucket: str) -> tuple[str, str, str]:
    s3 = build_s3_client()
    target_path = ROOT / target_key
    with tempfile.TemporaryDirectory(prefix="bulldog-r2-") as tmpdir:
        tmp = Path(tmpdir)
        source_path = None
        source_note = ""
        if target_path.exists():
            source_path = target_path
            source_note = "local"
        else:
            for candidate in candidate_sources(target_key, legacy_map):
                dest = tmp / Path(urlparse(candidate).path).name
                try:
                    download_url(candidate, dest)
                except subprocess.CalledProcessError:
                    continue
                source_path = dest
                source_note = candidate
                break

        if source_path is None:
            raise FileNotFoundError(f"No source found for {target_key}")

        final_path = source_path
        if source_path.suffix.lower() in PACKAGED_VIDEO_EXTS:
            final_path = tmp / (Path(target_key).stem + ".mp4")
            if final_path != source_path:
                transcode_to_mp4(source_path, final_path)
        else:
            final_path = tmp / (Path(target_key).stem + ".mp4")
            transcode_to_mp4(source_path, final_path)

        upload_file(s3, bucket, target_key, final_path)
        return target_key, source_note, str(final_path.stat().st_size)


def main() -> int:
    bucket = os.environ.get("R2_BUCKET", DEFAULT_BUCKET).strip() or DEFAULT_BUCKET
    workers = int(os.environ.get("R2_WORKERS", str(DEFAULT_WORKERS)))

    targets = collect_current_targets()
    print(f"Found {len(targets)} unique video targets.", flush=True)
    legacy_map = build_legacy_map()
    print(f"Built legacy source map with {len(legacy_map)} entries.", flush=True)

    missing: list[str] = []
    completed = 0
    with futures.ThreadPoolExecutor(max_workers=workers) as pool:
        future_map = {
            pool.submit(process_target, target, legacy_map, bucket): target
            for target in targets
        }
        for future in futures.as_completed(future_map):
            target = future_map[future]
            try:
                key, source_note, size = future.result()
                completed += 1
                print(f"[{completed}/{len(targets)}] uploaded {key} ({size} bytes) from {source_note}", flush=True)
            except Exception as exc:
                missing.append(target)
                print(f"[error] {target}: {exc}", flush=True)

    if missing:
        print("\nMissing or failed uploads:", flush=True)
        for item in missing:
            print(f" - {item}", flush=True)
        return 1

    print("\nAll video targets uploaded successfully.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
