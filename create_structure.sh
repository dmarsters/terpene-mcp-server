#!/bin/bash
# Create directory structure and small files for terpene-vocabulary-mcp server
# Usage: bash create_structure.sh

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "Creating directory structure..."

# Core directories
mkdir -p src/terpene_vocabulary
mkdir -p tests
mkdir -p docs

# Test subdirectories
mkdir -p tests/unit
mkdir -p tests/integration

# Documentation
mkdir -p docs/examples

echo "Creating small files..."

# .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
.coverage
htmlcov/
.tox/
.venv
env/
venv/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
EOF

# __init__.py for src/terpene_vocabulary
cat > src/terpene_vocabulary/__init__.py << 'EOF'
"""
Terpene Visual Vocabulary MCP Server

Deterministic mapping of terpene compounds to visual parameters for image generation.
"""

__version__ = "0.1.0"
EOF

# __init__.py for tests
cat > tests/__init__.py << 'EOF'
"""Tests for terpene-vocabulary-mcp"""
EOF

# tests/unit/__init__.py
cat > tests/unit/__init__.py << 'EOF'
"""Unit tests"""
EOF

# tests/integration/__init__.py
cat > tests/integration/__init__.py << 'EOF'
"""Integration tests"""
EOF

# __main__.py for local testing
cat > src/terpene_vocabulary/__main__.py << 'EOF'
"""
Local execution script for Terpene Vocabulary MCP server.

Usage:
    python -m terpene_vocabulary

This runs the server locally for testing and development.
For production, use FastMCP Cloud deployment.
"""

from .server import mcp

if __name__ == "__main__":
    mcp.run()
EOF

# handler.py for FastMCP Cloud
cat > src/terpene_vocabulary/handler.py << 'EOF'
"""
FastMCP Cloud entry point for Terpene Vocabulary server.

For FastMCP Cloud deployment, the entry point function must RETURN the server object.
The cloud platform handles the event loop and server.run() call.
"""

from .server import mcp

def handler():
    """Entry point for FastMCP Cloud deployment."""
    return mcp
EOF

# pyproject.toml
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "terpene-vocabulary-mcp"
version = "0.1.0"
description = "MCP server for terpene visual vocabulary - deterministic mapping of terpene compounds to visual parameters"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "Dal Marsters", email = "dal@lushy.ai"}
]
license = {text = "MIT"}

dependencies = [
    "fastmcp>=0.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=22.0",
    "ruff>=0.1.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/terpene_vocabulary"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.ruff]
line-length = 100
target-version = "py38"
EOF

# README.md
cat > README.md << 'EOF'
# Terpene Vocabulary MCP Server

A FastMCP server providing deterministic mapping of terpene compounds to visual parameters for image generation.

## Quick Start

### Installation
```bash
pip install -e ".[dev]"
```

### Local Testing
```bash
python -m terpene_vocabulary
```

### Running Tests
```bash
bash tests/run_tests.sh
```

### FastMCP Cloud Deployment
Entry point: `src/terpene_vocabulary/handler.py:handler()`

## Features

- 11 fully-documented terpenes with complete visual vocabularies
- 10 tools for lookup, discovery, comparison, and intensity control
- 4 temporal stages (Fresh, Active, Fading, Traces)
- Master prompts ready for LLM fusion
- Deterministic taxonomy mapping (zero LLM cost)

## Terpenes

1. Limonene - Bright, radial, citrus
2. Pinene - Sharp, geometric, defensive
3. Myrcene - Flowing, organic, earthy
4. Caryophyllene - Complex, sophisticated, spiced
5. Linalool - Ethereal, soft, delicate
6. Terpinolene - Fresh, crisp, sophisticated
7. Humulene - Earthy, grounded, hoppy
8. Ocimene - Delicate, flowing, energetic
9. Sabinene - Warm, spiced, dynamic
10. Geraniol - Romantic, warm, floral
11. Thymol - Structured, medicinal, herbal

## Documentation

- `ARCHITECTURE.md` - System design and deployment
- `docs/examples/` - Usage examples and patterns

## License

MIT
EOF

# ARCHITECTURE.md (truncated reference)
cat > ARCHITECTURE.md << 'EOF'
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
EOF

echo ""
echo "✓ Directory structure created"
echo "✓ Small files generated (.gitignore, __init__.py, __main__.py, handler.py, pyproject.toml, README.md)"
echo ""
echo "Next steps:"
echo "1. Copy server.py to src/terpene_vocabulary/"
echo "2. Add test files to tests/unit/ and tests/integration/"
echo "3. Run: bash verify_structure.sh"
echo "4. Run: pip install -e \".[dev]\""
echo "5. Run: bash tests/run_tests.sh"
