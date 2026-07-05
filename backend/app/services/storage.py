from __future__ import annotations

import uuid
from pathlib import Path

import boto3

from app.core.config import get_settings


class StorageService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.local_upload_dir = Path("uploads")
        self.local_upload_dir.mkdir(exist_ok=True)
        self.s3_client = None
        if self.settings.aws_access_key_id and self.settings.aws_secret_access_key and self.settings.s3_bucket:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.settings.aws_access_key_id,
                aws_secret_access_key=self.settings.aws_secret_access_key,
                region_name=self.settings.aws_default_region,
            )

    def save_bytes(self, content: bytes, suffix: str = ".png") -> tuple[str, str]:
        key = f"generated/{uuid.uuid4().hex}{suffix}"
        if self.s3_client:
            self.s3_client.put_object(
                Bucket=self.settings.s3_bucket,
                Key=key,
                Body=content,
                ContentType="image/png",
            )
            url = f"https://{self.settings.s3_bucket}.s3.amazonaws.com/{key}"
            return key, url

        target = self.local_upload_dir / Path(key).name
        target.write_bytes(content)
        return key, f"/static/{target.name}"

