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

## Author
Dal Marsters - Lushy.app
