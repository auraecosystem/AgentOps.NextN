import importlib.util
import json
import os
import subprocess
import sys
import time
import types
import warnings
from collections import defaultdict
from pathlib import Path

warnings.filterwarnings("ignore")
import logging
logging.disable(logging.WARNING)
logging.disable(logging.CRITICAL)

WORKING_DIR = Path("/kaggle/working")
WORKING_DIR.mkdir(parents=True, exist_ok=True)

TRUE_SUBMISSION = os.environ.get("KAGGLE_IS_COMPETITION_RERUN", "").strip().lower() in {"1", "true"}
print(f"Submission mode: {TRUE_SUBMISSION}")
