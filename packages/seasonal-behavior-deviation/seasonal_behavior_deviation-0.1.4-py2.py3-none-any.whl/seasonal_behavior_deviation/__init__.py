# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound


from .preprocess import preprocess, add_season_steps  # noqa: E402
from .anomaly_detection import SeasonalBehaviorDeviation  # noqa: E402
from .util import normalize_column  # noqa: E402
