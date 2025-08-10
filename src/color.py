class Color:
    """Discrete color palette for organisms."""

    # 8 distinct colors for even distribution
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    VIOLET = (128, 0, 255)
    ORANGE = (255, 128, 0)  # Completes the palette

    # List for easy indexing
    PALETTE = [
        CYAN,
        MAGENTA,
        YELLOW,
        GREEN,
        BLUE,
        RED,
        VIOLET,
        ORANGE
    ]

    @classmethod
    def from_genome(cls, genome_string):
        """Get a color from the palette based on genome checksum."""
        import hashlib

        # Use MD5 hash for good distribution
        hash_value = hashlib.md5(genome_string.encode()).hexdigest()
        # Convert first few hex chars to int
        index = int(hash_value[:8], 16) % len(cls.PALETTE)

        return cls.PALETTE[index]
