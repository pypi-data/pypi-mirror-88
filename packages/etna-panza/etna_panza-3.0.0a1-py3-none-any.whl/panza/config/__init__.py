"""
Module providing helpers for panza's configuration
"""

from dataclasses import dataclass, field
from typing import List

from panza import metadata


@dataclass
class AdditionalDockerDaemonConfiguration:
    network_bridge_mask: str
    max_wait_time: float = 10.0
    dns: List[str] = field(default_factory=list)


@dataclass
class PanzaConfiguration:
    root_directory: str
    additional_docker_daemon: AdditionalDockerDaemonConfiguration
    base_image: str = f"etnajawa/panza-base:{metadata.__version__}"
    always_pull: bool = False
