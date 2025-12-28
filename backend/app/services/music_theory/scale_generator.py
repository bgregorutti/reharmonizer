"""
Scale generator service - wraps reharmonizer_core functionality.
"""

from reharmonizer_core.theory import ScaleGenerator as CoreScaleGenerator
from typing import List


class ScaleGenerator:
    """
    Scale generator service.

    Wraps the reharmonizer_core.ScaleGenerator for use in the backend.
    """

    def __init__(self):
        self.core_generator = CoreScaleGenerator()

    def get_major_scale(self, root: str) -> List[str]:
        """Generate a major scale."""
        return self.core_generator.get_major_scale(root)

    def get_minor_scale(self, root: str, mode: str = "natural") -> List[str]:
        """Generate a minor scale."""
        return self.core_generator.get_minor_scale(root, mode)

    def get_scale_for_key(self, key_name: str, mode: str) -> List[str]:
        """Get scale notes for a key signature."""
        return self.core_generator.get_scale_for_key(key_name, mode)

    def get_chromatic_scale(self, starting_note: str = "C") -> List[str]:
        """Get chromatic scale."""
        return self.core_generator.get_chromatic_scale(starting_note)
