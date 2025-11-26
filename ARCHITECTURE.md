# Terpene Vocabulary MCP Server - Architecture

## Overview

Deterministic mapping layer for terpene visual vocabulary. Provides all metadata lookups and parameter calculations without LLM cost.

## Structure

```
terpene-mcp-server/
├── create_structure.sh       # Generate directory structure
├── verify_structure.sh       # Validate structure
├── src/
│   └── terpene_vocabulary/
│       ├── __init__.py
│       ├── server.py         # Main MCP server (manual add)
│       ├── __main__.py       # Local testing entry point
│       └── handler.py        # FastMCP Cloud entry point
├── tests/
│   ├── run_tests.sh         # Test runner script
│   ├── unit/
│   │   └── test_*.py        # Unit tests (manual add)
│   └── integration/
│       └── test_*.py        # Integration tests (manual add)
├── docs/
│   └── examples/            # Usage examples
├── pyproject.toml           # Project config
├── README.md                # Quick reference
└── ARCHITECTURE.md          # This file
```

## Tools

- `list_terpenes()` - Get all terpenes with basic info
- `get_terpene(name)` - Complete metadata for one terpene
- `get_color_palette(name, stage)` - Color specs + temporal adjustments
- `get_temporal_stages(name)` - All 4 stages for a terpene
- `get_composition_rules(name)` - Structural & semantic info
- `get_master_prompt(name, stage)` - The core descriptor for LLM fusion
- `get_chemical_communication(name)` - Biological meaning
- `compare_terpenes(name1, name2)` - Side-by-side comparison
- `suggest_terpene_for_concept(concept)` - Semantic matching
- `apply_intensity_modifier(name, intensity)` - Control fusion strength

## Deployment

### Local
```bash
python -m terpene_vocabulary
```

### FastMCP Cloud
Entry point: `src/terpene_vocabulary/handler.py:handler()`

See full documentation in docs/ for complete API reference.
