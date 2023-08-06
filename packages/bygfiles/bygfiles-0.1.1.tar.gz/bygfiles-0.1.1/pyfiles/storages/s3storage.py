import os
import boto3
import botocore

from pyfiles.storages.core import Storage


class S3Storage(Storage):
    def __init__(
        self,
        access_key=None,
        secret_key=None,
        endpoint_url=None,
        region_name=None,
        bucket_name="",
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.bucket_name = bucket_name

    def get_client(self):
        if not hasattr(self, "_s3"):
            self._s3 = boto3.resource(
                "s3",
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
                region_name=self.region_name,
            )

        return self._s3

    def _generate_temp_url(self, obj):
        return self.get_client().meta.client.generate_presigned_url(
            "get_object", Params={"Bucket": self.bucket_name, "Key": obj.key}
        )

    async def search(self, namespace, filename, version="latest"):
        s3 = self.get_client()

        if version == "latest":
            version_prefix = ""
        else:
            version_prefix = version

        bucket = s3.Bucket(self.bucket_name)

        filelist = []
        for obj in bucket.objects.filter(Prefix="/".join(namespace.split("."))):

            if obj.key.endswith(filename):  # Filter only wanted filename
                full_obj = s3.Object(self.bucket_name, obj.key)
                obj_version = full_obj.metadata.get(
                    "version"
                )  # Extract version from metadata

                if obj_version and obj_version.startswith(
                    version_prefix
                ):  # Filter version
                    filelist.append((obj_version, full_obj))

        if not filelist:
            return None

        selected_file = sorted(filelist, key=lambda x: x[0])[-1][1]

        return {
            "version": selected_file.metadata["version"],
            "url": self._generate_temp_url(selected_file),
        }

    async def versions(self, namespace, filename):
        s3 = self.get_client()

        bucket = s3.Bucket(self.bucket_name)

        filelist = []
        for obj in bucket.objects.filter(Prefix="/".join(namespace.split("."))):

            if obj.key.endswith(filename):  # Filter only wanted filename
                full_obj = s3.Object(self.bucket_name, obj.key)
                obj_version = full_obj.metadata.get(
                    "version"
                )  # Extract version from metadata

                filelist.append((obj_version, full_obj))

        return [o[0] for o in filelist]

    async def store(self, stream, namespace, filename, version):
        s3 = self.get_client()

        # FIXME can we use os.path join here ?
        fname = "/".join(namespace.split(".")) + f"/{version}/{filename}"

        # TODO make it async
        s3.Bucket(self.bucket_name).put_object(
            Key=fname, Body=stream, Metadata={"version": version}
        )

    async def delete(self, namespace, filename, version):
        s3 = self.get_client()

        # FIXME can we use os.path join here ?
        fname = "/".join(namespace.split(".")) + f"/{version}/{filename}"

        # TODO make it async
        s3.Object(self.bucket_name, fname).delete()
