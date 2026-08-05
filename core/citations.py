"""
citations.py
Tracks and manages source citations throughout a conversation session.
Every response Homer gives is grounded in classical sources.
"""


class CitationManager:
    """
    Tracks which classical sources have been referenced
    during the current conversation session.
    """

    # Master list of all classical sources in our knowledge base
    KNOWN_SOURCES = {
        "Homer - Iliad": "Homer's Iliad — Epic poem about the Trojan War (c. 8th century BC)",
        "Homer - Odyssey": "Homer's Odyssey — Epic poem about Odysseus's journey home (c. 8th century BC)",
        "Hesiod - Theogony": "Hesiod's Theogony — Origin of the gods and cosmos (c. 700 BC)",
        "Hesiod - Works and Days": "Hesiod's Works and Days — Ethics and the Five Ages of Man (c. 700 BC)",
        "Homeric Hymn to Apollo": "Homeric Hymn to Apollo — Hymn celebrating Apollo (c. 7th century BC)",
        "Homeric Hymn to Demeter": "Homeric Hymn to Demeter — Story of Persephone's abduction (c. 7th century BC)",
        "Homeric Hymn to Hermes": "Homeric Hymn to Hermes — Birth and exploits of Hermes (c. 6th century BC)",
        "Homeric Hymn to Artemis": "Homeric Hymn to Artemis — Hymn celebrating Artemis (c. 7th century BC)",
        "Apollodorus - The Library": "Apollodorus's The Library — Comprehensive mythology handbook (c. 1st-2nd century AD)",
        "Ovid - Metamorphoses": "Ovid's Metamorphoses — Mythological transformations (c. 8 AD)",
        "Pindar - Odes": "Pindar's Odes — Victory odes referencing myths (c. 5th century BC)",
    }

    def __init__(self):
        self.cited_sources: list[str] = []

    def add_citations(self, sources: list[str]) -> list[str]:
        """Add new citations avoiding duplicates. Returns only the new ones."""
        new_citations = []
        for source in sources:
            if source not in self.cited_sources:
                self.cited_sources.append(source)
                new_citations.append(source)
        return new_citations

    def get_all(self) -> list[str]:
        """Return all citations used in this session."""
        return self.cited_sources

    def format_citations(self) -> str:
        """Format citations as a readable string."""
        if not self.cited_sources:
            return "No sources cited yet."

        lines = ["Sources referenced in this session:"]
        for source in self.cited_sources:
            description = self.KNOWN_SOURCES.get(source, source)
            lines.append(f"  • {description}")
        return "\n".join(lines)

    def clear(self):
        """Reset citations for a new session."""
        self.cited_sources = []