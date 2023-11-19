import platform
import sys
from importlib.metadata import Distribution, version
from operator import itemgetter
from typing import ClassVar, Dict, List, Optional

from .base import DebugPanel


__all__ = ("VersionDebugPanel",)
aiohttp_version = version("aiohttp")


class VersionDebugPanel(DebugPanel):
    """
    Panel that displays the Python version, the aiohttp version, and the
    versions of other software on your PYTHONPATH.
    """

    name = "Version"
    has_content = True
    template = "versions.jinja2"
    title = "Versions"
    nav_title = title
    packages: ClassVar[Optional[List[Dict[str, str]]]] = None

    def __init__(self, request):
        super().__init__(request)
        self.data = {
            "platform": self.get_platform(),
            "packages": self.get_packages(),
            "aiohttp_version": aiohttp_version,
        }

    @classmethod
    def get_packages(cls) -> List[Dict[str, str]]:
        if VersionDebugPanel.packages:
            return VersionDebugPanel.packages

        packages = []
        for distribution in Distribution.discover():
            name = distribution.metadata["Name"]
            dependencies = [d for d in distribution.requires or ()]
            url = distribution.metadata.get("Home-page")

            packages.append(
                {
                    "version": distribution.version,
                    "lowername": name.lower(),
                    "name": name,
                    "dependencies": dependencies,
                    "url": url,
                }
            )

        VersionDebugPanel.packages = sorted(packages, key=itemgetter("lowername"))
        return VersionDebugPanel.packages

    def _get_platform_name(self):
        return platform.platform()

    def get_platform(self):
        return f"Python {sys.version} on {self._get_platform_name()}"
