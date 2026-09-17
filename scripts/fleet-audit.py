from pathlib import Path

import runpy

if __name__ == "__main__":
    # Compatibility entry point; inventory v2 replaces this legacy implementation.
    runpy.run_path(str(Path(__file__).with_name("fleet-inventory.py")), run_name="__main__")
