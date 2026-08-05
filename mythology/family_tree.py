"""
family_tree.py
Structured relationship data for Greek mythology figures.
This data powers the NetworkX graph engine and the visual
family tree in the UI.

Primary source: Hesiod's Theogony + Apollodorus's The Library
"""

from typing import Any


# ── Node definitions ──────────────────────────────────────────────────────────
# Each figure has: name, category, description, and source
MYTHOLOGY_FIGURES: dict[str, dict[str, Any]] = {

    # Primordial Gods
    "Chaos":      {"category": "primordial", "description": "The first being, a primordial void", "source": "Hesiod - Theogony"},
    "Gaia":       {"category": "primordial", "description": "Goddess of Earth, mother of Titans", "source": "Hesiod - Theogony"},
    "Uranus":     {"category": "primordial", "description": "God of the Sky, father of Titans", "source": "Hesiod - Theogony"},
    "Tartarus":   {"category": "primordial", "description": "The deep abyss, used as dungeon of torment", "source": "Hesiod - Theogony"},
    "Eros":       {"category": "primordial", "description": "Primordial god of Love", "source": "Hesiod - Theogony"},
    "Nyx":        {"category": "primordial", "description": "Goddess of Night", "source": "Hesiod - Theogony"},
    "Erebus":     {"category": "primordial", "description": "God of Darkness", "source": "Hesiod - Theogony"},
    "Pontus":     {"category": "primordial", "description": "God of the Sea, born from Gaia", "source": "Hesiod - Theogony"},

    # Titans
    "Cronus":     {"category": "titan", "description": "Titan ruler of the cosmos, father of Olympians", "source": "Hesiod - Theogony"},
    "Rhea":       {"category": "titan", "description": "Titan goddess, mother of the Olympians", "source": "Hesiod - Theogony"},
    "Oceanus":    {"category": "titan", "description": "Titan god of the ocean river", "source": "Hesiod - Theogony"},
    "Tethys":     {"category": "titan", "description": "Titan goddess of fresh water", "source": "Hesiod - Theogony"},
    "Hyperion":   {"category": "titan", "description": "Titan god of heavenly light", "source": "Hesiod - Theogony"},
    "Theia":      {"category": "titan", "description": "Titan goddess of sight and light", "source": "Hesiod - Theogony"},
    "Coeus":      {"category": "titan", "description": "Titan god of intellect", "source": "Hesiod - Theogony"},
    "Phoebe":     {"category": "titan", "description": "Titan goddess of the moon", "source": "Hesiod - Theogony"},
    "Iapetus":    {"category": "titan", "description": "Titan god, father of Prometheus", "source": "Hesiod - Theogony"},
    "Clymene":    {"category": "titan", "description": "Oceanid, mother of Prometheus", "source": "Hesiod - Theogony"},
    "Mnemosyne":  {"category": "titan", "description": "Titan goddess of memory, mother of the Muses", "source": "Hesiod - Theogony"},
    "Themis":     {"category": "titan", "description": "Titan goddess of law and order", "source": "Hesiod - Theogony"},
    "Prometheus": {"category": "titan", "description": "Titan who gave fire to humanity", "source": "Hesiod - Theogony"},
    "Epimetheus": {"category": "titan", "description": "Titan, brother of Prometheus", "source": "Hesiod - Theogony"},
    "Atlas":      {"category": "titan", "description": "Titan condemned to hold up the sky", "source": "Hesiod - Theogony"},
    "Leto":       {"category": "titan", "description": "Titaness, mother of Apollo and Artemis", "source": "Hesiod - Theogony"},
    "Asteria":    {"category": "titan", "description": "Titaness of falling stars", "source": "Hesiod - Theogony"},

    # Olympians
    "Zeus":       {"category": "olympian", "description": "King of the gods, ruler of Mount Olympus", "source": "Hesiod - Theogony"},
    "Hera":       {"category": "olympian", "description": "Queen of the gods, goddess of marriage", "source": "Hesiod - Theogony"},
    "Poseidon":   {"category": "olympian", "description": "God of the sea and earthquakes", "source": "Homer - Odyssey"},
    "Demeter":    {"category": "olympian", "description": "Goddess of harvest and agriculture", "source": "Homeric Hymn to Demeter"},
    "Hestia":     {"category": "olympian", "description": "Goddess of the hearth and home", "source": "Hesiod - Theogony"},
    "Hades":      {"category": "underworld", "description": "God of the underworld, ruler of the dead", "source": "Hesiod - Theogony"},
    "Athena":     {"category": "olympian", "description": "Goddess of wisdom and warfare strategy", "source": "Hesiod - Theogony"},
    "Apollo":     {"category": "olympian", "description": "God of the sun, music, and prophecy", "source": "Homeric Hymn to Apollo"},
    "Artemis":    {"category": "olympian", "description": "Goddess of the hunt and the moon", "source": "Homeric Hymn to Artemis"},
    "Ares":       {"category": "olympian", "description": "God of war and violence", "source": "Homer - Iliad"},
    "Aphrodite":  {"category": "olympian", "description": "Goddess of love and beauty", "source": "Hesiod - Theogony"},
    "Hephaestus": {"category": "olympian", "description": "God of fire and the forge", "source": "Homer - Iliad"},
    "Hermes":     {"category": "olympian", "description": "Messenger of the gods, god of travel", "source": "Homeric Hymn to Hermes"},
    "Dionysus":   {"category": "olympian", "description": "God of wine, festivity, and theater", "source": "Hesiod - Theogony"},
    "Persephone": {"category": "underworld", "description": "Goddess of spring, queen of the underworld", "source": "Homeric Hymn to Demeter"},
    "Metis":      {"category": "titan", "description": "Titaness of wisdom, first wife of Zeus", "source": "Hesiod - Theogony"},
    "Maia":       {"category": "nymph", "description": "Pleiad nymph, mother of Hermes", "source": "Homeric Hymn to Hermes"},
    "Semele":     {"category": "mortal", "description": "Mortal princess, mother of Dionysus", "source": "Hesiod - Theogony"},
    "Alcmene":    {"category": "mortal", "description": "Mortal woman, mother of Heracles", "source": "Apollodorus - The Library"},
    "Dione":      {"category": "titan", "description": "Titaness, mother of Aphrodite in some accounts", "source": "Homer - Iliad"},

    # Minor Gods
    "Hebe":       {"category": "minor_god", "description": "Goddess of youth, cupbearer of the gods", "source": "Hesiod - Theogony"},
    "Eileithyia": {"category": "minor_god", "description": "Goddess of childbirth", "source": "Hesiod - Theogony"},
    "Eris":       {"category": "minor_god", "description": "Goddess of discord", "source": "Hesiod - Theogony"},
    "Enyo":       {"category": "minor_god", "description": "Goddess of war", "source": "Homer - Iliad"},
    "Phobos":     {"category": "minor_god", "description": "God of fear, son of Ares", "source": "Hesiod - Theogony"},
    "Deimos":     {"category": "minor_god", "description": "God of dread, son of Ares", "source": "Hesiod - Theogony"},
    "Eros":       {"category": "minor_god", "description": "God of love, son of Ares and Aphrodite", "source": "Hesiod - Theogony"},
    "Helios":     {"category": "minor_god", "description": "God of the Sun, son of Hyperion", "source": "Hesiod - Theogony"},
    "Selene":     {"category": "minor_god", "description": "Goddess of the Moon, daughter of Hyperion", "source": "Hesiod - Theogony"},
    "Eos":        {"category": "minor_god", "description": "Goddess of the Dawn, daughter of Hyperion", "source": "Hesiod - Theogony"},
    "Hecate":     {"category": "minor_god", "description": "Goddess of magic and crossroads", "source": "Hesiod - Theogony"},
    "Tyche":      {"category": "minor_god", "description": "Goddess of fortune and prosperity", "source": "Hesiod - Theogony"},
    "Nike":       {"category": "minor_god", "description": "Goddess of victory", "source": "Hesiod - Theogony"},

    # Heroes
    "Heracles":   {"category": "hero", "description": "Greatest Greek hero, son of Zeus and Alcmene", "source": "Apollodorus - The Library"},
    "Perseus":    {"category": "hero", "description": "Hero who slew Medusa, son of Zeus and Danae", "source": "Apollodorus - The Library"},
    "Achilles":   {"category": "hero", "description": "Greatest warrior of the Trojan War", "source": "Homer - Iliad"},
    "Odysseus":   {"category": "hero", "description": "King of Ithaca, hero of the Odyssey", "source": "Homer - Odyssey"},
    "Theseus":    {"category": "hero", "description": "Hero who slew the Minotaur, king of Athens", "source": "Apollodorus - The Library"},
    "Danae":      {"category": "mortal", "description": "Mortal princess, mother of Perseus", "source": "Apollodorus - The Library"},
    "Peleus":     {"category": "hero", "description": "Hero, king of Phthia, father of Achilles", "source": "Homer - Iliad"},
    "Thetis":     {"category": "nymph", "description": "Sea nymph, mother of Achilles", "source": "Homer - Iliad"},
    "Aeacus":     {"category": "hero", "description": "King of Aegina, son of Zeus, judge of the dead", "source": "Apollodorus - The Library"},

    # Nymphs
    "Nereus":      {"category": "primordial", "description": "Ancient sea god, father of the Nereids", "source": "Hesiod - Theogony"},
    "Doris":       {"category": "nymph", "description": "Oceanid, wife of Nereus, mother of the Nereids", "source": "Hesiod - Theogony"},
    "Amphitrite":  {"category": "nymph", "description": "Nereid, queen of the sea, wife of Poseidon", "source": "Hesiod - Theogony"},
    "Galatea":     {"category": "nymph", "description": "Nereid, sea nymph loved by the Cyclops Polyphemus", "source": "Hesiod - Theogony"},
    "Psamathe":    {"category": "nymph", "description": "Nereid, goddess of sand beaches", "source": "Hesiod - Theogony"},
    "Styx":        {"category": "nymph", "description": "Oceanid, goddess of the underworld river", "source": "Hesiod - Theogony"},
    "Eurynome":    {"category": "nymph", "description": "Oceanid, mother of the Graces by Zeus", "source": "Hesiod - Theogony"},
    "Calypso":     {"category": "nymph", "description": "Oceanid nymph who kept Odysseus on her island for seven years", "source": "Homer - Odyssey"},
    "Circe":       {"category": "nymph", "description": "Daughter of Helios, sorceress who transformed Odysseus's men into swine", "source": "Homer - Odyssey"},

    # Muses
    "Calliope":    {"category": "muse", "description": "Muse of epic poetry, greatest of the Muses", "source": "Hesiod - Theogony"},
    "Clio":        {"category": "muse", "description": "Muse of history", "source": "Hesiod - Theogony"},
    "Erato":       {"category": "muse", "description": "Muse of love poetry", "source": "Hesiod - Theogony"},
    "Euterpe":     {"category": "muse", "description": "Muse of music and lyric poetry", "source": "Hesiod - Theogony"},
    "Melpomene":   {"category": "muse", "description": "Muse of tragedy", "source": "Hesiod - Theogony"},
    "Polyhymnia":  {"category": "muse", "description": "Muse of sacred poetry and hymns", "source": "Hesiod - Theogony"},
    "Terpsichore": {"category": "muse", "description": "Muse of dance and chorus", "source": "Hesiod - Theogony"},
    "Thalia":      {"category": "muse", "description": "Muse of comedy and idyllic poetry", "source": "Hesiod - Theogony"},
    "Urania":      {"category": "muse", "description": "Muse of astronomy", "source": "Hesiod - Theogony"},
}


