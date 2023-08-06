import logging
import subprocess
import sys


log = logging.getLogger(__name__)


def install_requirements(req_file):
    """Install requirements from a file programatically

    Args:
        req_file (str): Path to requirements file

    Raises:
        SystemExit: If there was an error from pip
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
    except subprocess.CalledProcessError as e:
        log.error(f"Could not install requirements, pip exit code {e.returncode}")
        sys.exit(1)
