"""
Motor Insurance Claims & Policy Analytics Package.

Exposes standard submodules and ensures reliable import resolution across environments:
- logger
- data_loader
- validation
- data_cleaner
- insurance_analysis
- visualization
- insights
"""

import os
import sys
import importlib.util

__version__ = "1.0.0"

_src_dir = os.path.dirname(os.path.abspath(__file__))

# Explicitly register submodules in sys.modules to bypass filesystem directory-cache latencies
_MODULE_LOAD_ORDER = [
    "logger",
    "data_loader",
    "validation",
    "data_cleaner",
    "insurance_analysis",
    "visualization",
    "insights"
]

for _name in _MODULE_LOAD_ORDER:
    _full_name = f"src.{_name}"
    _file_path = os.path.join(_src_dir, f"{_name}.py")
    if os.path.isfile(_file_path) and _full_name not in sys.modules:
        _spec = importlib.util.spec_from_file_location(_full_name, _file_path)
        if _spec and _spec.loader:
            _mod = importlib.util.module_from_spec(_spec)
            sys.modules[_full_name] = _mod
            _spec.loader.exec_module(_mod)

# Expose modules at package level
for _name in _MODULE_LOAD_ORDER:
    _full_name = f"src.{_name}"
    if _full_name in sys.modules:
        globals()[_name] = sys.modules[_full_name]

__all__ = _MODULE_LOAD_ORDER