# ── Edge definitions ──────────────────────────────────────────────────────────
# Each edge: (parent, child, relationship_type)
FAMILY_RELATIONSHIPS: list[tuple[str, str, str]] = [

    # Primordial generation
    ("Chaos",    "Gaia",      "parent"),
    ("Chaos",    "Tartarus",  "parent"),
    ("Chaos",    "Eros",      "parent"),
    ("Chaos",    "Nyx",       "parent"),
    ("Chaos",    "Erebus",    "parent"),
    ("Gaia",     "Uranus",    "parent"),
    ("Gaia",     "Pontus",    "parent"),

    # Titans — children of Gaia and Uranus
    ("Gaia",     "Cronus",    "parent"),
    ("Gaia",     "Rhea",      "parent"),
    ("Gaia",     "Oceanus",   "parent"),
    ("Gaia",     "Tethys",    "parent"),
    ("Gaia",     "Hyperion",  "parent"),
    ("Gaia",     "Theia",     "parent"),
    ("Gaia",     "Coeus",     "parent"),
    ("Gaia",     "Phoebe",    "parent"),
    ("Gaia",     "Iapetus",   "parent"),
    ("Gaia",     "Mnemosyne", "parent"),
    ("Gaia",     "Themis",    "parent"),
    ("Uranus",   "Cronus",    "parent"),
    ("Uranus",   "Rhea",      "parent"),
    ("Uranus",   "Oceanus",   "parent"),
    ("Uranus",   "Tethys",    "parent"),
    ("Uranus",   "Hyperion",  "parent"),
    ("Uranus",   "Theia",     "parent"),
    ("Uranus",   "Coeus",     "parent"),
    ("Uranus",   "Phoebe",    "parent"),
    ("Uranus",   "Iapetus",   "parent"),
    ("Uranus",   "Mnemosyne", "parent"),
    ("Uranus",   "Themis",    "parent"),

    # Children of Iapetus and Clymene
    ("Iapetus",  "Prometheus", "parent"),
    ("Iapetus",  "Epimetheus", "parent"),
    ("Iapetus",  "Atlas",      "parent"),
    ("Clymene",  "Prometheus", "parent"),
    ("Clymene",  "Epimetheus", "parent"),
    ("Clymene",  "Atlas",      "parent"),

    # Children of Hyperion and Theia
    ("Hyperion", "Helios",    "parent"),
    ("Hyperion", "Selene",    "parent"),
    ("Hyperion", "Eos",       "parent"),
    ("Theia",    "Helios",    "parent"),
    ("Theia",    "Selene",    "parent"),
    ("Theia",    "Eos",       "parent"),

    # Children of Coeus and Phoebe
    ("Coeus",    "Leto",      "parent"),
    ("Coeus",    "Asteria",   "parent"),
    ("Phoebe",   "Leto",      "parent"),
    ("Phoebe",   "Asteria",   "parent"),

    # Olympians — children of Cronus and Rhea
    ("Cronus",   "Zeus",      "parent"),
    ("Cronus",   "Hera",      "parent"),
    ("Cronus",   "Poseidon",  "parent"),
    ("Cronus",   "Demeter",   "parent"),
    ("Cronus",   "Hestia",    "parent"),
    ("Cronus",   "Hades",     "parent"),
    ("Rhea",     "Zeus",      "parent"),
    ("Rhea",     "Hera",      "parent"),
    ("Rhea",     "Poseidon",  "parent"),
    ("Rhea",     "Demeter",   "parent"),
    ("Rhea",     "Hestia",    "parent"),
    ("Rhea",     "Hades",     "parent"),

    # Children of Zeus and Hera
    ("Zeus",     "Ares",       "parent"),
    ("Zeus",     "Hebe",       "parent"),
    ("Zeus",     "Hephaestus", "parent"),
    ("Zeus",     "Eileithyia", "parent"),
    ("Hera",     "Ares",       "parent"),
    ("Hera",     "Hebe",       "parent"),
    ("Hera",     "Hephaestus", "parent"),
    ("Hera",     "Eileithyia", "parent"),

    # Children of Zeus with others
    ("Zeus",     "Athena",     "parent"),
    ("Metis",    "Athena",     "parent"),
    ("Zeus",     "Apollo",     "parent"),
    ("Zeus",     "Artemis",    "parent"),
    ("Leto",     "Apollo",     "parent"),
    ("Leto",     "Artemis",    "parent"),
    ("Zeus",     "Hermes",     "parent"),
    ("Maia",     "Hermes",     "parent"),
    ("Zeus",     "Dionysus",   "parent"),
    ("Semele",   "Dionysus",   "parent"),
    ("Zeus",     "Heracles",   "parent"),
    ("Alcmene",  "Heracles",   "parent"),
    ("Zeus",     "Perseus",    "parent"),
    ("Danae",    "Perseus",    "parent"),
    ("Zeus",     "Persephone", "parent"),
    ("Demeter",  "Persephone", "parent"),

    # Children of Ares and Aphrodite
    ("Ares",     "Phobos",    "parent"),
    ("Ares",     "Deimos",    "parent"),
    ("Ares",     "Eros",      "parent"),
    ("Ares",     "Eris",      "parent"),
    ("Ares",     "Enyo",      "parent"),
    ("Aphrodite","Phobos",    "parent"),
    ("Aphrodite","Deimos",    "parent"),
    ("Aphrodite","Eros",      "parent"),

    # Other children of Zeus (minor gods)
    ("Zeus",      "Nike",     "parent"),
    ("Zeus",      "Tyche",    "parent"),

    # Heroes
    ("Zeus",    "Aeacus",  "parent"),
    ("Aeacus",  "Peleus",  "parent"),
    ("Peleus",   "Achilles",  "parent"),
    ("Thetis",   "Achilles",  "parent"),

    # Marriages
    ("Zeus",     "Hera",      "spouse"),
    ("Cronus",   "Rhea",      "spouse"),
    ("Oceanus",  "Tethys",    "spouse"),
    ("Hyperion", "Theia",     "spouse"),
    ("Coeus",    "Phoebe",    "spouse"),
    ("Iapetus",  "Clymene",   "spouse"),
    ("Hades",    "Persephone","spouse"),
    ("Hephaestus","Aphrodite","spouse"),
    ("Peleus",   "Thetis",    "spouse"),

    # Nymph edges
    ("Oceanus",  "Doris",      "parent"),
    ("Tethys",   "Doris",      "parent"),
    ("Oceanus",  "Styx",       "parent"),
    ("Tethys",   "Styx",       "parent"),
    ("Oceanus",  "Eurynome",   "parent"),
    ("Tethys",   "Eurynome",   "parent"),
    ("Oceanus",  "Calypso",    "parent"),
    ("Tethys",   "Calypso",    "parent"),
    ("Nereus",   "Amphitrite", "parent"),
    ("Doris",    "Amphitrite", "parent"),
    ("Nereus",   "Galatea",    "parent"),
    ("Doris",    "Galatea",    "parent"),
    ("Nereus",   "Psamathe",   "parent"),
    ("Doris",    "Psamathe",   "parent"),
    ("Nereus",   "Thetis",     "parent"),
    ("Doris",    "Thetis",     "parent"),
    ("Helios",   "Circe",      "parent"),

    # Muse edges
    ("Zeus",      "Calliope",    "parent"),
    ("Mnemosyne", "Calliope",    "parent"),
    ("Zeus",      "Clio",        "parent"),
    ("Mnemosyne", "Clio",        "parent"),
    ("Zeus",      "Erato",       "parent"),
    ("Mnemosyne", "Erato",       "parent"),
    ("Zeus",      "Euterpe",     "parent"),
    ("Mnemosyne", "Euterpe",     "parent"),
    ("Zeus",      "Melpomene",   "parent"),
    ("Mnemosyne", "Melpomene",   "parent"),
    ("Zeus",      "Polyhymnia",  "parent"),
    ("Mnemosyne", "Polyhymnia",  "parent"),
    ("Zeus",      "Terpsichore", "parent"),
    ("Mnemosyne", "Terpsichore", "parent"),
    ("Zeus",      "Thalia",      "parent"),
    ("Mnemosyne", "Thalia",      "parent"),
    ("Zeus",      "Urania",      "parent"),
    ("Mnemosyne", "Urania",      "parent"),
]


def get_figures() -> dict[str, dict[str, Any]]:
    """Return all mythology figures."""
    return MYTHOLOGY_FIGURES


def get_relationships() -> list[tuple[str, str, str]]:
    """Return all family relationships."""
    return FAMILY_RELATIONSHIPS