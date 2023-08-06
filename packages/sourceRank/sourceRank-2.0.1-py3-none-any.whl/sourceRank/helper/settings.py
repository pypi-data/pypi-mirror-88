import coloredlogs, logging
import warnings, os

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

default_field: str = "N/A"
resources_directory: str = "resources"
resources_domains_filename: str = "resources_domains.csv"
