#!/bin/bash
# Verify terpene-vocabulary-mcp server structure
# Run before manual file additions to establish baseline
# Run after to ensure all required files are present

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

REQUIRED_DIRS=(
    "src/terpene_vocabulary"
    "tests"
    "tests/unit"
    "tests/integration"
    "docs"
    "docs/examples"
)

REQUIRED_AUTO_FILES=(
    ".gitignore"
    "src/terpene_vocabulary/__init__.py"
    "src/terpene_vocabulary/__main__.py"
    "src/terpene_vocabulary/handler.py"
    "tests/__init__.py"
    "tests/unit/__init__.py"
    "tests/integration/__init__.py"
    "pyproject.toml"
    "README.md"
    "ARCHITECTURE.md"
)

REQUIRED_MANUAL_FILES=(
    "src/terpene_vocabulary/server.py"
    "tests/run_tests.sh"
)

echo "Verifying terpene-vocabulary-mcp structure..."
echo ""

# Check directories
echo "Checking directories..."
missing_dirs=0
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ $dir (MISSING)"
        missing_dirs=$((missing_dirs + 1))
    fi
done

echo ""
echo "Checking auto-generated files..."
missing_auto=0
for file in "${REQUIRED_AUTO_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
        missing_auto=$((missing_auto + 1))
    fi
done

echo ""
echo "Checking manual files (required for full functionality)..."
missing_manual=0
for file in "${REQUIRED_MANUAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (NOT YET ADDED)"
        missing_manual=$((missing_manual + 1))
    fi
done

# Summary
echo ""
echo "═══════════════════════════════════════════"
if [ $missing_dirs -eq 0 ] && [ $missing_auto -eq 0 ]; then
    if [ $missing_manual -eq 0 ]; then
        echo "✓ Structure complete and ready for installation"
        echo ""
        echo "Next: pip install -e \".[dev]\""
        exit 0
    else
        echo "✓ Auto-generated structure complete"
        echo "⚠ Missing $missing_manual manual file(s)"
        echo ""
        echo "Next steps:"
        echo "1. Copy server.py to src/terpene_vocabulary/"
        echo "2. Create tests/run_tests.sh"
        echo "3. Run: bash verify_structure.sh (again)"
        exit 0
    fi
else
    if [ $missing_dirs -gt 0 ]; then
        echo "✗ Missing $missing_dirs directory(ies)"
    fi
    if [ $missing_auto -gt 0 ]; then
        echo "✗ Missing $missing_auto auto-generated file(s)"
    fi
    echo ""
    echo "Run: bash create_structure.sh"
    exit 1
fi
