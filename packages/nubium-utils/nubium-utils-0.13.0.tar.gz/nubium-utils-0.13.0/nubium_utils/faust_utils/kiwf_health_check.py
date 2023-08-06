import sys
from logging import getLogger
from collections import deque
from nubium_utils import init_logger
from nubium_utils.faust_utils.faust_runtime_vars import default_env_vars


def kiwf(errors):
    init_logger(__name__)
    getLogger(__name__).error(f"KIWF encountered error(s): [{', '.join(errors)}].\nKilling Pod.")
    sys.exit(1)


def kiwf_log_analysis():
    lines_to_tail = 10
    last_lines = str(deque(open(default_env_vars()['KIWF_LOG_FILEPATH']), lines_to_tail))

    if '[^---Fetcher]: Starting...' in last_lines:
        if '[^Worker]: Ready' not in last_lines:
            kiwf(['POD STUCK ON STARTING (Fetcher)'])

    if '[^---Recovery]: Resuming flow...' in last_lines:
        if '[^---Recovery]: Recovery complete' not in last_lines or '[^---Recovery]: Still fetching changelog topics' not in last_lines:
            kiwf(['POD STUCK ON STARTING (Recovery)'])

    errors = [error_string for error_string in default_env_vars()['KIWF_ERROR_STRINGS'].split(',') if
              error_string in last_lines]
    if errors:
        kiwf(errors)
