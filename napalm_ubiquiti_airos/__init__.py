"""napalm_airos package."""

# Import stdlib
import pkg_resources

# Import local modules
from napalm_ubiquiti_airos.airos import AirOSDriver

try:
    __version__ = pkg_resources.get_distribution('napalm-airos').version
except pkg_resources.DistributionNotFound:
    __version__ = "Not installed"

__all__ = ('AirOSDriver', )
