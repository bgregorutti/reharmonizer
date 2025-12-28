"""Constants used throughout the application."""

# Common chord qualities
CHORD_QUALITIES = {
    "major": "major",
    "minor": "minor",
    "diminished": "diminished",
    "augmented": "augmented",
    "major7": "major7",
    "minor7": "minor7",
    "dominant7": "dominant7",
    "diminished7": "diminished7",
    "half_diminished7": "half-diminished7",
}

# Notes in chromatic scale
CHROMATIC_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Circle of fifths
CIRCLE_OF_FIFTHS = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]

# Common substitution types
SUBSTITUTION_TYPES = {
    "tritone": "tritone",
    "diatonic": "diatonic",
    "chromatic": "chromatic",
    "circle_of_fifths": "circle_of_fifths",
}

# Intervals in semitones
INTERVALS = {
    "unison": 0,
    "minor_second": 1,
    "major_second": 2,
    "minor_third": 3,
    "major_third": 4,
    "perfect_fourth": 5,
    "tritone": 6,
    "perfect_fifth": 7,
    "minor_sixth": 8,
    "major_sixth": 9,
    "minor_seventh": 10,
    "major_seventh": 11,
    "octave": 12,
}
