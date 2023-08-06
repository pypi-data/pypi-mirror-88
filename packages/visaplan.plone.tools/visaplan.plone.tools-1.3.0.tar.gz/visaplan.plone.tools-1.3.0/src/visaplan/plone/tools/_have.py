# detect optional packages

# Setup tools:
import pkg_resources

try:
    pkg_resources.get_distribution('visaplan.plone.subportals')
except pkg_resources.DistributionNotFound:
    HAS_SUBPORTALS = False
else:
    HAS_SUBPORTALS = True

try:
    pkg_resources.get_distribution('visaplan.plone.search')
except pkg_resources.DistributionNotFound:
    HAS_VPSEARCH = False
else:
    HAS_VPSEARCH = True
