import boto3
import contextlib
import io
import logging
from bmlx.fs.file_system import FileSystem
from bmlx.config import ConfigError, NotFoundError
from typing import Text, Dict


class CephFileSystem(FileSystem):
    def _resolove_path(self, path):
        # ceph://fs-ceph-hk.bigo.sg/bmlx-pipeline/{object-name}
        paths = path.split(self.pathsep)
        paths = [p for p in paths if p != ""]
        return paths[2], self.pathsep.join(paths[3:])

    def __init__(self, endpoint, access_key, secret_key):
        session = boto3.session.Session()
        self.s3_client = session.client(
            service_name="s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def cat(self, path):
        bucket, obj = self._resolove_path(path)
        resp = self.s3_client.get_object(Bucket=bucket, Key=obj)
        return resp["Body"].read()

    def stat(self, path):
        bucket, obj = self._resolove_path(path)
        self.s3_client.head_object(Bucket=bucket, Key=obj)

    def ls(self, path):
        bucket, obj = self._resolove_path(path)
        return [
            ele["Key"][len(obj) + 1 :]
            for ele in self.s3_client.list_objects(
                Bucket=bucket, Prefix=obj
            ).get("Contents", [])
        ]

    def delete(self, path, recursive=False):
        bucket, obj = self._resolove_path(path)
        self.s3_client.delete_object(Bucket=bucket, Key=obj)

    def disk_usage(self, path):
        raise NotImplementedError()

    def _path_join(self, *args):
        return self.pathsep.join(args)

    def rm(self, path, recursive=False):
        return self.delete(path, recursive=recursive)

    def mv(self, path, new_path):
        return self.rename(path, new_path)

    def rename(self, path, new_path):
        self.copy(path, new_path)
        self.rm(path)

    def copy(self, path, new_path):
        bucket, obj = self._resolove_path(new_path)
        self.s3_client.copy_object(Bucket=bucket, CopySource=obj, Key=path)

    def exists(self, path):
        try:
            self.stat(path)
            return True
        except Exception:  # as e:
            # print("stat file get exception %s", e)
            return False

    def _isfilestore(self):
        return False

    @contextlib.contextmanager
    def open(self, path, mode="rb"):
        bucket, obj = self._resolove_path(path)
        if "w" in mode:
            try:
                b = bytes()
                streaming = io.BytesIO(b)
                yield streaming
            finally:
                streaming.seek(0)
                self.s3_client.put_object(
                    Bucket=bucket,
                    Key=obj,
                    Body=streaming.read(),
                    ContentLength=len(streaming.getbuffer()),
                )
        elif "r" in mode:
            try:
                resp = self.s3_client.get_object(Bucket=bucket, Key=obj)
                yield resp["Body"]
            finally:
                resp["Body"].close()
        else:
            raise RuntimeError("unknown mode %s" % mode)

    @property
    def pathsep(self):
        return "/"
