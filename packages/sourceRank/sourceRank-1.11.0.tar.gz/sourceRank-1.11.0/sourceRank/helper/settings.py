import coloredlogs, logging
import warnings, os
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

parent_dir: str = os.getenv("PARENT_DIR") if "PARENT_DIR" in os.environ else "sourceRank"
default_field: str = "N/A"
resources_directory: str = os.path.join(parent_dir, "resources")
resources_domains_filename: str = "resources_domains.csv"
