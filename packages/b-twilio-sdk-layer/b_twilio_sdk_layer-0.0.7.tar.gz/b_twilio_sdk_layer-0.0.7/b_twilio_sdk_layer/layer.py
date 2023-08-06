from functools import lru_cache
from typing import List, Optional

from aws_cdk.aws_lambda import Code, LayerVersion, Runtime
from aws_cdk.core import Stack, AssetHashType, BundlingOptions, BundlingDockerImage


class Layer(LayerVersion):
    def __init__(self, scope: Stack, name: str, boto3_version: Optional[str] = None):
        install_command = [
            'pip install -r requirements.txt -t /tmp/asset-output/python',
        ]

        if boto3_version:
            install_command.append(f'pip install boto3=={boto3_version} -t /tmp/asset-output/python')

        build_command = [
            'find /tmp/asset-output -type f -name "*.py[co]" -delete',
            'find /tmp/asset-output -type d -name "__pycache__" -delete',
            'cp -R /tmp/asset-output/. /asset-output/.',
            'ls -laR /asset-output/.'
        ]

        super().__init__(
            scope=scope,
            id=name,
            layer_version_name=name,
            code=Code.from_asset(
                self.get_source_path(),
                asset_hash_type=AssetHashType.BUNDLE,
                bundling=BundlingOptions(
                    image=BundlingDockerImage.from_registry('python:3.9'),
                    command=[
                        'bash', '-c', ' && '.join(install_command + build_command)
                    ]
                )
            ),
            compatible_runtimes=self.runtimes()
        )

    @lru_cache
    def get_source_path(self) -> str:
        """
        Returns path to layer source.

        :return: Path to layer source.
        """
        from .source import root
        return root

    def runtimes(self) -> List[Runtime]:
        """
        Available runtimes for lambda functions.

        :return: List of available runtimes.
        """
        return [
            Runtime.PYTHON_2_7,
            Runtime.PYTHON_3_6,
            Runtime.PYTHON_3_7,
            Runtime.PYTHON_3_8
        ]
