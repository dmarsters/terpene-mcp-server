#!/bin/bash
# Test runner for terpene-vocabulary-mcp server
# Usage: bash tests/run_tests.sh

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Running tests for terpene-vocabulary-mcp..."
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Installing dev dependencies..."
    pip install -e ".[dev]" > /dev/null
fi

# Run tests
echo "Running unit tests..."
pytest tests/unit/ -v --tb=short

echo ""
echo "Running integration tests..."
pytest tests/integration/ -v --tb=short

echo ""
echo "Running test coverage..."
pytest tests/ --cov=src/terpene_vocabulary --cov-report=term-missing

echo ""
echo "✓ All tests passed"
