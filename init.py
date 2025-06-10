"""Compatibility shim for importing :class:`DynamicPromptImporter` from the
repository root.

This file simply re-exports the real implementation located in the
``dynamic_prompt_importer`` package so that older examples using
``from init import DynamicPromptImporter`` continue to work.
"""

from dynamic_prompt_importer import DynamicPromptImporter

__all__ = ["DynamicPromptImporter"]
