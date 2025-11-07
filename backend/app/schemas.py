"""
Legacy schemas file for backward compatibility.
All schemas are now in the schemas/ package.
This file re-exports them for any code still using direct imports.
"""
# Re-export all schemas from the schemas package
from .schemas import *  # noqa
