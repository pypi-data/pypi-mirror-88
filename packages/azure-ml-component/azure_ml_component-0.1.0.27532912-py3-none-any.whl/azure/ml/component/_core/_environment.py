# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import Optional
from ._core import AssetVersion


class Environment(AssetVersion):
    """This is a simple implementation of environment, will be replaced by the finalized one."""

    CONDA_FILE_KEY = 'conda_dependencies_file'
    CONDA_DICT_KEY = 'conda_dependencies'

    def __init__(self, conda: dict = None, docker: dict = None, os: str = None):
        """Initialize an environment object with conda, docker and os.

        :param conda: A conda environment dict to represent the python dependencies.
        :param docker: A docker section which contain a docker image to run the component.
        :param os: Indicate which os could run the component. Could be Linux/Windows.
        """
        self._docker = docker
        self._os = os
        self._conda = conda
        self._update_fields()

    @property
    def docker(self):
        return self._docker

    @property
    def conda(self) -> dict:
        return self._conda

    @property
    def conda_dict(self) -> Optional[dict]:
        return None if self._conda is None else self._conda.get(self.CONDA_DICT_KEY)

    @property
    def conda_file(self) -> Optional[str]:
        return None if self._conda is None else self._conda.get(self.CONDA_FILE_KEY)

    @property
    def os(self):
        return self._os

    @classmethod
    def _from_dict(cls, dct):
        return cls(**dct)

    def _to_dict(self):
        return {
            'docker': self.docker,
            'conda': self.conda,
            'os': self.os,
        }

    def _to_aml_sdk_env(self):
        from azureml.core.environment import Environment, CondaDependencies
        env = Environment(name=None, _skip_defaults=True)
        conda = self.conda.get(self.CONDA_DICT_KEY) if self.conda else None
        if conda:
            env.python.conda_dependencies = CondaDependencies(_underlying_structure=conda)
        else:
            # If conda is not set, use the user's custom image.
            env.python.user_managed_dependencies = True
        if self.docker:
            if 'image' in self.docker:
                env.docker.base_image = self.docker['image']
        return env

    def _update_fields(self):
        """Update fields to make it align to new design."""
        if self._os is None:
            self._os = 'Linux'

        if self.conda:
            conda_mapping = {
                'condaDependencies': self.CONDA_DICT_KEY,
                'condaDependenciesFile': self.CONDA_FILE_KEY,
                'pipRequirementsFile': 'pip_requirements_file',
            }
            for k, v in conda_mapping.items():
                if k in self.conda:
                    self.conda[v] = self.conda.pop(k)

        if self.docker:
            docker_mapping = {
                'baseImage': 'image'
            }

            for k, v in docker_mapping.items():
                if k in self.docker:
                    self.docker[v] = self.docker.pop(k)
