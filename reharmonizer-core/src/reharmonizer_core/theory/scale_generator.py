"""Scale generation utilities."""

from typing import List
from music21 import scale as m21_scale, pitch as m21_pitch


class ScaleGenerator:
    """Generate musical scales."""

    @staticmethod
    def get_major_scale(root: str) -> List[str]:
        """
        Generate a major scale.

        Args:
            root: Root note name (e.g., "C")

        Returns:
            List of note names in the major scale
        """
        try:
            scale = m21_scale.MajorScale(root)
            return [p.name for p in scale.pitches]
        except Exception:
            return []

    @staticmethod
    def get_minor_scale(root: str, mode: str = "natural") -> List[str]:
        """
        Generate a minor scale.

        Args:
            root: Root note name
            mode: Type of minor scale ("natural", "harmonic", "melodic")

        Returns:
            List of note names
        """
        try:
            if mode == "harmonic":
                scale = m21_scale.HarmonicMinorScale(root)
            elif mode == "melodic":
                scale = m21_scale.MelodicMinorScale(root)
            else:  # natural
                scale = m21_scale.MinorScale(root)

            return [p.name for p in scale.pitches]
        except Exception:
            return []

    @staticmethod
    def get_scale_for_key(key_name: str, mode: str) -> List[str]:
        """
        Get scale notes for a key signature.

        Args:
            key_name: Key name (e.g., "C", "G", "Bb")
            mode: "major" or "minor"

        Returns:
            List of note names
        """
        if mode.lower() == "major":
            return ScaleGenerator.get_major_scale(key_name)
        else:
            return ScaleGenerator.get_minor_scale(key_name, "natural")

    @staticmethod
    def get_chromatic_scale(starting_note: str = "C") -> List[str]:
        """
        Get chromatic scale.

        Args:
            starting_note: Starting note (default: "C")

        Returns:
            List of all 12 chromatic notes starting from the given note
        """
        chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        try:
            start_index = chromatic.index(starting_note)
            return chromatic[start_index:] + chromatic[:start_index]
        except ValueError:
            return chromatic
