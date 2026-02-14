"""
Terpene Visual Vocabulary MCP Server
Version 2.0.0-phase2.7+tier4d

Deterministic mapping of terpene compounds to visual parameters for image generation.
This server handles all taxonomy lookups and parameter mapping - no LLM tokens required.

The server provides:
- Terpene metadata (smell profiles, visual character, color palettes)
- Temporal stage modifiers (Fresh, Active, Fading, Traces)
- Master prompts (complete terpene descriptors)
- Intensity parameter handling
- Multi-terpene composition rules

Phase 2.6 Enhancements:
- 5D normalized morphospace (11 canonical terpene states)
- 5 rhythmic presets with periods [16, 18, 20, 22, 24]
- Custom oscillation between arbitrary terpene states
- Smooth trajectory computation in parameter space

Phase 2.7 Enhancements:
- 5 visual types with keywords and optical properties
- 7 attractor presets (Tier 1-3 discovered/curated)
- Composite, split-view, and sequence prompt generation
- Domain registry integration for Tier 4D composition

Architecture:
  Layer 1: Pure taxonomy lookup — 0 tokens
  Layer 2: Deterministic computation (distance, trajectory, vocabulary) — 0 tokens
  Layer 3: Claude-assisted synthesis context — ~100-200 tokens
"""

from fastmcp import FastMCP
from typing import Optional, Literal, List, Tuple, Dict, Any
import json
import re

mcp = FastMCP("terpene-vocabulary")

# ============================================================================
# TERPENE DATABASE
# ============================================================================

TERPENES = {
    "limonene": {
        "name": "Limonene",
        "molecular_formula": "C₁₀H₁₆",
        "classification": "Monocyclic monoterpene",
        "scent_profile": "Bright, citrus, sharp, zesty, fresh, sweet-tart",
        "visual_character": "Crisp, radial, high-luminosity",
        "primary_colors": ["Saturated yellow", "Orange", "Bright white"],
        "color_specs": {
            "primary_palette": "Saturated yellows (60%), oranges (25%), whites/highlights (15%)",
            "saturation": "High (75-95%)",
            "luminosity": "Very bright (80-90%)",
            "boundaries": "Crisp transitions",
            "secondary_accents": "White highlights, pale lemon",
            "color_quality": "Transparent, translucent quality"
        },
        "composition": "Concentric spirals, radial symmetry, angular forms",
        "temporal_qualities": {
            "volatility": "Highly volatile",
            "persistence": "Rapid dissipation",
            "stages": {
                "fresh": {
                    "duration": "0-2 hours",
                    "description": "Sharp edges, maximal saturation, crisp geometry, intense highlights",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Crisp"
                },
                "active": {
                    "duration": "2-6 hours",
                    "description": "Slight softening at boundaries, saturation fading marginally",
                    "saturation_adjustment": 0.85,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Mostly crisp"
                },
                "fading": {
                    "duration": "6-12 hours",
                    "description": "Edges blur significantly, saturation drops to 40-60%, highlights diffuse",
                    "saturation_adjustment": 0.5,
                    "luminosity_adjustment": 0.85,
                    "edge_quality": "Soft"
                },
                "traces": {
                    "duration": "12+ hours",
                    "description": "Ghost impressions, pale yellows, very soft edges",
                    "saturation_adjustment": 0.2,
                    "luminosity_adjustment": 0.7,
                    "edge_quality": "Very soft"
                }
            }
        },
        "master_prompt": "Limonene generates crisp, radially symmetrical compositions in saturated yellows and oranges with bright white highlights. Concentric spirals emanate from a luminous center, suggesting broadcast signals of ripeness and attraction. The geometry is clean and angular—pointed edges catch sharp light. Colors transition acidically from warm yellow-orange cores to paler lemon tones at boundaries. High luminosity throughout, with minimal shadow depth. The composition captures volatility through crisp definition gradually softening at margins, as if the bright aromatic signal is dispersing into air, leaving fading citrus-colored traces.",
        "chemical_communication": "Signals ripeness and food sources to insects; broadcast/attractant quality",
        "fusion_strength": "Strong - works well with concepts involving visibility, broadcasting, energy",
        "semantic_bridges": ["radial presence", "broadcasting", "visibility", "bright presence", "citrus warmth"]
    },
    
    "pinene": {
        "name": "Pinene",
        "molecular_formula": "C₁₀H₁₆",
        "classification": "Bicyclic monoterpene",
        "scent_profile": "Woody, sharp, fresh-resinous, piney, slightly medicinal, clean",
        "visual_character": "Sharp, geometric, defensive, crystalline",
        "primary_colors": ["Deep green", "Amber", "Cool white"],
        "color_specs": {
            "primary_palette": "Deep greens (50%), amber/brown (30%), cool whites (20%)",
            "saturation": "Medium-high (65-80%)",
            "luminosity": "Medium (50-70%)",
            "boundaries": "Sharper than earthy terpenes",
            "secondary_accents": "Cool gray-whites, forest-deep greens",
            "color_quality": "Translucent, amber-like clarity"
        },
        "composition": "Interlocking planes, angular forms, needle-like protrusions, layered depth",
        "temporal_qualities": {
            "volatility": "Moderately volatile",
            "persistence": "More stable than limonene",
            "stages": {
                "fresh": {
                    "duration": "0-4 hours",
                    "description": "Sharp needle-like edges, deep green saturation, crisp amber highlights",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Sharp"
                },
                "active": {
                    "duration": "4-12 hours",
                    "description": "Slight dulling, amber becoming opaque",
                    "saturation_adjustment": 0.8,
                    "luminosity_adjustment": 0.9,
                    "edge_quality": "Mostly sharp"
                },
                "fading": {
                    "duration": "12-24 hours",
                    "description": "Geometric sharpness softens, colors muting and becoming earthy",
                    "saturation_adjustment": 0.5,
                    "luminosity_adjustment": 0.75,
                    "edge_quality": "Soft"
                },
                "traces": {
                    "duration": "24+ hours",
                    "description": "Pale greens and warm browns remain, edges very soft",
                    "saturation_adjustment": 0.25,
                    "luminosity_adjustment": 0.6,
                    "edge_quality": "Very soft"
                }
            }
        },
        "master_prompt": "Pinene generates complex, interlocking geometric compositions in deep greens and warm ambers. Bicyclic molecular structure translates to tightly-locked angular forms suggesting both structural rigidity and defensive positioning. Needle-like protrusions catch sharp, cool light while creating layered shadow depth. Saturation is medium-high but cooler in tone than limonene. The composition reads as crystalline and precise—resinous amber captured within geometric boundaries. Sharp edges and crisp intersections gradually soften over time, with bright amber highlights becoming warmer and deeper greens mellowing into earthy forest tones as the volatile pinene disperses.",
        "chemical_communication": "Signals plant defense and territorial marking; defensive/protective quality",
        "fusion_strength": "Strong - works well with concepts involving precision, defense, complexity, structure",
        "semantic_bridges": ["defensive geometry", "crystalline precision", "territorial marking", "rigidity", "woody depth"]
    },
    
    "myrcene": {
        "name": "Myrcene",
        "molecular_formula": "C₁₀H₁₆",
        "classification": "Acyclic monoterpene",
        "scent_profile": "Earthy, musky, herbal, spicy, clove-like, slightly fruity, warm",
        "visual_character": "Flowing, organic, earthy, distributed",
        "primary_colors": ["Warm brown", "Ochre", "Deep green"],
        "color_specs": {
            "primary_palette": "Warm browns (40%), ochres/earth tones (35%), deep greens (20%), golden accents (5%)",
            "saturation": "Medium-low (50-65%)",
            "luminosity": "Lower (35-50%)",
            "boundaries": "Soft, blurred transitions",
            "secondary_accents": "Clove-warm spice tones, muted olive greens",
            "color_quality": "Opaque, earthy, matte quality"
        },
        "composition": "Flowing ribbons, directional movement, organic shapes, non-geometric",
        "temporal_qualities": {
            "volatility": "Moderately volatile",
            "persistence": "Slightly more stable than monoterpenes",
            "stages": {
                "fresh": {
                    "duration": "0-6 hours",
                    "description": "Richest color saturation, slight green freshness visible",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Soft but defined"
                },
                "active": {
                    "duration": "6-12 hours",
                    "description": "Green tones fade, browns become dominant",
                    "saturation_adjustment": 0.75,
                    "luminosity_adjustment": 0.85,
                    "edge_quality": "Soft"
                },
                "fading": {
                    "duration": "12-24 hours",
                    "description": "Color becomes muddier, warm tones persist",
                    "saturation_adjustment": 0.45,
                    "luminosity_adjustment": 0.7,
                    "edge_quality": "Very soft"
                },
                "traces": {
                    "duration": "24+ hours",
                    "description": "Muted earth tones remain, very soft focus",
                    "saturation_adjustment": 0.2,
                    "luminosity_adjustment": 0.5,
                    "edge_quality": "Very soft"
                }
            }
        },
        "master_prompt": "Myrcene generates flowing, organic compositions dominated by warm earths, ochres, and muted greens. The linear molecular structure translates to ribbon-like forms moving through space with clear directional vectors, undulating and flexible rather than rigid. Saturation is deliberately lower and luminosity muted, creating a grounded, earthy aesthetic. Boundaries between color zones are soft and blurred, as if the composition is diffusing its presence throughout the surrounding space like distributed herbal signals. No sharp highlights or crisp edges—instead, everything has matte, warm, musky quality. Over time, green freshness fades while warm earth tones persist, eventually becoming indistinct traces of ochre and brown.",
        "chemical_communication": "Signals plant maturity and growth; distributed/expansive quality",
        "fusion_strength": "Strong - works well with organic subjects, landscapes, movement, growth",
        "semantic_bridges": ["flowing movement", "earthy grounding", "organic growth", "distributed presence", "natural unfolding"]
    },
    
    "caryophyllene": {
        "name": "Caryophyllene",
        "molecular_formula": "C₁₅H₂₄",
        "classification": "Bicyclic sesquiterpene",
        "scent_profile": "Spicy, peppery, woody, warm, slightly sweet, clove-like, complex, sophisticated",
        "visual_character": "Layered, complex, deep, warm-spiced",
        "primary_colors": ["Deep burgundy", "Rich brown", "Warm amber"],
        "color_specs": {
            "primary_palette": "Deep warm browns (35%), rich reds/burgundy (25%), amber (20%), dark earth tones (20%)",
            "saturation": "Medium (60-75%)",
            "luminosity": "Medium-low (45-60%)",
            "boundaries": "Some crisp, mostly soft",
            "secondary_accents": "Deep burgundy highlights, warm copper tones",
            "color_quality": "Rich, sophisticated, translucent amber"
        },
        "composition": "Interlocking forms, layered depth, complex structural relationships",
        "temporal_qualities": {
            "volatility": "Low volatility - sesquiterpene",
            "persistence": "Persists much longer than monoterpenes",
            "stages": {
                "fresh": {
                    "duration": "0-12 hours",
                    "description": "Rich saturation, deep burgundy prominent, warmest amber highlights",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Defined"
                },
                "active": {
                    "duration": "12-48 hours",
                    "description": "Saturation holds, colors remain sophisticated and deep",
                    "saturation_adjustment": 0.9,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Defined"
                },
                "fading": {
                    "duration": "48-72 hours",
                    "description": "Gradual dulling, warm tones becoming more uniform",
                    "saturation_adjustment": 0.65,
                    "luminosity_adjustment": 0.8,
                    "edge_quality": "Soft"
                },
                "traces": {
                    "duration": "72+ hours",
                    "description": "Deep browns remain, complexity fades",
                    "saturation_adjustment": 0.35,
                    "luminosity_adjustment": 0.6,
                    "edge_quality": "Soft"
                }
            }
        },
        "master_prompt": "Caryophyllene generates sophisticated, densely-layered compositions in deep burgundy, rich browns, warm amber, and dark earth tones. The bicyclic sesquiterpene structure creates interlocking forms more complex than smaller terpenes, suggesting both resilience and sophisticated molecular communication. Saturation is medium and warmth permeates throughout—no cool tones. Luminosity is deliberately held lower, creating visual weight and substance. The composition reads as layered complexity, with burgundy and amber creating depth within warm darkness. Unlike volatile monoterpenes, caryophyllene's persistence translates to long-lasting visual richness—colors and complexity maintain their depth over time before gradually simplifying into muted warm earth tones.",
        "chemical_communication": "Signals plant defense and stress response; complex ecological communication",
        "fusion_strength": "Strong - works well with sophisticated subjects, emotional depth, complexity",
        "semantic_bridges": ["sophisticated depth", "warm presence", "complex resilience", "spiced warmth", "layered intelligence"]
    },
    
    "linalool": {
        "name": "Linalool",
        "molecular_formula": "C₁₀H₁₈O",
        "classification": "Acyclic monoterpene alcohol",
        "scent_profile": "Floral, lavender, sweet, fresh, slightly fruity, delicate, soft, calming",
        "visual_character": "Ethereal, soft, luminous, delicate",
        "primary_colors": ["Soft purple", "Pale violet", "Luminous white"],
        "color_specs": {
            "primary_palette": "Soft purples/lavenders (40%), pale violets (20%), soft whites/cream (25%), pale pinks (15%)",
            "saturation": "Low-medium (50-65%)",
            "luminosity": "Very high (75-90%)",
            "boundaries": "Extremely soft, watercolor-like",
            "secondary_accents": "Pale lilac, cream highlights, soft mauve",
            "color_quality": "Translucent, ethereal, delicate"
        },
        "composition": "Flowing forms, graceful geometry, delicate structures",
        "temporal_qualities": {
            "volatility": "Moderately volatile",
            "persistence": "Less dramatic than some terpenes",
            "stages": {
                "fresh": {
                    "duration": "0-4 hours",
                    "description": "Richest purple saturation, brightest highlights, most luminous",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Very soft"
                },
                "active": {
                    "duration": "4-12 hours",
                    "description": "Slight warming in tone, purples becoming more mauve",
                    "saturation_adjustment": 0.8,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Very soft"
                },
                "fading": {
                    "duration": "12-24 hours",
                    "description": "Purples fading to pale lavenders, whites, losing saturation",
                    "saturation_adjustment": 0.45,
                    "luminosity_adjustment": 0.85,
                    "edge_quality": "Very soft"
                },
                "traces": {
                    "duration": "24+ hours",
                    "description": "Pale creams and ghostly lavender washes",
                    "saturation_adjustment": 0.15,
                    "luminosity_adjustment": 0.75,
                    "edge_quality": "Very soft"
                }
            }
        },
        "master_prompt": "Linalool generates ethereal, luminous compositions in soft lavenders, pale violets, and creamy whites. The acyclic structure translates to graceful, flowing forms—more delicate than other terpenes due to the hydroxyl functional group adding translucence. Saturation is deliberately kept low (50-65%) while luminosity remains very high (75-90%), creating an airy, almost watercolor-like aesthetic. Boundaries are extremely soft and blurred, suggesting delicate dissolution into surrounding space. The palette maintains cool tones but reads as warm and inviting through ethereal quality. Forms appear graceful and gently communicative rather than signaling forcefully. Linalool's moderate volatility means the composition gradually transitions from rich lavender luminescence to pale ghostly traces, fading delicately over extended time.",
        "chemical_communication": "Signals attraction and gentle communication; calming/peaceful quality",
        "fusion_strength": "Strong - works well with delicate subjects, romantic concepts, spiritual themes",
        "semantic_bridges": ["ethereal presence", "graceful communication", "floral softness", "calming luminescence", "delicate transcendence"]
    },
    
    "terpinolene": {
        "name": "Terpinolene",
        "molecular_formula": "C₁₀H₁₆",
        "classification": "Bicyclic monoterpene with exocyclic double bond",
        "scent_profile": "Fresh, herbal, woody, piney, slightly fruity, complex, crisp, sophisticated",
        "visual_character": "Fresh, complex, crisp, sophisticated",
        "primary_colors": ["Fresh green", "Crisp white", "Soft earth"],
        "color_specs": {
            "primary_palette": "Fresh greens (35%), crisp whites/highlights (25%), soft earths (20%), cool grays (15%), pale yellows (5%)",
            "saturation": "Medium (65-75%)",
            "luminosity": "High (70-85%)",
            "boundaries": "Mixed - some crisp, some soft",
            "secondary_accents": "Pale sage, cool gray-greens, soft golden",
            "color_quality": "Translucent in some zones, opaque in others"
        },
        "composition": "Complex geometric forms with outward-reaching elements, balanced structure and motion",
        "temporal_qualities": {
            "volatility": "Volatile",
            "persistence": "Dissipates relatively quickly",
            "stages": {
                "fresh": {
                    "duration": "0-3 hours",
                    "description": "Brightest greens, sharpest highlights, most complex saturation",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Mixed crisp/soft"
                },
                "active": {
                    "duration": "3-9 hours",
                    "description": "Slight softening, green intensity maintaining",
                    "saturation_adjustment": 0.85,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Mostly soft"
                },
                "fading": {
                    "duration": "9-18 hours",
                    "description": "Greens muting, sophistication fading to simpler herbal",
                    "saturation_adjustment": 0.55,
                    "luminosity_adjustment": 0.8,
                    "edge_quality": "Soft"
                },
                "traces": {
                    "duration": "18+ hours",
                    "description": "Pale greens and soft grays remain",
                    "saturation_adjustment": 0.25,
                    "luminosity_adjustment": 0.65,
                    "edge_quality": "Very soft"
                }
            }
        },
        "master_prompt": "Terpinolene generates sophisticated fresh compositions with complex geometric layering in vibrant greens, crisp whites, earthy undertones, and cool grays. The unusual bicyclic structure with exocyclic double bond creates visual tension between internal geometric stability and outward-reaching motion. Saturation is medium-high with high luminosity, creating crisp, airy aesthetic distinct from other fresh terpenes. The composition reads as sophisticated freshness—not simple brightness, but rather complex herbal clarity with geometric precision. Boundaries are deliberately mixed: some areas crisp and defined, others softer, reflecting structural complexity. Terpinolene's volatility means the composition gradually transitions from complex geometric freshness to muted herbal tones over roughly 18 hours, with bright greens fading first.",
        "chemical_communication": "Signals plant vitality and complex ecological information; sophisticated presence",
        "fusion_strength": "Medium-strong - works well with intellectual/sophisticated concepts",
        "semantic_bridges": ["sophisticated freshness", "complex clarity", "herbal precision", "outward expansion", "geometric grace"]
    },
    
    "humulene": {
        "name": "Humulene",
        "molecular_formula": "C₁₅H₂₄",
        "classification": "Bicyclic sesquiterpene (isomer of caryophyllene)",
        "scent_profile": "Hoppy, woody, earthy, spicy, herbal, complex, slightly sweet",
        "visual_character": "Earthy, warm, grounded, hoppy-golden",
        "primary_colors": ["Rich brown", "Golden-amber", "Earth tones"],
        "color_specs": {
            "primary_palette": "Rich browns (35%), golden-amber (25%), deep earth (20%), subtle greens (10%), warm accents (10%)",
            "saturation": "Medium (65-75%)",
            "luminosity": "Medium (50-65%)",
            "boundaries": "Soft-to-medium transitions",
            "secondary_accents": "Hoppy gold, muted sage, warm copper",
            "color_quality": "Warm, substantial, golden translucence"
        },
        "composition": "Complex interlocking forms, earthy grounding, natural flow",
        "temporal_qualities": {
            "volatility": "Low volatility - sesquiterpene",
            "persistence": "Long-lasting like caryophyllene",
            "stages": {
                "fresh": {
                    "duration": "0-12 hours",
                    "description": "Rich golden-brown saturation, warmest amber highlights",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Soft-defined"
                },
                "active": {
                    "duration": "12-48 hours",
                    "description": "Saturation holding steady, complexity visible",
                    "saturation_adjustment": 0.88,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Soft-defined"
                },
                "fading": {
                    "duration": "48-72 hours",
                    "description": "Cooling from gold to neutral brown",
                    "saturation_adjustment": 0.65,
                    "luminosity_adjustment": 0.8,
                    "edge_quality": "Soft"
                },
                "traces": {
                    "duration": "72+ hours",
                    "description": "Deep muted browns remain",
                    "saturation_adjustment": 0.35,
                    "luminosity_adjustment": 0.6,
                    "edge_quality": "Soft"
                }
            }
        },
        "master_prompt": "Humulene generates complex, earthy compositions in golden-browns, warm earth tones, subtle herbal greens, and amber highlights. As a sesquiterpene isomer of caryophyllene, humulene shares similar structural complexity and visual density, but reads distinctly more earthy and hoppy-golden rather than deeply burgundy and spiced. Saturation is medium with medium luminosity, creating substantial aesthetic. Boundaries are softer than caryophyllene, reflecting humulene's slightly different spatial configuration. The palette maintains warm golden undertones throughout. Composition suggests herbal grounding and transformation (fermentation) rather than deep mystery. Like other sesquiterpenes, humulene persists significantly longer than monoterpenes, maintaining warm golden-brown complexity over 48+ hours before gradually transitioning to simpler muted earth tones.",
        "chemical_communication": "Signals hop plant presence and fermentation; grounding/transformation quality",
        "fusion_strength": "Strong - works well with earthy, grounded, natural subjects",
        "semantic_bridges": ["hoppy warmth", "earthy grounding", "fermentation transformation", "herbal complexity", "golden presence"]
    },
    
    "ocimene": {
        "name": "Ocimene",
        "molecular_formula": "C₁₀H₁₆",
        "classification": "Acyclic monoterpene",
        "scent_profile": "Floral, sweet, herbal, fruity, slightly spicy, fresh, delicate",
        "visual_character": "Delicate, flowing, pastel, energetic",
        "primary_colors": ["Pale pink", "Soft green", "Creamy white"],
        "color_specs": {
            "primary_palette": "Soft pastels—pale pinks (25%), soft greens (25%), creamy whites (25%), pale yellows (15%), soft lavenders (10%)",
            "saturation": "Low (45-60%)",
            "luminosity": "High (75-90%)",
            "boundaries": "Soft, watercolor-like",
            "secondary_accents": "Pale sage, soft apricot, cream",
            "color_quality": "Translucent, delicate, luminous"
        },
        "composition": "Flowing graceful forms with subtle energetic quality, delicate but dynamic",
        "temporal_qualities": {
            "volatility": "Highly volatile",
            "persistence": "Quick dissipation",
            "stages": {
                "fresh": {
                    "duration": "0-4 hours",
                    "description": "Richest pastel saturation, brightest highlights, most color",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Soft"
                },
                "active": {
                    "duration": "4-10 hours",
                    "description": "Slight softening, delicate quality increasing",
                    "saturation_adjustment": 0.75,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Soft"
                },
                "fading": {
                    "duration": "10-20 hours",
                    "description": "Pastels becoming pale and washed out",
                    "saturation_adjustment": 0.35,
                    "luminosity_adjustment": 0.85,
                    "edge_quality": "Very soft"
                },
                "traces": {
                    "duration": "20+ hours",
                    "description": "Ghost-like pale washes",
                    "saturation_adjustment": 0.1,
                    "luminosity_adjustment": 0.75,
                    "edge_quality": "Very soft"
                }
            }
        },
        "master_prompt": "Ocimene generates delicate, luminous compositions in soft pastels (pale pinks, soft greens, creams, pale yellows, soft lavenders). The acyclic structure with extended conjugation creates flowing, graceful forms suggesting subtle energetic quality—not rigid, but gently dynamic. Saturation is deliberately kept low (45-60%) while luminosity remains very high (75-90%), creating ethereal aesthetic. Boundaries are extremely soft and watercolor-like. The composition reads as delicate and communicative rather than forceful, with graceful motion throughout. Like other volatile monoterpenes, ocimene's brightness rapidly fades over 10-20 hours, with rich pastels transitioning through pale washes to ghost-like traces before dissipating.",
        "chemical_communication": "Signals plant attraction and nuanced communication; graceful/energetic quality",
        "fusion_strength": "Medium-strong - works well with delicate, dynamic, artistic concepts",
        "semantic_bridges": ["graceful motion", "delicate energy", "subtle communication", "pastoral softness", "energetic flow"]
    },
    
    "sabinene": {
        "name": "Sabinene",
        "molecular_formula": "C₁₀H₁₆",
        "classification": "Bicyclic monoterpene with exocyclic double bond",
        "scent_profile": "Spicy, peppery, warm, woody, slightly bitter, herbal, sharp",
        "visual_character": "Warm, spiced, sharp, dynamic",
        "primary_colors": ["Warm brown", "Spice red", "Golden tone"],
        "color_specs": {
            "primary_palette": "Warm browns (30%), spice reds (25%), golden tones (20%), dark earth (15%), warm highlights (10%)",
            "saturation": "Medium-high (70-80%)",
            "luminosity": "Medium (55-70%)",
            "boundaries": "Mixed - dynamic quality",
            "secondary_accents": "Peppery red, golden amber, warm copper",
            "color_quality": "Warm, spiced, translucent amber"
        },
        "composition": "Warm geometric forms with outward-reaching quality, dynamic structural tension",
        "temporal_qualities": {
            "volatility": "Moderately volatile",
            "persistence": "Slower dissipation than limonene",
            "stages": {
                "fresh": {
                    "duration": "0-5 hours",
                    "description": "Richest red and golden saturation, sharpest contrasts",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Sharp"
                },
                "active": {
                    "duration": "5-12 hours",
                    "description": "Saturation holding, warmth persisting",
                    "saturation_adjustment": 0.82,
                    "luminosity_adjustment": 0.92,
                    "edge_quality": "Mostly sharp"
                },
                "fading": {
                    "duration": "12-24 hours",
                    "description": "Reds fading to browns, highlights duller",
                    "saturation_adjustment": 0.5,
                    "luminosity_adjustment": 0.75,
                    "edge_quality": "Mixed"
                },
                "traces": {
                    "duration": "24+ hours",
                    "description": "Warm browns remain, peppery character gone",
                    "saturation_adjustment": 0.25,
                    "luminosity_adjustment": 0.6,
                    "edge_quality": "Soft"
                }
            }
        },
        "master_prompt": "Sabinene generates warm, dynamically-structured compositions in spice reds, golden tones, warm browns, and rich earth tones. The bicyclic structure with exocyclic double bond creates visual tension between contained structure and outward-reaching energy. Saturation is medium-high with medium luminosity, creating substantial warm aesthetic. Boundaries are deliberately mixed—some areas crisp and sharp, others soft—reflecting dynamic structural complexity. The palette maintains active warmth throughout, suggesting pepper and spice presence. Composition reads as containing active heat rather than passive grounding. Moderately volatile nature means rich red and golden saturation gradually transitions to warmer, duller browns over 12-24 hours, with peppery sharpness fading but warm undertones persisting longer.",
        "chemical_communication": "Signals spice plant presence and peppery defense; warming/dynamic quality",
        "fusion_strength": "Strong - works well with warm, active, spiced concepts",
        "semantic_bridges": ["active warmth", "peppery presence", "dynamic heat", "spiced complexity", "warm sharpness"]
    },
    
    "geraniol": {
        "name": "Geraniol",
        "molecular_formula": "C₁₀H₁₈O",
        "classification": "Acyclic monoterpene alcohol",
        "scent_profile": "Floral, rose-like, sweet, slightly fruity, fresh, delicate, sophisticated",
        "visual_character": "Romantic, warm, ethereal, sophisticated",
        "primary_colors": ["Soft rose pink", "Warm cream", "Pale peach"],
        "color_specs": {
            "primary_palette": "Soft rose pinks (35%), warm creams (25%), pale peachy tones (20%), soft lavenders (15%), white highlights (5%)",
            "saturation": "Low-medium (55-70%)",
            "luminosity": "High (75-90%)",
            "boundaries": "Soft romantic transitions",
            "secondary_accents": "Pale rose-mauve, warm peach, soft cream",
            "color_quality": "Translucent, warm, delicate"
        },
        "composition": "Flowing graceful forms with warm presence, romantic aesthetic",
        "temporal_qualities": {
            "volatility": "Moderately volatile",
            "persistence": "Persists slightly longer than some monoterpenes",
            "stages": {
                "fresh": {
                    "duration": "0-6 hours",
                    "description": "Richest rose-pink saturation, warmest peachy tones",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Soft"
                },
                "active": {
                    "duration": "6-12 hours",
                    "description": "Saturation holding, rose character remaining",
                    "saturation_adjustment": 0.85,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Soft"
                },
                "fading": {
                    "duration": "12-24 hours",
                    "description": "Pinks becoming paler and more mauve-like",
                    "saturation_adjustment": 0.5,
                    "luminosity_adjustment": 0.85,
                    "edge_quality": "Soft"
                },
                "traces": {
                    "duration": "24+ hours",
                    "description": "Pale lavender-creams remain",
                    "saturation_adjustment": 0.2,
                    "luminosity_adjustment": 0.75,
                    "edge_quality": "Very soft"
                }
            }
        },
        "master_prompt": "Geraniol generates sophisticated, romantic compositions in soft rose pinks, warm creams, pale peach tones, and soft lavenders. The acyclic alcohol structure (like linalool) creates graceful, flowing forms, but geraniol reads warmer and more romantic than linalool's cool lavender. Saturation is low-medium with high luminosity, creating ethereal airy aesthetic. The composition maintains translucence throughout—forms appear delicate and attractive rather than substantial. Boundaries are soft and romantic, suggesting gentle transitions and blooming quality. Color palette emphasizes warmth within delicate framework. Moderate volatility means rich rose-pink saturation and peachy warmth persist slightly longer than some monoterpenes, gradually fading to pale lavender-creams over 12-24 hours.",
        "chemical_communication": "Signals flower attraction and romantic appeal; inviting/beautiful quality",
        "fusion_strength": "Strong - works well with romantic, delicate, warm concepts",
        "semantic_bridges": ["romantic presence", "floral beauty", "warm delicacy", "graceful attraction", "blooming quality"]
    },
    
    "thymol": {
        "name": "Thymol",
        "molecular_formula": "C₁₀H₁₄O",
        "classification": "Monoterpene phenol",
        "scent_profile": "Herbal, thyme-like, warm, slightly spicy, medicinal, antiseptic, complex, intense",
        "visual_character": "Structured, medicinal, herbal-sophisticated, potent",
        "primary_colors": ["Complex green", "Warm brown", "Golden-amber"],
        "color_specs": {
            "primary_palette": "Complex greens (35%), warm browns (30%), golden-amber (20%), earth tones (15%)",
            "saturation": "Medium-high (70-80%)",
            "luminosity": "Medium (55-70%)",
            "boundaries": "Medium sharpness - defined but not crystalline",
            "secondary_accents": "Warm sage, medicinal copper, deep bronze",
            "color_quality": "Warm, complex, translucent amber"
        },
        "composition": "Structured geometric forms, herbal complexity with medicinal precision",
        "temporal_qualities": {
            "volatility": "Lower volatility - phenolic compound",
            "persistence": "Moderate persistence",
            "stages": {
                "fresh": {
                    "duration": "0-8 hours",
                    "description": "Richest green and golden saturation, sharpest definition",
                    "saturation_adjustment": 1.0,
                    "luminosity_adjustment": 1.0,
                    "edge_quality": "Defined"
                },
                "active": {
                    "duration": "8-24 hours",
                    "description": "Saturation holding, complexity visible",
                    "saturation_adjustment": 0.85,
                    "luminosity_adjustment": 0.95,
                    "edge_quality": "Defined"
                },
                "fading": {
                    "duration": "24-48 hours",
                    "description": "Greens muting, golden tones warming and dulling",
                    "saturation_adjustment": 0.55,
                    "luminosity_adjustment": 0.8,
                    "edge_quality": "Soft"
                },
                "traces": {
                    "duration": "48+ hours",
                    "description": "Warm browns, herbal character faded",
                    "saturation_adjustment": 0.3,
                    "luminosity_adjustment": 0.65,
                    "edge_quality": "Soft"
                }
            }
        },
        "master_prompt": "Thymol generates structured, sophisticated compositions in complex greens, warm browns, golden-ambers, and earth tones. The phenolic aromatic ring structure creates geometric precision and structural rigidity absent in typical terpenes. Saturation is medium-high with medium luminosity, creating substantial warm aesthetic with significant visual weight. Boundaries are defined—sharp enough to suggest medicinal clarity, but not crystalline. The composition reads as intentionally potent and historically significant rather than organically growing. Warm undertones persist throughout. Unlike more volatile monoterpenes, thymol's lower volatility means the composition maintains its rich complex saturation and medicinal character over 24+ hours, gradually warming and simplifying to muted earth tones over extended duration.",
        "chemical_communication": "Signals antimicrobial presence and medicinal potency; structured/potent quality",
        "fusion_strength": "Medium-strong - works well with intellectual, medicinal, historical concepts",
        "semantic_bridges": ["medicinal potency", "structured wisdom", "herbal sophistication", "warming clarity", "intentional presence"]
    }
}

# ============================================================================
# TOOLS
# ============================================================================

@mcp.tool()
def list_terpenes() -> str:
    """List all available terpenes with basic metadata."""
    result = []
    for terpene_id, terpene_data in TERPENES.items():
        result.append({
            "id": terpene_id,
            "name": terpene_data["name"],
            "formula": terpene_data["molecular_formula"],
            "scent": terpene_data["scent_profile"],
            "visual_character": terpene_data["visual_character"]
        })
    return json.dumps(result, indent=2)

@mcp.tool()
def get_terpene(terpene_name: str) -> str:
    """Get complete metadata for a specific terpene."""
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENES:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found"})
    return json.dumps(TERPENES[terpene_id], indent=2)

@mcp.tool()
def get_master_prompt(terpene_name: str, temporal_stage: Optional[Literal["fresh", "active", "fading", "traces"]] = "fresh") -> str:
    """Get the master prompt for a terpene, optionally modified for temporal stage."""
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENES:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found"})
    
    terpene = TERPENES[terpene_id]
    master = terpene["master_prompt"]
    
    # Apply temporal stage adjustments to description
    if temporal_stage != "fresh" and temporal_stage in terpene["temporal_qualities"]["stages"]:
        stage_data = terpene["temporal_qualities"]["stages"][temporal_stage]
        temporal_note = f"\n\n[{temporal_stage.upper()} STAGE: {stage_data['description']}]"
        return json.dumps({
            "terpene": terpene["name"],
            "temporal_stage": temporal_stage,
            "master_prompt": master + temporal_note,
            "stage_adjustments": stage_data
        }, indent=2)
    
    return json.dumps({
        "terpene": terpene["name"],
        "temporal_stage": temporal_stage,
        "master_prompt": master,
        "stage_adjustments": terpene["temporal_qualities"]["stages"]["fresh"]
    }, indent=2)

@mcp.tool()
def get_color_palette(terpene_name: str, temporal_stage: Optional[Literal["fresh", "active", "fading", "traces"]] = "fresh") -> str:
    """Get color palette specifications for a terpene, adjusted for temporal stage."""
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENES:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found"})
    
    terpene = TERPENES[terpene_id]
    palette = terpene["color_specs"].copy()
    
    # Apply temporal adjustments
    if temporal_stage in terpene["temporal_qualities"]["stages"]:
        stage_data = terpene["temporal_qualities"]["stages"][temporal_stage]
        palette["temporal_adjustments"] = {
            "saturation_multiplier": stage_data["saturation_adjustment"],
            "luminosity_multiplier": stage_data["luminosity_adjustment"],
            "edge_quality": stage_data["edge_quality"],
            "stage_description": stage_data["description"]
        }
    
    return json.dumps({
        "terpene": terpene["name"],
        "temporal_stage": temporal_stage,
        "color_specs": palette
    }, indent=2)

@mcp.tool()
def get_temporal_stages(terpene_name: str) -> str:
    """Get all temporal stages and their characteristics for a terpene."""
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENES:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found"})
    
    terpene = TERPENES[terpene_id]
    temporal = terpene["temporal_qualities"]
    
    result = {
        "terpene": terpene["name"],
        "volatility": temporal["volatility"],
        "persistence": temporal["persistence"],
        "stages": temporal["stages"]
    }
    
    return json.dumps(result, indent=2)

@mcp.tool()
def get_composition_rules(terpene_name: str) -> str:
    """Get compositional and structural rules for a terpene."""
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENES:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found"})
    
    terpene = TERPENES[terpene_id]
    
    return json.dumps({
        "terpene": terpene["name"],
        "molecular_structure": terpene["classification"],
        "formula": terpene["molecular_formula"],
        "composition": terpene["composition"],
        "semantic_bridges": terpene["semantic_bridges"],
        "fusion_strength": terpene["fusion_strength"]
    }, indent=2)

@mcp.tool()
def compare_terpenes(terpene1_name: str, terpene2_name: str) -> str:
    """Compare two terpenes across visual and olfactory dimensions."""
    t1_id = terpene1_name.lower().strip()
    t2_id = terpene2_name.lower().strip()
    
    if t1_id not in TERPENES or t2_id not in TERPENES:
        return json.dumps({"error": "One or both terpenes not found"})
    
    t1 = TERPENES[t1_id]
    t2 = TERPENES[t2_id]
    
    comparison = {
        "terpene1": t1["name"],
        "terpene2": t2["name"],
        "comparison": {
            "scent_profiles": {
                "terpene1": t1["scent_profile"],
                "terpene2": t2["scent_profile"]
            },
            "visual_character": {
                "terpene1": t1["visual_character"],
                "terpene2": t2["visual_character"]
            },
            "primary_colors": {
                "terpene1": t1["primary_colors"],
                "terpene2": t2["primary_colors"]
            },
            "saturation_range": {
                "terpene1": t1["color_specs"]["saturation"],
                "terpene2": t2["color_specs"]["saturation"]
            },
            "luminosity_range": {
                "terpene1": t1["color_specs"]["luminosity"],
                "terpene2": t2["color_specs"]["luminosity"]
            },
            "volatility": {
                "terpene1": t1["temporal_qualities"]["volatility"],
                "terpene2": t2["temporal_qualities"]["volatility"]
            },
            "composition_style": {
                "terpene1": t1["composition"],
                "terpene2": t2["composition"]
            }
        }
    }
    
    return json.dumps(comparison, indent=2)

@mcp.tool()
def get_chemical_communication(terpene_name: str) -> str:
    """Get the chemical communication/biological signaling aspect of a terpene."""
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENES:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found"})
    
    terpene = TERPENES[terpene_id]
    
    return json.dumps({
        "terpene": terpene["name"],
        "chemical_communication": terpene["chemical_communication"],
        "biological_role": terpene["scent_profile"],
        "visual_interpretation": terpene["master_prompt"][:200] + "..."
    }, indent=2)

@mcp.tool()
def suggest_terpene_for_concept(concept: str) -> str:
    """Suggest terpenes that would pair well with a given concept."""
    concept_lower = concept.lower()
    
    # Simple keyword matching to suggest terpenes
    suggestions = []
    
    keyword_map = {
        "bright|visible|broadcast|radiant|citrus|energy": "limonene",
        "defense|defensive|barrier|fortress|structure|precise": "pinene",
        "flow|organic|movement|dance|growth|earthy": "myrcene",
        "complex|sophisticated|depth|intelligent|spiced|warm": "caryophyllene",
        "delicate|ethereal|soft|calming|spiritual|romantic": "linalool",
        "fresh|crisp|sophisticated|intellectual|herbal": "terpinolene",
        "grounded|hoppy|ferment|transform|natural": "humulene",
        "delicate|flowing|graceful|energetic|artistic": "ocimene",
        "warm|spiced|dynamic|heat|pepper": "sabinene",
        "romantic|floral|beautiful|inviting|blooming": "geraniol",
        "medicinal|potent|herbal|historical|intentional": "thymol"
    }
    
    for keywords, terpene_id in keyword_map.items():
        if any(kw in concept_lower for kw in keywords.split("|")):
            suggestions.append({
                "terpene": TERPENES[terpene_id]["name"],
                "terpene_id": terpene_id,
                "reason": f"Concept contains '{concept}' which aligns with {TERPENES[terpene_id]['visual_character']} aesthetic"
            })
    
    if not suggestions:
        # Default to showing all with fusion strength
        suggestions = [
            {
                "terpene": TERPENES[t_id]["name"],
                "terpene_id": t_id,
                "fusion_strength": TERPENES[t_id]["fusion_strength"]
            }
            for t_id in list(TERPENES.keys())[:5]
        ]
    
    return json.dumps({
        "concept": concept,
        "suggestions": suggestions,
        "note": "These are suggestions based on semantic bridges. Try different terpenes to see which works best for your specific intent."
    }, indent=2)

@mcp.tool()
def apply_intensity_modifier(terpene_name: str, intensity: float) -> str:
    """Apply an intensity multiplier (0-1) to a terpene's color/saturation parameters."""
    if not 0 <= intensity <= 1:
        return json.dumps({"error": "Intensity must be between 0 and 1"})
    
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENES:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found"})
    
    terpene = TERPENES[terpene_id]
    
    return json.dumps({
        "terpene": terpene["name"],
        "intensity_level": intensity,
        "intensity_description": {
            0.0: "Ignored - use base prompt only",
            0.25: "Subtle - gentle hints of terpene character",
            0.5: "Balanced - terpene reshapes execution while subject remains primary",
            0.75: "Strong - terpene properties heavily influence all aspects",
            1.0: "Maximum - terpene dominates while subject remains recognizable"
        }.get(round(intensity, 2), f"Custom intensity {intensity}"),
        "application": {
            "saturation_modifier": intensity,
            "luminosity_modifier": 0.7 + (intensity * 0.3),
            "edge_softness_modifier": 1 - (intensity * 0.5),
            "composition_emphasis": "Minimal" if intensity < 0.3 else "Balanced" if intensity < 0.7 else "Maximum"
        }
    }, indent=2)


# ============================================================================
# PHASE 2.6 - RHYTHMIC PRESETS & MORPHOSPACE COORDINATES
# ============================================================================
#
# Normalized 5D parameter space for terpene aesthetics.
# Each terpene maps to coordinates in [0, 1]^5 derived from its
# color specs, temporal qualities, and compositional character.
#
# Parameters:
#   saturation_intensity  - Color saturation depth (0=muted/pastel, 1=vivid/saturated)
#   luminosity_level      - Brightness/lightness (0=dark/deep, 1=bright/luminous)
#   edge_definition       - Boundary sharpness (0=watercolor-soft, 1=crystalline-sharp)
#   color_warmth          - Temperature axis (0=cool lavender/green, 1=warm amber/burgundy)
#   structural_complexity - Form intricacy (0=simple flowing, 1=interlocking geometric)
#

TERPENE_PARAMETER_NAMES = [
    "saturation_intensity",
    "luminosity_level",
    "edge_definition",
    "color_warmth",
    "structural_complexity"
]

TERPENE_COORDS = {
    "limonene": {
        "saturation_intensity": 0.85,
        "luminosity_level": 0.85,
        "edge_definition": 0.80,
        "color_warmth": 0.60,
        "structural_complexity": 0.55
    },
    "pinene": {
        "saturation_intensity": 0.72,
        "luminosity_level": 0.60,
        "edge_definition": 0.85,
        "color_warmth": 0.45,
        "structural_complexity": 0.80
    },
    "myrcene": {
        "saturation_intensity": 0.55,
        "luminosity_level": 0.40,
        "edge_definition": 0.20,
        "color_warmth": 0.70,
        "structural_complexity": 0.30
    },
    "caryophyllene": {
        "saturation_intensity": 0.68,
        "luminosity_level": 0.50,
        "edge_definition": 0.50,
        "color_warmth": 0.85,
        "structural_complexity": 0.85
    },
    "linalool": {
        "saturation_intensity": 0.55,
        "luminosity_level": 0.85,
        "edge_definition": 0.10,
        "color_warmth": 0.30,
        "structural_complexity": 0.35
    },
    "terpinolene": {
        "saturation_intensity": 0.70,
        "luminosity_level": 0.78,
        "edge_definition": 0.55,
        "color_warmth": 0.40,
        "structural_complexity": 0.70
    },
    "humulene": {
        "saturation_intensity": 0.70,
        "luminosity_level": 0.55,
        "edge_definition": 0.40,
        "color_warmth": 0.75,
        "structural_complexity": 0.75
    },
    "ocimene": {
        "saturation_intensity": 0.50,
        "luminosity_level": 0.82,
        "edge_definition": 0.15,
        "color_warmth": 0.35,
        "structural_complexity": 0.25
    },
    "sabinene": {
        "saturation_intensity": 0.75,
        "luminosity_level": 0.62,
        "edge_definition": 0.70,
        "color_warmth": 0.80,
        "structural_complexity": 0.65
    },
    "geraniol": {
        "saturation_intensity": 0.60,
        "luminosity_level": 0.82,
        "edge_definition": 0.15,
        "color_warmth": 0.55,
        "structural_complexity": 0.30
    },
    "thymol": {
        "saturation_intensity": 0.75,
        "luminosity_level": 0.62,
        "edge_definition": 0.60,
        "color_warmth": 0.70,
        "structural_complexity": 0.70
    }
}

# Phase 2.6 Rhythmic Presets
# Each preset defines an oscillation between two terpene states,
# creating a temporal aesthetic trajectory in 5D parameter space.
#
# These become attractor manifolds for Tier 4C/4D limit cycle discovery.

TERPENE_RHYTHMIC_PRESETS = {
    "volatility_wave": {
        "state_a": "limonene",
        "state_b": "caryophyllene",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 20,
        "description": "Bright volatile citrus ↔ deep persistent spice. "
                       "Oscillates between high-luminosity radial burst and "
                       "low-luminosity layered warmth."
    },
    "floral_drift": {
        "state_a": "linalool",
        "state_b": "geraniol",
        "pattern": "sinusoidal",
        "num_cycles": 5,
        "steps_per_cycle": 16,
        "description": "Cool lavender ethereal ↔ warm rose romantic. "
                       "Gentle oscillation between floral poles—both soft-edged "
                       "but differing in warmth and color family."
    },
    "defense_pulse": {
        "state_a": "pinene",
        "state_b": "myrcene",
        "pattern": "triangular",
        "num_cycles": 3,
        "steps_per_cycle": 24,
        "description": "Sharp crystalline defense ↔ soft organic flow. "
                       "Maximum edge-definition contrast: geometric fortress "
                       "dissolving into earthy ribbons and back."
    },
    "warmth_cycle": {
        "state_a": "ocimene",
        "state_b": "sabinene",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 18,
        "description": "Cool delicate pastel ↔ warm dynamic spice. "
                       "Spans the full warmth axis with simultaneous "
                       "complexity and edge transitions."
    },
    "complexity_cascade": {
        "state_a": "terpinolene",
        "state_b": "humulene",
        "pattern": "triangular",
        "num_cycles": 3,
        "steps_per_cycle": 22,
        "description": "Fresh sophisticated clarity ↔ earthy grounded warmth. "
                       "Two complex terpenes trading between cool precision "
                       "and warm density."
    }
}


def _generate_terpene_oscillation(
    num_steps: int,
    num_cycles: float,
    pattern: str
) -> list:
    """Generate oscillation alpha values [0, 1] for preset interpolation.

    Pure Layer 2 computation - zero token cost.
    """
    import math
    result = []
    for i in range(num_steps):
        t = 2 * math.pi * num_cycles * i / num_steps
        if pattern == "sinusoidal":
            result.append(0.5 * (1 + math.sin(t)))
        elif pattern == "triangular":
            t_norm = (t / (2 * math.pi)) % 1.0
            result.append(2 * t_norm if t_norm < 0.5 else 2 * (1 - t_norm))
        elif pattern == "square":
            t_norm = (t / (2 * math.pi)) % 1.0
            result.append(0.0 if t_norm < 0.5 else 1.0)
        else:
            result.append(0.5)
    return result


def _generate_preset_trajectory(preset_config: dict) -> list:
    """Generate full preset trajectory as list of state dicts.

    Returns list of dicts, each mapping parameter name → value.
    """
    state_a = TERPENE_COORDS[preset_config["state_a"]]
    state_b = TERPENE_COORDS[preset_config["state_b"]]
    total_steps = preset_config["num_cycles"] * preset_config["steps_per_cycle"]

    alphas = _generate_terpene_oscillation(
        total_steps,
        preset_config["num_cycles"],
        preset_config["pattern"]
    )

    trajectory = []
    for alpha in alphas:
        state = {}
        for p in TERPENE_PARAMETER_NAMES:
            state[p] = state_a[p] * (1 - alpha) + state_b[p] * alpha
        trajectory.append(state)

    return trajectory


@mcp.tool()
def get_terpene_coordinates(terpene_name: str) -> str:
    """Get normalized 5D morphospace coordinates for a terpene.

    Returns the terpene's position in the aesthetic parameter space used
    by Phase 2.6 rhythmic presets and Tier 4 attractor discovery.

    Parameters:
      saturation_intensity  - Color depth (0=pastel, 1=vivid)
      luminosity_level      - Brightness (0=dark, 1=luminous)
      edge_definition       - Boundary sharpness (0=watercolor, 1=crystalline)
      color_warmth          - Temperature (0=cool, 1=warm)
      structural_complexity - Form intricacy (0=flowing, 1=interlocking)

    Args:
        terpene_name: Name of terpene (e.g. 'limonene', 'caryophyllene')

    Returns:
        JSON with coordinates and parameter descriptions

    Cost: 0 tokens (deterministic lookup)
    """
    terpene_id = terpene_name.lower().strip()
    if terpene_id not in TERPENE_COORDS:
        return json.dumps({"error": f"Terpene '{terpene_name}' not found in morphospace"})

    coords = TERPENE_COORDS[terpene_id]
    return json.dumps({
        "terpene": terpene_id,
        "parameter_names": TERPENE_PARAMETER_NAMES,
        "coordinates": coords,
        "description": TERPENES[terpene_id]["visual_character"]
    }, indent=2)


@mcp.tool()
def list_rhythmic_presets() -> str:
    """List all Phase 2.6 terpene rhythmic presets.

    Each preset defines an oscillation between two terpene states
    in 5D parameter space, creating temporal aesthetic trajectories.

    Returns:
        JSON list of preset configurations with periods and descriptions

    Cost: 0 tokens (deterministic lookup)
    """
    result = []
    for name, config in TERPENE_RHYTHMIC_PRESETS.items():
        result.append({
            "preset_id": name,
            "state_a": config["state_a"],
            "state_b": config["state_b"],
            "pattern": config["pattern"],
            "steps_per_cycle": config["steps_per_cycle"],
            "num_cycles": config["num_cycles"],
            "total_steps": config["num_cycles"] * config["steps_per_cycle"],
            "description": config["description"]
        })
    return json.dumps(result, indent=2)


@mcp.tool()
def generate_rhythmic_composition(
    preset_name: str,
    num_cycles: Optional[int] = None,
    steps_per_cycle: Optional[int] = None
) -> str:
    """Generate a rhythmic composition trajectory from a Phase 2.6 preset.

    Computes the full oscillation trajectory between two terpene states
    in 5D parameter space. Each step is a complete aesthetic configuration
    suitable for frame-by-frame image generation or temporal visualization.

    Args:
        preset_name: Preset ID (e.g. 'volatility_wave', 'defense_pulse')
        num_cycles: Override default cycle count (optional)
        steps_per_cycle: Override default steps per cycle (optional)

    Returns:
        JSON with trajectory (list of parameter states), metadata, and
        endpoint terpene descriptions

    Cost: 0 tokens (deterministic interpolation)
    """
    preset_id = preset_name.lower().strip()
    if preset_id not in TERPENE_RHYTHMIC_PRESETS:
        available = list(TERPENE_RHYTHMIC_PRESETS.keys())
        return json.dumps({"error": f"Preset '{preset_name}' not found. Available: {available}"})

    config = TERPENE_RHYTHMIC_PRESETS[preset_id].copy()
    if num_cycles is not None:
        config["num_cycles"] = num_cycles
    if steps_per_cycle is not None:
        config["steps_per_cycle"] = steps_per_cycle

    trajectory = _generate_preset_trajectory(config)

    # Sample 5 keyframes for preview
    total = len(trajectory)
    indices = [0, total // 4, total // 2, 3 * total // 4, total - 1]
    keyframes = [{"step": i, "state": trajectory[i]} for i in indices]

    return json.dumps({
        "preset": preset_id,
        "description": config["description"],
        "state_a": config["state_a"],
        "state_b": config["state_b"],
        "pattern": config["pattern"],
        "period": config["steps_per_cycle"],
        "total_steps": total,
        "keyframes": keyframes,
        "trajectory": trajectory,
        "endpoint_visuals": {
            config["state_a"]: TERPENES[config["state_a"]]["visual_character"],
            config["state_b"]: TERPENES[config["state_b"]]["visual_character"]
        }
    }, indent=2)


@mcp.tool()
def extract_terpene_morphospace() -> str:
    """Extract complete terpene morphospace for Tier 4 attractor discovery.

    Returns all terpene coordinates and preset configurations in the format
    expected by the emergent attractor characterization system
    (domain_registry.py / emergent_attractor_system.py).

    This is the integration point for multi-domain composition—compose
    terpene presets with microscopy, nuclear, catastrophe, etc.

    Returns:
        JSON with domain_id, parameter_names, coordinates, and presets

    Cost: 0 tokens (deterministic extraction)
    """
    presets_export = {}
    for name, config in TERPENE_RHYTHMIC_PRESETS.items():
        presets_export[name] = {
            "period": config["steps_per_cycle"],
            "state_a": config["state_a"],
            "state_b": config["state_b"],
            "pattern": config["pattern"],
            "description": config["description"]
        }

    return json.dumps({
        "domain_id": "terpene",
        "display_name": "Terpene Visual Vocabulary",
        "mcp_server": "terpene-vocabulary",
        "parameter_names": TERPENE_PARAMETER_NAMES,
        "state_coordinates": TERPENE_COORDS,
        "presets": presets_export,
        "individual_periods": [
            config["steps_per_cycle"]
            for config in TERPENE_RHYTHMIC_PRESETS.values()
        ],
        "unique_periods": sorted(set(
            config["steps_per_cycle"]
            for config in TERPENE_RHYTHMIC_PRESETS.values()
        )),
        "integration_notes": (
            "Register via domain_registry.py using register_terpene_domain(). "
            "All 11 terpene states available as canonical coordinates. "
            "5 rhythmic presets with periods [16, 18, 20, 22, 24]."
        )
    }, indent=2)


# ============================================================================
# PHASE 2.7 - ATTRACTOR VISUALIZATION PROMPT GENERATION
# ============================================================================
#
# Translates parameter-space positions into image generation vocabulary.
# Maps 5D terpene coordinates to visual descriptors using nearest-neighbor
# lookup against canonical visual types.
#
# Visual types cluster the 11 terpenes into 5 aesthetic families:
#   citrus_radiant    - limonene, sabinene: bright, saturated, sharp, warm
#   forest_crystalline - pinene, terpinolene: geometric, green, precise
#   earth_flowing     - myrcene, humulene: organic, muted, warm, grounded
#   deep_spiced       - caryophyllene, thymol: layered, complex, dark, warm
#   ethereal_floral   - linalool, ocimene, geraniol: soft, luminous, delicate
#

TERPENE_VISUAL_TYPES = {
    "citrus_radiant": {
        "coords": {
            "saturation_intensity": 0.80,
            "luminosity_level": 0.74,
            "edge_definition": 0.75,
            "color_warmth": 0.70,
            "structural_complexity": 0.60
        },
        "keywords": [
            "saturated yellow-orange radial burst",
            "crisp bright highlight edges",
            "concentric spirals emanating from luminous center",
            "warm citrus palette with sharp angular forms",
            "high-luminosity translucent color field",
            "volatile energy captured in crystalline geometry",
            "zesty acidic color transitions"
        ]
    },
    "forest_crystalline": {
        "coords": {
            "saturation_intensity": 0.71,
            "luminosity_level": 0.69,
            "edge_definition": 0.70,
            "color_warmth": 0.42,
            "structural_complexity": 0.75
        },
        "keywords": [
            "deep green interlocking geometric planes",
            "amber-like translucent crystalline forms",
            "needle-like protrusions catching cool light",
            "layered shadow depth between angular structures",
            "resinous surfaces with sharp intersections",
            "cool-toned precision with forest undertones",
            "defensive geometric lattice in green and amber"
        ]
    },
    "earth_flowing": {
        "coords": {
            "saturation_intensity": 0.62,
            "luminosity_level": 0.48,
            "edge_definition": 0.30,
            "color_warmth": 0.72,
            "structural_complexity": 0.52
        },
        "keywords": [
            "warm ochre and brown flowing ribbons",
            "soft blurred boundaries between earth tones",
            "matte organic surfaces with directional movement",
            "distributed earthy presence diffusing into space",
            "golden-brown translucence with herbal undertones",
            "grounded compositional weight in muted palette"
        ]
    },
    "deep_spiced": {
        "coords": {
            "saturation_intensity": 0.72,
            "luminosity_level": 0.56,
            "edge_definition": 0.55,
            "color_warmth": 0.78,
            "structural_complexity": 0.78
        },
        "keywords": [
            "deep burgundy layered with warm amber",
            "interlocking forms creating sophisticated depth",
            "rich spiced warmth permeating dark earth tones",
            "complex structural relationships in warm darkness",
            "translucent amber captured within geometric density",
            "medicinal precision with warm copper accents",
            "sesquiterpene visual weight and persistence"
        ]
    },
    "ethereal_floral": {
        "coords": {
            "saturation_intensity": 0.55,
            "luminosity_level": 0.83,
            "edge_definition": 0.13,
            "color_warmth": 0.40,
            "structural_complexity": 0.30
        },
        "keywords": [
            "soft lavender and pale violet washes",
            "watercolor-like translucent boundaries",
            "ethereal luminous forms in pastel palette",
            "delicate rose-cream tones with high brightness",
            "graceful flowing structures dissolving at edges",
            "calming floral presence with gentle light"
        ]
    }
}


# Optical properties for each visual type — used by map_terpene_parameters
# and image generators that accept material/finish specifications.
TERPENE_OPTICAL_PROPERTIES = {
    "citrus_radiant": {
        "finish": "glossy translucent",
        "refraction": "high — light passes through with bright caustics",
        "color_temperature": "warm (5500-6500K citrus daylight)",
        "surface_quality": "smooth glassy with sharp specular highlights",
        "transparency": "semi-transparent, backlit glow",
        "scatter": "minimal — clean light transmission"
    },
    "forest_crystalline": {
        "finish": "resinous semi-matte with amber depth",
        "refraction": "moderate — amber-like internal glow",
        "color_temperature": "cool-neutral (5000-5800K forest light)",
        "surface_quality": "faceted crystalline with sharp intersections",
        "transparency": "translucent amber to opaque at depth",
        "scatter": "moderate — subsurface scattering in resin"
    },
    "earth_flowing": {
        "finish": "matte to satin with organic sheen",
        "refraction": "low — absorbed light, muted returns",
        "color_temperature": "warm (4000-5000K golden hour earth)",
        "surface_quality": "soft organic with directional flow marks",
        "transparency": "mostly opaque, translucent at thin edges",
        "scatter": "high — diffuse warm glow"
    },
    "deep_spiced": {
        "finish": "lacquered matte with selective gloss",
        "refraction": "low-moderate — deep internal warmth",
        "color_temperature": "very warm (3200-4200K firelight)",
        "surface_quality": "layered complex with visible depth planes",
        "transparency": "opaque dark with translucent amber accents",
        "scatter": "low — light absorbed into depth"
    },
    "ethereal_floral": {
        "finish": "watercolor matte with soft luminance",
        "refraction": "very high — light diffuses through pastel washes",
        "color_temperature": "cool (6500-8000K overcast floral)",
        "surface_quality": "soft gradients with dissolved edges",
        "transparency": "highly translucent, luminous from within",
        "scatter": "very high — maximum diffusion, glow"
    }
}


# ============================================================================
# TERPENE VOCABULARY CATEGORIES
# ============================================================================
#
# Indexed by parameter ranges for context-sensitive keyword selection.
# Used by map_terpene_parameters to weight vocabulary by emphasis.

TERPENE_VOCABULARY = {
    "color_palette": {
        "high_saturation": [
            "vivid saturated pigments", "intense chromatic depth",
            "bold color concentration", "rich tonal presence"
        ],
        "low_saturation": [
            "muted pastel washes", "desaturated earth tones",
            "gentle diluted hues", "whispered color"
        ]
    },
    "light_behavior": {
        "high_luminosity": [
            "bright luminous glow", "high-key radiant light",
            "brilliant translucent diffusion", "incandescent warmth"
        ],
        "low_luminosity": [
            "deep shadow-rich pools", "low-key absorbed light",
            "matte dark earth presence", "subterranean glow"
        ]
    },
    "edge_character": {
        "sharp_edges": [
            "crystalline hard edges", "precisely defined contours",
            "geometric faceted boundaries", "crisp angular intersections"
        ],
        "soft_edges": [
            "watercolor dissolved boundaries", "gentle gradient transitions",
            "organic flowing contours", "diffused ethereal margins"
        ]
    },
    "thermal_quality": {
        "warm_tones": [
            "amber-gold warmth", "spiced earth radiance",
            "sun-warmed copper glow", "burgundy thermal depth"
        ],
        "cool_tones": [
            "cool lavender stillness", "green-blue forest calm",
            "pale silvery light", "mint-tinged freshness"
        ]
    },
    "structural_form": {
        "complex_structure": [
            "interlocking geometric planes", "layered depth relationships",
            "multi-scale structural density", "fractal-like recursive forms"
        ],
        "simple_structure": [
            "flowing singular ribbons", "simple organic curves",
            "minimal open composition", "graceful unadorned forms"
        ]
    }
}


# ============================================================================
# ATTRACTOR PRESETS — Discovered and Curated
# ============================================================================
#
# Terpene-domain coordinates for known emergent attractors from Tier 4D
# multi-domain compositional limit cycle discovery.
#
# Each preset specifies WHERE in terpene morphospace the attractor sits —
# the characteristic terpene aesthetic that dominates at each period.

TERPENE_ATTRACTOR_PRESETS = {
    # ── Tier 1: Stable Cores ──────────────────────────────────────────
    "period_30": {
        "name": "Period 30 — Universal Sync",
        "description": (
            "Dominant LCM synchronization. Terpene complexity_cascade preset "
            "(period 22) is nearest individual. Attractor sits in the "
            "forest_crystalline territory — cool-toned geometric precision "
            "with moderate warmth. The most stable multi-domain terpene state."
        ),
        "basin_size": 0.116,
        "classification": "lcm_sync",
        "source_domains": ["microscopy", "diatom", "heraldic", "terpene"],
        "state": {
            "saturation_intensity": 0.68,
            "luminosity_level": 0.65,
            "edge_definition": 0.62,
            "color_warmth": 0.55,
            "structural_complexity": 0.65
        }
    },
    "period_29": {
        "name": "Period 29 — Emergent Resonance",
        "description": (
            "Purely emergent multi-domain attractor. Terpene character is "
            "an intermediate state between forest_crystalline and earth_flowing — "
            "cool geometric structure softening into organic warmth. "
            "This aesthetic exists nowhere in any single terpene."
        ),
        "basin_size": 0.084,
        "classification": "lcm_sync",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom", "heraldic"],
        "state": {
            "saturation_intensity": 0.62,
            "luminosity_level": 0.58,
            "edge_definition": 0.48,
            "color_warmth": 0.62,
            "structural_complexity": 0.58
        }
    },
    "period_19": {
        "name": "Period 19 — Gap Flow",
        "description": (
            "Resilient novel gap-filler between periods 18 and 20. "
            "Terpene is a bright precise state with strong edges and "
            "moderate complexity — the clean analytical character of "
            "laboratory-grade terpene visualization. Prime-period beats."
        ),
        "basin_size": 0.074,
        "classification": "novel",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom"],
        "state": {
            "saturation_intensity": 0.72,
            "luminosity_level": 0.72,
            "edge_definition": 0.75,
            "color_warmth": 0.48,
            "structural_complexity": 0.70
        }
    },
    # ── Tier 2: Specialized ───────────────────────────────────────────
    "period_28": {
        "name": "Period 28 — Composite Beat",
        "description": (
            "Novel composite beat (Period 60 − 2×16 = 28). Terpene sits "
            "in the deep_spiced zone — rich layered warmth with structural "
            "complexity. Tension between persistent base-note depth "
            "and geometric precision. The held breath of spice."
        ),
        "basin_size": 0.024,
        "classification": "novel",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom"],
        "state": {
            "saturation_intensity": 0.70,
            "luminosity_level": 0.52,
            "edge_definition": 0.55,
            "color_warmth": 0.78,
            "structural_complexity": 0.78
        }
    },
    "period_60": {
        "name": "Period 60 — Harmonic Hub",
        "description": (
            "Major LCM hub (3×20, 4×15, 5×12). Terpene oscillates through "
            "full aromatic palette — volatile citrus through resinous depth "
            "across the long cycle. Complex synchronization, advanced use."
        ),
        "basin_size": 0.040,
        "classification": "harmonic",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom"],
        "state": {
            "saturation_intensity": 0.65,
            "luminosity_level": 0.62,
            "edge_definition": 0.52,
            "color_warmth": 0.58,
            "structural_complexity": 0.60
        }
    },
    # ── Tier 3: Curated Edge States ───────────────────────────────────
    "volatile_burst": {
        "name": "Volatile Burst — Top-Note Flash",
        "description": (
            "Curated state at maximum volatility. Pure limonene territory: "
            "the initial burst of citrus when a peel is snapped — "
            "maximum saturation, luminosity, and edge definition with "
            "angular radial geometry. Bright, sharp, ephemeral."
        ),
        "basin_size": None,
        "classification": "curated",
        "source_domains": ["terpene"],
        "state": {
            "saturation_intensity": 0.88,
            "luminosity_level": 0.88,
            "edge_definition": 0.85,
            "color_warmth": 0.62,
            "structural_complexity": 0.58
        }
    },
    "base_note_depth": {
        "name": "Base Note Depth — Persistent Ground",
        "description": (
            "Curated state at maximum persistence and depth. Myrcene-"
            "caryophyllene blend: the lingering base note hours after "
            "application — warm, matte, flowing, complex, absorbed into "
            "the body like earth absorbing rain."
        ),
        "basin_size": None,
        "classification": "curated",
        "source_domains": ["terpene"],
        "state": {
            "saturation_intensity": 0.60,
            "luminosity_level": 0.42,
            "edge_definition": 0.28,
            "color_warmth": 0.80,
            "structural_complexity": 0.62
        }
    }
}


# ============================================================================
# Phase 2.6/2.7 Helper Functions
# ============================================================================

def _terpene_euclidean_distance(
    a: Dict[str, float], b: Dict[str, float]
) -> float:
    """Euclidean distance between two states in terpene parameter space."""
    import math
    return math.sqrt(sum(
        (a.get(p, 0.5) - b.get(p, 0.5)) ** 2
        for p in TERPENE_PARAMETER_NAMES
    ))


def _terpene_nearest_visual_type(
    params: Dict[str, float]
) -> tuple:
    """Find nearest visual type and return (type_name, distance)."""
    import math
    best_type = None
    best_dist = float("inf")
    for type_name, type_data in TERPENE_VISUAL_TYPES.items():
        dist = math.sqrt(sum(
            (params.get(p, 0.5) - type_data["coords"][p]) ** 2
            for p in TERPENE_PARAMETER_NAMES
        ))
        if dist < best_dist:
            best_dist = dist
            best_type = type_name
    return best_type, best_dist


def _terpene_select_vocabulary(params: Dict[str, float]) -> Dict[str, list]:
    """Select vocabulary terms based on parameter values."""
    sat = params.get("saturation_intensity", 0.5)
    lum = params.get("luminosity_level", 0.5)
    edge = params.get("edge_definition", 0.5)
    warm = params.get("color_warmth", 0.5)
    comp = params.get("structural_complexity", 0.5)

    result = {}
    result["color_palette"] = (
        TERPENE_VOCABULARY["color_palette"]["high_saturation"]
        if sat >= 0.5 else
        TERPENE_VOCABULARY["color_palette"]["low_saturation"]
    )
    result["light_behavior"] = (
        TERPENE_VOCABULARY["light_behavior"]["high_luminosity"]
        if lum >= 0.5 else
        TERPENE_VOCABULARY["light_behavior"]["low_luminosity"]
    )
    result["edge_character"] = (
        TERPENE_VOCABULARY["edge_character"]["sharp_edges"]
        if edge >= 0.5 else
        TERPENE_VOCABULARY["edge_character"]["soft_edges"]
    )
    result["thermal_quality"] = (
        TERPENE_VOCABULARY["thermal_quality"]["warm_tones"]
        if warm >= 0.5 else
        TERPENE_VOCABULARY["thermal_quality"]["cool_tones"]
    )
    result["structural_form"] = (
        TERPENE_VOCABULARY["structural_form"]["complex_structure"]
        if comp >= 0.5 else
        TERPENE_VOCABULARY["structural_form"]["simple_structure"]
    )
    return result


def _extract_visual_vocabulary_from_terpene_params(
    params: dict,
    strength: float = 1.0
) -> dict:
    """Find nearest visual type and return weighted keywords.

    Pure Layer 2 nearest-neighbor lookup. Zero token cost.

    Args:
        params: Dict mapping parameter names to float values [0, 1]
        strength: Weight multiplier for keyword inclusion (0-1)

    Returns:
        Dict with nearest_type, distance, and keywords list
    """
    import math

    best_type = None
    best_dist = float("inf")

    for type_name, type_data in TERPENE_VISUAL_TYPES.items():
        dist_sq = 0.0
        for p in TERPENE_PARAMETER_NAMES:
            val = params.get(p, 0.5)
            ref = type_data["coords"][p]
            dist_sq += (val - ref) ** 2
        dist = math.sqrt(dist_sq)
        if dist < best_dist:
            best_dist = dist
            best_type = type_name

    type_data = TERPENE_VISUAL_TYPES[best_type]

    # Select keywords proportional to strength
    all_kw = type_data["keywords"]
    n_keywords = max(2, int(len(all_kw) * strength))
    selected = all_kw[:n_keywords]

    return {
        "nearest_type": best_type,
        "distance": round(best_dist, 4),
        "keywords": selected,
        "strength": strength
    }


def _find_nearest_terpene(params: dict) -> str:
    """Find the nearest canonical terpene state to a parameter vector."""
    import math
    best_id = None
    best_dist = float("inf")
    for terp_id, terp_coords in TERPENE_COORDS.items():
        dist_sq = sum(
            (params.get(p, 0.5) - terp_coords[p]) ** 2
            for p in TERPENE_PARAMETER_NAMES
        )
        if dist_sq < best_dist:
            best_dist = dist_sq
            best_id = terp_id
    return best_id


@mcp.tool()
def generate_attractor_visualization_prompt(
    attractor_state: str,
    mode: Optional[Literal["composite", "split_view", "sequence"]] = "composite",
    style_prefix: Optional[str] = ""
) -> str:
    """Generate image-generation prompts from an attractor state in terpene parameter space.

    Phase 2.7 visualization: translates a discovered attractor's terpene-domain
    coordinates into descriptive vocabulary suitable for text-to-image models.

    Three output modes:
      composite  - Single blended prompt combining all visual keywords
      split_view - Separate prompt section for the terpene domain
      sequence   - Multiple keyframe prompts for animation/video

    Args:
        attractor_state: JSON string with terpene parameter values, e.g.
            '{"saturation_intensity": 0.72, "luminosity_level": 0.56, ...}'
            OR a terpene name like "caryophyllene" to use its canonical coords
        mode: Output format (composite|split_view|sequence)
        style_prefix: Optional prefix prepended to generated prompts
            (e.g. "oil painting of", "microscopic photograph of")

    Returns:
        JSON with generated prompt(s), vocabulary breakdown, and nearest
        terpene identification

    Cost: 0 tokens (deterministic vocabulary extraction + nearest-neighbor)
    """
    # Parse attractor state
    try:
        if isinstance(attractor_state, str):
            stripped = attractor_state.strip()
            # Check if it's a terpene name rather than JSON
            if stripped.lower() in TERPENE_COORDS:
                params = TERPENE_COORDS[stripped.lower()]
            else:
                params = json.loads(stripped)
        else:
            params = attractor_state
    except (json.JSONDecodeError, TypeError):
        return json.dumps({
            "error": "Could not parse attractor_state. Provide JSON parameter dict "
                     "or a terpene name (e.g. 'caryophyllene')."
        })

    # Validate parameters present
    missing = [p for p in TERPENE_PARAMETER_NAMES if p not in params]
    if missing:
        return json.dumps({
            "error": f"Missing parameters: {missing}",
            "expected": TERPENE_PARAMETER_NAMES
        })

    # Extract vocabulary
    vocab = _extract_visual_vocabulary_from_terpene_params(params, strength=1.0)
    nearest_terpene = _find_nearest_terpene(params)
    nearest_terpene_data = TERPENES[nearest_terpene]

    if mode == "composite":
        # Single blended prompt
        keyword_str = ", ".join(vocab["keywords"])
        prompt_parts = []
        if style_prefix:
            prompt_parts.append(style_prefix.strip())
        prompt_parts.append(keyword_str)
        prompt_parts.append(
            f"inspired by {nearest_terpene_data['name'].lower()} "
            f"terpene aesthetic, {nearest_terpene_data['visual_character'].lower()}"
        )
        full_prompt = ", ".join(prompt_parts)

        return json.dumps({
            "mode": "composite",
            "prompt": full_prompt,
            "vocabulary": {
                "visual_type": vocab["nearest_type"],
                "keywords": vocab["keywords"],
                "type_distance": vocab["distance"]
            },
            "nearest_terpene": nearest_terpene,
            "terpene_character": nearest_terpene_data["visual_character"],
            "parameters": {p: round(params[p], 3) for p in TERPENE_PARAMETER_NAMES}
        }, indent=2)

    elif mode == "split_view":
        # Separate domain prompt section
        keyword_str = ", ".join(vocab["keywords"])

        return json.dumps({
            "mode": "split_view",
            "domain": "terpene",
            "domain_prompt": (
                f"{style_prefix + ', ' if style_prefix else ''}"
                f"{keyword_str}"
            ),
            "domain_context": (
                f"Terpene domain: {nearest_terpene_data['name']} aesthetic — "
                f"{nearest_terpene_data['visual_character']}. "
                f"{nearest_terpene_data['composition']}"
            ),
            "vocabulary": {
                "visual_type": vocab["nearest_type"],
                "keywords": vocab["keywords"],
                "type_distance": vocab["distance"]
            },
            "nearest_terpene": nearest_terpene,
            "color_palette": nearest_terpene_data["color_specs"]["primary_palette"],
            "parameters": {p: round(params[p], 3) for p in TERPENE_PARAMETER_NAMES}
        }, indent=2)

    elif mode == "sequence":
        # Generate keyframes along a trajectory from current state toward
        # the two nearest visual-type poles
        keyframes = []

        # Keyframe 0: current state
        kw0 = ", ".join(vocab["keywords"][:4])
        keyframes.append({
            "frame": 0,
            "prompt": f"{style_prefix + ', ' if style_prefix else ''}{kw0}",
            "label": f"Attractor center — {vocab['nearest_type']}"
        })

        # Keyframe 1: shift toward nearest canonical terpene at full strength
        near_coords = TERPENE_COORDS[nearest_terpene]
        mid_params = {
            p: 0.5 * params[p] + 0.5 * near_coords[p]
            for p in TERPENE_PARAMETER_NAMES
        }
        vocab_mid = _extract_visual_vocabulary_from_terpene_params(mid_params, strength=0.8)
        kw1 = ", ".join(vocab_mid["keywords"][:4])
        keyframes.append({
            "frame": 1,
            "prompt": (
                f"{style_prefix + ', ' if style_prefix else ''}{kw1}, "
                f"shifting toward {nearest_terpene_data['name'].lower()} character"
            ),
            "label": f"Approaching {nearest_terpene}"
        })

        # Keyframe 2: at canonical terpene state
        vocab_full = _extract_visual_vocabulary_from_terpene_params(near_coords, strength=1.0)
        kw2 = ", ".join(vocab_full["keywords"][:5])
        keyframes.append({
            "frame": 2,
            "prompt": (
                f"{style_prefix + ', ' if style_prefix else ''}{kw2}, "
                f"pure {nearest_terpene_data['name'].lower()} terpene aesthetic"
            ),
            "label": f"Canonical {nearest_terpene}"
        })

        return json.dumps({
            "mode": "sequence",
            "keyframes": keyframes,
            "nearest_terpene": nearest_terpene,
            "parameters": {p: round(params[p], 3) for p in TERPENE_PARAMETER_NAMES}
        }, indent=2)

    else:
        return json.dumps({"error": f"Unknown mode '{mode}'. Use composite, split_view, or sequence."})


@mcp.tool()
def generate_rhythmic_visualization_prompts(
    preset_name: str,
    num_keyframes: Optional[int] = 5,
    style_prefix: Optional[str] = ""
) -> str:
    """Generate a sequence of image prompts from a Phase 2.6 rhythmic preset.

    Samples keyframes along the preset trajectory and converts each to
    an image-generation prompt via vocabulary extraction. Useful for
    creating animated sequences or storyboard panels that visualize
    temporal terpene oscillations.

    Args:
        preset_name: Preset ID (e.g. 'volatility_wave', 'defense_pulse')
        num_keyframes: Number of keyframe prompts to generate (2-20, default 5)
        style_prefix: Optional prefix for all prompts

    Returns:
        JSON with ordered keyframe prompts and trajectory metadata

    Cost: 0 tokens (deterministic trajectory + vocabulary extraction)
    """
    preset_id = preset_name.lower().strip()
    if preset_id not in TERPENE_RHYTHMIC_PRESETS:
        available = list(TERPENE_RHYTHMIC_PRESETS.keys())
        return json.dumps({"error": f"Preset '{preset_name}' not found. Available: {available}"})

    num_keyframes = max(2, min(20, num_keyframes or 5))

    config = TERPENE_RHYTHMIC_PRESETS[preset_id]
    trajectory = _generate_preset_trajectory(config)
    total = len(trajectory)

    # Sample evenly spaced keyframes
    indices = [int(i * (total - 1) / (num_keyframes - 1)) for i in range(num_keyframes)]

    keyframes = []
    for kf_idx, traj_idx in enumerate(indices):
        state = trajectory[traj_idx]
        vocab = _extract_visual_vocabulary_from_terpene_params(state, strength=1.0)
        nearest = _find_nearest_terpene(state)
        nearest_data = TERPENES[nearest]

        kw_str = ", ".join(vocab["keywords"][:5])
        prompt = (
            f"{style_prefix + ', ' if style_prefix else ''}"
            f"{kw_str}, "
            f"{nearest_data['visual_character'].lower()} terpene quality"
        )

        keyframes.append({
            "keyframe": kf_idx,
            "trajectory_step": traj_idx,
            "prompt": prompt,
            "visual_type": vocab["nearest_type"],
            "nearest_terpene": nearest,
            "parameters": {p: round(state[p], 3) for p in TERPENE_PARAMETER_NAMES}
        })

    return json.dumps({
        "preset": preset_id,
        "description": config["description"],
        "state_a": config["state_a"],
        "state_b": config["state_b"],
        "period": config["steps_per_cycle"],
        "total_trajectory_steps": total,
        "num_keyframes": num_keyframes,
        "keyframes": keyframes
    }, indent=2)


@mcp.tool()
def get_terpene_domain_info() -> str:
    """Get complete Phase 2.6 + 2.7 capability summary for the terpene domain.

    Returns server capabilities including morphospace definition,
    rhythmic presets, visual vocabulary types, and integration points
    for multi-domain composition.

    Cost: 0 tokens (static metadata)
    """
    return json.dumps({
        "domain": "terpene",
        "server": "terpene-vocabulary",
        "version": "2.0.0-phase2.7+tier4d",
        "phase_2_6_enhancements": {
            "rhythmic_presets": True,
            "preset_count": len(TERPENE_RHYTHMIC_PRESETS),
            "presets": {
                name: {
                    "period": cfg["steps_per_cycle"],
                    "pattern": cfg["pattern"],
                    "states": f"{cfg['state_a']} ↔ {cfg['state_b']}"
                }
                for name, cfg in TERPENE_RHYTHMIC_PRESETS.items()
            },
            "unique_periods": sorted(set(
                c["steps_per_cycle"] for c in TERPENE_RHYTHMIC_PRESETS.values()
            )),
            "morphospace": {
                "dimensions": len(TERPENE_PARAMETER_NAMES),
                "parameters": TERPENE_PARAMETER_NAMES,
                "canonical_states": len(TERPENE_COORDS),
                "state_names": list(TERPENE_COORDS.keys())
            },
            "custom_oscillation": True,
            "trajectory_computation": True,
            "distance_computation": True
        },
        "phase_2_7_enhancements": {
            "attractor_visualization": True,
            "visual_types": list(TERPENE_VISUAL_TYPES.keys()),
            "visual_type_count": len(TERPENE_VISUAL_TYPES),
            "optical_properties": True,
            "prompt_modes": ["composite", "split_view", "sequence"],
            "attractor_presets": list(TERPENE_ATTRACTOR_PRESETS.keys()),
            "attractor_preset_count": len(TERPENE_ATTRACTOR_PRESETS),
            "rhythmic_visualization": True,
            "vocabulary_categories": list(TERPENE_VOCABULARY.keys())
        },
        "integration": {
            "domain_registry_ready": True,
            "tier_4_compatible": True,
            "multi_domain_composition": True,
            "extract_tool": "get_terpene_domain_registry_config",
            "compatible_servers": [
                "catastrophe-morph-mcp",
                "diatom-morphology-mcp",
                "surface-design-aesthetics",
                "microscopy-aesthetics-mcp",
                "splash-aesthetics-mcp",
                "aesthetic-dynamics-core",
                "composition-graph-mcp"
            ]
        }
    }, indent=2)


# ============================================================================
# PHASE 2.6/2.7 FRAMEWORK-COMPLIANT TOOLS
# ============================================================================
#
# Standard interface tools matching the Lushy Aesthetic Dynamics framework.
# These provide full parity with other domain servers (splash, catastrophe,
# surface-design, diatom, microscopy).

@mcp.tool()
def get_terpene_canonical_states() -> str:
    """List all 11 canonical terpene states with their 5D coordinates.

    Returns every terpene in the morphospace with parameter values,
    visual character description, and the nearest visual type.

    Cost: 0 tokens (deterministic lookup)
    """
    states = []
    for terp_id, coords in TERPENE_COORDS.items():
        vtype, vdist = _terpene_nearest_visual_type(coords)
        terp_meta = TERPENES.get(terp_id, {})
        states.append({
            "terpene_id": terp_id,
            "name": terp_meta.get("name", terp_id),
            "coordinates": coords,
            "visual_character": terp_meta.get("visual_character", ""),
            "classification": terp_meta.get("classification", ""),
            "nearest_visual_type": vtype,
            "visual_type_distance": round(vdist, 4)
        })
    return json.dumps({
        "parameter_names": TERPENE_PARAMETER_NAMES,
        "total_states": len(states),
        "states": states
    }, indent=2)


@mcp.tool()
def get_terpene_visual_types() -> str:
    """List all 5 visual types with keywords and optical properties.

    Visual types cluster the 11 terpenes into aesthetic families.
    Each includes image-generation keywords and material optical specs.

    Cost: 0 tokens (deterministic lookup)
    """
    types = []
    for vtype, vdata in TERPENE_VISUAL_TYPES.items():
        types.append({
            "type_id": vtype,
            "coordinates": vdata["coords"],
            "keywords": vdata["keywords"],
            "optical_properties": TERPENE_OPTICAL_PROPERTIES.get(vtype, {})
        })
    return json.dumps({
        "total_types": len(types),
        "types": types
    }, indent=2)


@mcp.tool()
def compute_terpene_distance(
    terpene_id_1: str,
    terpene_id_2: str
) -> str:
    """Compute Euclidean distance between two terpene states.

    Layer 2: Pure distance computation (0 tokens).

    Args:
        terpene_id_1: First terpene (e.g. 'limonene')
        terpene_id_2: Second terpene (e.g. 'caryophyllene')

    Returns:
        Distance value and per-parameter breakdown.
    """
    id1 = terpene_id_1.lower().strip()
    id2 = terpene_id_2.lower().strip()
    if id1 not in TERPENE_COORDS:
        return json.dumps({"error": f"Unknown: {id1}", "available": list(TERPENE_COORDS.keys())})
    if id2 not in TERPENE_COORDS:
        return json.dumps({"error": f"Unknown: {id2}", "available": list(TERPENE_COORDS.keys())})

    a = TERPENE_COORDS[id1]
    b = TERPENE_COORDS[id2]
    dist = _terpene_euclidean_distance(a, b)
    breakdown = {p: round(abs(a[p] - b[p]), 4) for p in TERPENE_PARAMETER_NAMES}
    max_param = max(breakdown, key=breakdown.get)

    return json.dumps({
        "terpene_1": id1,
        "terpene_2": id2,
        "euclidean_distance": round(dist, 4),
        "per_parameter_difference": breakdown,
        "max_difference_parameter": max_param,
        "max_difference_value": breakdown[max_param]
    }, indent=2)


@mcp.tool()
def compute_terpene_trajectory(
    start_terpene_id: str,
    end_terpene_id: str,
    num_steps: int = 20
) -> str:
    """Compute smooth trajectory between two terpene states.

    Layer 2: Deterministic linear interpolation (0 tokens).
    Each step is a complete 5D parameter state suitable for
    vocabulary extraction or image generation.

    Args:
        start_terpene_id: Starting terpene
        end_terpene_id: Target terpene
        num_steps: Number of interpolation steps (2-100, default 20)

    Returns:
        Trajectory with intermediate states and distance profile.
    """
    sid = start_terpene_id.lower().strip()
    eid = end_terpene_id.lower().strip()
    if sid not in TERPENE_COORDS:
        return json.dumps({"error": f"Unknown: {sid}", "available": list(TERPENE_COORDS.keys())})
    if eid not in TERPENE_COORDS:
        return json.dumps({"error": f"Unknown: {eid}", "available": list(TERPENE_COORDS.keys())})

    num_steps = max(2, min(100, num_steps))
    a = TERPENE_COORDS[sid]
    b = TERPENE_COORDS[eid]
    total_dist = _terpene_euclidean_distance(a, b)

    trajectory = []
    for i in range(num_steps + 1):
        t = i / num_steps
        state = {p: round(a[p] * (1 - t) + b[p] * t, 4) for p in TERPENE_PARAMETER_NAMES}
        vtype, vdist = _terpene_nearest_visual_type(state)
        nearest = _find_nearest_terpene(state)
        trajectory.append({
            "step": i,
            "t": round(t, 3),
            "state": state,
            "nearest_visual_type": vtype,
            "nearest_terpene": nearest
        })

    return json.dumps({
        "start": sid,
        "end": eid,
        "total_distance": round(total_dist, 4),
        "num_steps": num_steps,
        "trajectory": trajectory
    }, indent=2)


@mcp.tool()
def extract_terpene_visual_vocabulary(
    terpene_id: Optional[str] = None,
    custom_state: Optional[str] = None,
    strength: float = 1.0
) -> str:
    """Extract image-generation keywords from terpene coordinates.

    Layer 2: Deterministic nearest-neighbor vocabulary extraction (0 tokens).

    Provide either a canonical terpene name OR a custom state JSON.

    Args:
        terpene_id: Canonical terpene name (e.g. 'pinene')
        custom_state: JSON with 5D parameter values
        strength: Keyword weight multiplier [0.0, 1.0]

    Returns:
        Nearest visual type, keywords, optical properties, and distance.
    """
    if terpene_id:
        tid = terpene_id.lower().strip()
        if tid not in TERPENE_COORDS:
            return json.dumps({"error": f"Unknown: {tid}", "available": list(TERPENE_COORDS.keys())})
        params = TERPENE_COORDS[tid]
    elif custom_state:
        try:
            params = json.loads(custom_state) if isinstance(custom_state, str) else custom_state
        except (json.JSONDecodeError, TypeError):
            return json.dumps({"error": "Could not parse custom_state as JSON"})
        missing = [p for p in TERPENE_PARAMETER_NAMES if p not in params]
        if missing:
            return json.dumps({"error": f"Missing parameters: {missing}"})
    else:
        return json.dumps({"error": "Provide either terpene_id or custom_state"})

    strength = max(0.0, min(1.0, strength))
    vocab = _extract_visual_vocabulary_from_terpene_params(params, strength)
    vtype, vdist = _terpene_nearest_visual_type(params)
    optical = TERPENE_OPTICAL_PROPERTIES.get(vtype, {})

    return json.dumps({
        "nearest_visual_type": vtype,
        "visual_type_distance": round(vdist, 4),
        "keywords": vocab["keywords"],
        "optical_properties": optical,
        "strength": strength,
        "parameters": {p: round(params[p], 4) for p in TERPENE_PARAMETER_NAMES}
    }, indent=2)


@mcp.tool()
def map_terpene_parameters(
    terpene_id: str,
    intensity: str = "moderate",
    emphasis: str = "color_palette"
) -> str:
    """Map terpene state to visual parameters for image generation.

    Layer 2: Deterministic operation (0 tokens).

    Args:
        terpene_id: Canonical terpene ID (e.g. 'caryophyllene')
        intensity: subtle, moderate, or dramatic
        emphasis: color_palette, light_behavior, edge_character,
                  thermal_quality, or structural_form

    Returns:
        Complete parameter set for visual synthesis including
        vocabulary weighted by intensity and emphasis.
    """
    tid = terpene_id.lower().strip()
    if tid not in TERPENE_COORDS:
        return json.dumps({"error": f"Unknown: {tid}", "available": list(TERPENE_COORDS.keys())})

    params = TERPENE_COORDS[tid]
    vtype, vdist = _terpene_nearest_visual_type(params)
    vdata = TERPENE_VISUAL_TYPES[vtype]
    optical = TERPENE_OPTICAL_PROPERTIES.get(vtype, {})
    all_vocab = _terpene_select_vocabulary(params)

    intensity_weights = {"subtle": 0.6, "moderate": 1.0, "dramatic": 1.5}
    weight = intensity_weights.get(intensity, 1.0)

    # Primary emphasis category
    valid_cats = list(TERPENE_VOCABULARY.keys())
    primary_cat = emphasis if emphasis in valid_cats else "color_palette"
    primary_terms = all_vocab.get(primary_cat, [])

    return json.dumps({
        "terpene_id": tid,
        "terpene_name": TERPENES.get(tid, {}).get("name", tid),
        "intensity": intensity,
        "emphasis": emphasis,
        "weight": weight,
        "state": params,
        "nearest_visual_type": vtype,
        "visual_distance": round(vdist, 4),
        "optical_properties": optical,
        "primary_vocabulary": primary_terms,
        "full_vocabulary": all_vocab,
        "keywords": vdata["keywords"]
    }, indent=2)


@mcp.tool()
def generate_terpene_rhythmic_sequence(
    state_a_id: str,
    state_b_id: str,
    oscillation_pattern: str = "sinusoidal",
    num_cycles: int = 3,
    steps_per_cycle: int = 20,
    phase_offset: float = 0.0
) -> str:
    """Generate rhythmic oscillation between any two terpene states.

    Layer 2: Deterministic temporal composition (0 tokens).
    Unlike preset-based generation, this accepts arbitrary terpene pairs.

    Args:
        state_a_id: Starting terpene
        state_b_id: Alternating terpene
        oscillation_pattern: sinusoidal, triangular, or square
        num_cycles: Number of complete A→B→A cycles (1-10)
        steps_per_cycle: Samples per cycle (4-60)
        phase_offset: Starting phase (0.0=A, 0.5=B)

    Returns:
        Sequence with states, pattern info, and endpoint metadata.
    """
    aid = state_a_id.lower().strip()
    bid = state_b_id.lower().strip()
    if aid not in TERPENE_COORDS:
        return json.dumps({"error": f"Unknown: {aid}", "available": list(TERPENE_COORDS.keys())})
    if bid not in TERPENE_COORDS:
        return json.dumps({"error": f"Unknown: {bid}", "available": list(TERPENE_COORDS.keys())})
    if oscillation_pattern not in ("sinusoidal", "triangular", "square"):
        return json.dumps({"error": f"Unknown pattern: {oscillation_pattern}"})

    num_cycles = max(1, min(10, num_cycles))
    steps_per_cycle = max(4, min(60, steps_per_cycle))
    total_steps = num_cycles * steps_per_cycle

    config = {
        "state_a": aid,
        "state_b": bid,
        "pattern": oscillation_pattern,
        "num_cycles": num_cycles,
        "steps_per_cycle": steps_per_cycle
    }
    trajectory = _generate_preset_trajectory(config)

    # Apply phase offset by rotating trajectory
    if phase_offset > 0:
        offset_steps = int(phase_offset * steps_per_cycle) % total_steps
        trajectory = trajectory[offset_steps:] + trajectory[:offset_steps]

    dist = _terpene_euclidean_distance(TERPENE_COORDS[aid], TERPENE_COORDS[bid])

    # Sample 5 keyframes for preview
    indices = [0, total_steps // 4, total_steps // 2, 3 * total_steps // 4, total_steps - 1]
    keyframes = [{"step": i, "state": trajectory[i]} for i in indices if i < len(trajectory)]

    return json.dumps({
        "state_a": aid,
        "state_b": bid,
        "pattern": oscillation_pattern,
        "period": steps_per_cycle,
        "num_cycles": num_cycles,
        "total_steps": total_steps,
        "phase_offset": phase_offset,
        "endpoint_distance": round(dist, 4),
        "keyframes": keyframes,
        "trajectory": trajectory,
        "endpoint_visuals": {
            aid: TERPENES.get(aid, {}).get("visual_character", ""),
            bid: TERPENES.get(bid, {}).get("visual_character", "")
        }
    }, indent=2)


@mcp.tool()
def list_terpene_attractor_presets() -> str:
    """List all discovered and curated attractor presets for visualization.

    Phase 2.7 tool: Shows attractor configurations from Tier 4D
    multi-domain compositional limit cycle discovery.

    Returns:
        Preset catalog with names, basin sizes, classifications, and states.

    Cost: 0 tokens (deterministic lookup)
    """
    presets = []
    for aid, adata in TERPENE_ATTRACTOR_PRESETS.items():
        vtype, vdist = _terpene_nearest_visual_type(adata["state"])
        presets.append({
            "attractor_id": aid,
            "name": adata["name"],
            "description": adata["description"],
            "basin_size": adata["basin_size"],
            "classification": adata["classification"],
            "source_domains": adata["source_domains"],
            "nearest_visual_type": vtype,
            "visual_type_distance": round(vdist, 4),
            "state": adata["state"]
        })
    return json.dumps({
        "total_presets": len(presets),
        "presets": presets
    }, indent=2)


@mcp.tool()
def generate_terpene_attractor_prompt(
    attractor_id: str = "",
    custom_state: Optional[str] = None,
    mode: str = "composite",
    style_modifier: str = "",
    keyframe_count: int = 4
) -> str:
    """Generate image-generation prompt from attractor state or custom coordinates.

    Phase 2.7 tool: Translates mathematical attractor coordinates into
    visual prompts suitable for image generation (ComfyUI, Stable Diffusion, etc.).

    Modes:
        composite:  Single blended prompt from attractor state
        split_view: Separate prompt per visual type component
        sequence:   Multiple keyframe prompts for animation

    Args:
        attractor_id: Preset attractor name (period_30, volatile_burst, etc.)
            Leave empty and provide custom_state for arbitrary coordinates.
        custom_state: Optional JSON string with 5D parameter coordinates.
        mode: composite, split_view, or sequence
        style_modifier: Optional prefix (e.g. 'photorealistic', 'oil painting')
        keyframe_count: Number of keyframes for sequence mode (2-8)

    Returns:
        Dict with prompt(s), vocabulary details, and attractor metadata.

    Cost: 0 tokens (Layer 2 deterministic)
    """
    # Resolve parameters
    params = None
    attractor_meta = None

    if custom_state:
        try:
            params = json.loads(custom_state) if isinstance(custom_state, str) else custom_state
        except (json.JSONDecodeError, TypeError):
            return json.dumps({"error": "Could not parse custom_state as JSON"})
    elif attractor_id:
        aid = attractor_id.lower().strip()
        if aid in TERPENE_ATTRACTOR_PRESETS:
            attractor_meta = TERPENE_ATTRACTOR_PRESETS[aid]
            params = attractor_meta["state"]
        elif aid in TERPENE_COORDS:
            params = TERPENE_COORDS[aid]
        else:
            return json.dumps({
                "error": f"Unknown attractor/terpene: {aid}",
                "available_attractors": list(TERPENE_ATTRACTOR_PRESETS.keys()),
                "available_terpenes": list(TERPENE_COORDS.keys())
            })
    else:
        return json.dumps({"error": "Provide attractor_id or custom_state"})

    # Validate parameters
    missing = [p for p in TERPENE_PARAMETER_NAMES if p not in params]
    if missing:
        return json.dumps({"error": f"Missing parameters: {missing}"})

    # Extract vocabulary
    vocab = _extract_visual_vocabulary_from_terpene_params(params, strength=1.0)
    vtype, vdist = _terpene_nearest_visual_type(params)
    optical = TERPENE_OPTICAL_PROPERTIES.get(vtype, {})
    nearest_terp = _find_nearest_terpene(params)
    nearest_data = TERPENES.get(nearest_terp, {})

    style = style_modifier.strip()

    if mode == "composite":
        kw_str = ", ".join(vocab["keywords"])
        parts = []
        if style:
            parts.append(style)
        parts.append(kw_str)
        parts.append(
            f"inspired by {nearest_data.get('name', nearest_terp).lower()} "
            f"terpene aesthetic, {nearest_data.get('visual_character', '').lower()}"
        )
        prompt = ", ".join(parts)

        result = {
            "mode": "composite",
            "prompt": prompt,
            "vocabulary": {
                "visual_type": vtype,
                "keywords": vocab["keywords"],
                "type_distance": round(vdist, 4)
            },
            "optical_properties": optical,
            "nearest_terpene": nearest_terp,
            "parameters": {p: round(params[p], 4) for p in TERPENE_PARAMETER_NAMES}
        }
        if attractor_meta:
            result["attractor"] = {
                "name": attractor_meta["name"],
                "basin_size": attractor_meta["basin_size"],
                "classification": attractor_meta["classification"]
            }
        return json.dumps(result, indent=2)

    elif mode == "split_view":
        kw_str = ", ".join(vocab["keywords"])
        result = {
            "mode": "split_view",
            "domain": "terpene",
            "domain_prompt": f"{style + ', ' if style else ''}{kw_str}",
            "domain_context": (
                f"Terpene domain: {nearest_data.get('name', nearest_terp)} — "
                f"{nearest_data.get('visual_character', '')}. "
                f"{nearest_data.get('composition', '')}"
            ),
            "vocabulary": {
                "visual_type": vtype,
                "keywords": vocab["keywords"],
                "type_distance": round(vdist, 4)
            },
            "optical_properties": optical,
            "nearest_terpene": nearest_terp,
            "color_palette": nearest_data.get("color_specs", {}).get("primary_palette", ""),
            "parameters": {p: round(params[p], 4) for p in TERPENE_PARAMETER_NAMES}
        }
        if attractor_meta:
            result["attractor"] = {
                "name": attractor_meta["name"],
                "classification": attractor_meta["classification"]
            }
        return json.dumps(result, indent=2)

    elif mode == "sequence":
        keyframe_count = max(2, min(8, keyframe_count))
        keyframes = []

        # Build a mini trajectory radiating from attractor toward nearest terpene
        near_coords = TERPENE_COORDS[nearest_terp]
        for kf in range(keyframe_count):
            t = kf / max(1, keyframe_count - 1)
            # Oscillate: 0 → nearest → back to center
            if t <= 0.5:
                blend = t * 2  # 0→1 toward canonical
            else:
                blend = 2 * (1 - t)  # 1→0 back toward attractor

            kf_params = {
                p: params[p] * (1 - blend) + near_coords[p] * blend
                for p in TERPENE_PARAMETER_NAMES
            }
            kf_vocab = _extract_visual_vocabulary_from_terpene_params(kf_params, strength=0.9)
            kf_kw = ", ".join(kf_vocab["keywords"][:5])

            prompt = f"{style + ', ' if style else ''}{kf_kw}"
            if kf == 0:
                prompt += f", attractor center — {vtype}"
            elif blend > 0.8:
                prompt += f", pure {nearest_data.get('name', nearest_terp).lower()} character"

            keyframes.append({
                "keyframe": kf,
                "blend": round(blend, 3),
                "prompt": prompt,
                "visual_type": kf_vocab["nearest_type"],
                "parameters": {p: round(kf_params[p], 4) for p in TERPENE_PARAMETER_NAMES}
            })

        result = {
            "mode": "sequence",
            "keyframes": keyframes,
            "nearest_terpene": nearest_terp,
            "parameters": {p: round(params[p], 4) for p in TERPENE_PARAMETER_NAMES}
        }
        if attractor_meta:
            result["attractor"] = {
                "name": attractor_meta["name"],
                "classification": attractor_meta["classification"]
            }
        return json.dumps(result, indent=2)

    else:
        return json.dumps({"error": f"Unknown mode: {mode}. Use composite, split_view, or sequence."})


@mcp.tool()
def generate_terpene_sequence_prompts(
    preset_name: str,
    keyframe_count: int = 4,
    style_modifier: str = ""
) -> str:
    """Generate keyframe prompts from a Phase 2.6 rhythmic preset.

    Phase 2.7 tool: Extracts evenly-spaced keyframes from a rhythmic
    oscillation sequence and generates an image prompt for each.

    Useful for storyboard generation, animation keyframes, and
    multi-panel visualization of temporal terpene evolution.

    Args:
        preset_name: Phase 2.6 preset (volatility_wave, floral_drift, etc.)
        keyframe_count: Number of keyframes to extract (2-12, default 4)
        style_modifier: Optional style prefix for all prompts

    Returns:
        Dict with keyframes, each containing step, state, prompt, and vocabulary.

    Cost: 0 tokens (deterministic trajectory + vocabulary extraction)
    """
    pid = preset_name.lower().strip()
    if pid not in TERPENE_RHYTHMIC_PRESETS:
        return json.dumps({
            "error": f"Unknown preset: {pid}",
            "available": list(TERPENE_RHYTHMIC_PRESETS.keys())
        })

    keyframe_count = max(2, min(12, keyframe_count))
    config = TERPENE_RHYTHMIC_PRESETS[pid]
    trajectory = _generate_preset_trajectory(config)
    total = len(trajectory)

    indices = [int(i * (total - 1) / (keyframe_count - 1)) for i in range(keyframe_count)]
    style = style_modifier.strip()

    keyframes = []
    for kf_idx, traj_idx in enumerate(indices):
        state = trajectory[traj_idx]
        vocab = _extract_visual_vocabulary_from_terpene_params(state, strength=1.0)
        nearest = _find_nearest_terpene(state)
        nearest_data = TERPENES.get(nearest, {})

        kw_str = ", ".join(vocab["keywords"][:5])
        prompt = (
            f"{style + ', ' if style else ''}"
            f"{kw_str}, "
            f"{nearest_data.get('visual_character', '').lower()} terpene quality"
        )

        keyframes.append({
            "keyframe": kf_idx,
            "trajectory_step": traj_idx,
            "prompt": prompt,
            "visual_type": vocab["nearest_type"],
            "nearest_terpene": nearest,
            "parameters": {p: round(state[p], 4) for p in TERPENE_PARAMETER_NAMES}
        })

    return json.dumps({
        "preset": pid,
        "description": config["description"],
        "state_a": config["state_a"],
        "state_b": config["state_b"],
        "period": config["steps_per_cycle"],
        "total_trajectory_steps": total,
        "num_keyframes": keyframe_count,
        "keyframes": keyframes
    }, indent=2)


@mcp.tool()
def get_terpene_domain_registry_config() -> str:
    """Get complete domain configuration for emergent attractor discovery.

    Returns the data needed by domain_registry.py to integrate terpene
    aesthetics into the Tier 4D compositional limit cycle discovery system.
    Follows the ADDING_NEW_DOMAINS.md integration pattern.

    Returns:
        JSON with domain_id, parameter_names, state_coordinates, presets,
        vocabulary, periods, and attractor_presets.

    Cost: 0 tokens (deterministic extraction)
    """
    # Build presets in registry format
    registry_presets = {}
    for name, cfg in TERPENE_RHYTHMIC_PRESETS.items():
        registry_presets[name] = {
            "name": name,
            "period": cfg["steps_per_cycle"],
            "state_a_id": cfg["state_a"],
            "state_b_id": cfg["state_b"],
            "pattern": cfg["pattern"],
            "description": cfg["description"]
        }

    # Build vocabulary from visual types
    registry_vocab = {}
    for vtype, vdata in TERPENE_VISUAL_TYPES.items():
        registry_vocab[vtype] = vdata["keywords"]

    periods = sorted(set(
        cfg["steps_per_cycle"] for cfg in TERPENE_RHYTHMIC_PRESETS.values()
    ))

    return json.dumps({
        "domain_id": "terpene",
        "display_name": "Terpene Visual Vocabulary",
        "description": "Chemical aromatic compounds mapped to visual aesthetic parameters",
        "mcp_server": "terpene-vocabulary",
        "parameter_names": TERPENE_PARAMETER_NAMES,
        "state_coordinates": TERPENE_COORDS,
        "presets": registry_presets,
        "vocabulary": registry_vocab,
        "periods": periods,
        "attractor_presets": {
            aid: {
                "name": adata["name"],
                "basin_size": adata["basin_size"],
                "classification": adata["classification"],
                "state": adata["state"]
            }
            for aid, adata in TERPENE_ATTRACTOR_PRESETS.items()
        },
        "integration_notes": (
            f"Register via domain_registry.py using register_terpene_domain(). "
            f"All {len(TERPENE_COORDS)} terpene states available as canonical coordinates. "
            f"{len(TERPENE_RHYTHMIC_PRESETS)} rhythmic presets with periods {periods}. "
            f"{len(TERPENE_ATTRACTOR_PRESETS)} attractor presets (Tier 1-3)."
        ),
        "compatible_servers": [
            "catastrophe-morph-mcp",
            "diatom-morphology-mcp",
            "surface-design-aesthetics",
            "microscopy-aesthetics-mcp",
            "splash-aesthetics-mcp",
            "aesthetic-dynamics-core",
            "composition-graph-mcp"
        ],
        "domain_registry_ready": True,
        "phase": "2.7+tier4d"
    }, indent=2)


# ============================================================================

STRATEGIC_PATTERNS = {
    "volatility_persistence": {
        "high_volatility": {
            "pattern": r"\b(urgent|immediate|crisis|rapid|fast-moving|short-term|quick|fleeting|temporary|shifting)\b",
            "threshold": 4,
            "confidence": 0.80,
            "categorical_family": "constraints"
        },
        "low_volatility": {
            "pattern": r"\b(stable|long-term|enduring|sustained|permanent|continuous|persistent|ongoing|consistent|established)\b",
            "threshold": 3,
            "confidence": 0.75,
            "categorical_family": "constraints"
        }
    },
    "visual_character": {
        "radial_geometric": {
            "pattern": r"\b(centralized|hub|core|focal|center|radiating|emanating|single point|unified|convergent)\b",
            "threshold": 3,
            "confidence": 0.75,
            "categorical_family": "morphisms"
        },
        "flowing_organic": {
            "pattern": r"\b(fluid|adaptive|flexible|organic|evolving|dynamic|natural|flowing|continuous|gradual)\b",
            "threshold": 2,
            "confidence": 0.70,
            "categorical_family": "morphisms"
        },
        "interlocking_layered": {
            "pattern": r"\b(integrated|interconnected|layered|networked|multi-level|hierarchical|nested|complex|interdependent)\b",
            "threshold": 3,
            "confidence": 0.75,
            "categorical_family": "morphisms"
        }
    },
    "chemical_communication": {
        "attractant_broadcast": {
            "pattern": r"\b(attract|outreach|marketing|visibility|awareness|recruitment|growth|expansion|acquisition|invite)\b",
            "threshold": 3,
            "confidence": 0.80,
            "categorical_family": "objects"
        },
        "defensive_protective": {
            "pattern": r"\b(protect|defend|security|safeguard|mitigation|risk|prevention|shield|preserve|maintain)\b",
            "threshold": 3,
            "confidence": 0.75,
            "categorical_family": "objects"
        },
        "territorial": {
            "pattern": r"\b(competitive|position|market share|dominance|leadership|advantage|differentiation|unique|exclusive)\b",
            "threshold": 3,
            "confidence": 0.75,
            "categorical_family": "objects"
        }
    },
    "saturation_luminosity": {
        "high_intensity": {
            "pattern": r"\b(aggressive|bold|major|significant|substantial|large-scale|intensive|comprehensive|ambitious|transformative)\b",
            "threshold": 3,
            "confidence": 0.80,
            "categorical_family": "morphisms"
        },
        "low_intensity": {
            "pattern": r"\b(minimal|modest|incremental|gradual|measured|conservative|careful|cautious|limited|focused)\b",
            "threshold": 3,
            "confidence": 0.75,
            "categorical_family": "morphisms"
        }
    },
    "edge_quality": {
        "crisp_sharp": {
            "pattern": r"\b(clear|defined|specific|precise|explicit|distinct|unambiguous|exact|definitive|structured)\b",
            "threshold": 4,
            "confidence": 0.85,
            "categorical_family": "constraints"
        },
        "soft_blurred": {
            "pattern": r"\b(flexible|adaptable|evolving|exploratory|experimental|iterative|adjustable|fluid|ambiguous|open-ended)\b",
            "threshold": 3,
            "confidence": 0.75,
            "categorical_family": "constraints"
        }
    }
}


def detect_volatility_persistence(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect temporal stability patterns in strategy."""
    text_lower = text.lower()
    
    # High volatility
    high_vol_pattern = STRATEGIC_PATTERNS["volatility_persistence"]["high_volatility"]["pattern"]
    high_vol_matches = re.findall(high_vol_pattern, text_lower)
    if len(high_vol_matches) >= STRATEGIC_PATTERNS["volatility_persistence"]["high_volatility"]["threshold"]:
        return (
            "high_volatility",
            STRATEGIC_PATTERNS["volatility_persistence"]["high_volatility"]["confidence"],
            [f"High volatility indicators: {high_vol_matches[:5]}"]
        )
    
    # Low volatility
    low_vol_pattern = STRATEGIC_PATTERNS["volatility_persistence"]["low_volatility"]["pattern"]
    low_vol_matches = re.findall(low_vol_pattern, text_lower)
    if len(low_vol_matches) >= STRATEGIC_PATTERNS["volatility_persistence"]["low_volatility"]["threshold"]:
        return (
            "low_volatility",
            STRATEGIC_PATTERNS["volatility_persistence"]["low_volatility"]["confidence"],
            [f"Low volatility indicators: {low_vol_matches[:5]}"]
        )
    
    return None, 0.0, []


def detect_visual_character(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect structural organization patterns."""
    text_lower = text.lower()
    
    # Radial geometric
    radial_pattern = STRATEGIC_PATTERNS["visual_character"]["radial_geometric"]["pattern"]
    radial_matches = re.findall(radial_pattern, text_lower)
    if len(radial_matches) >= STRATEGIC_PATTERNS["visual_character"]["radial_geometric"]["threshold"]:
        return (
            "radial_geometric",
            STRATEGIC_PATTERNS["visual_character"]["radial_geometric"]["confidence"],
            [f"Radial organization: {radial_matches[:5]}"]
        )
    
    # Flowing organic
    flowing_pattern = STRATEGIC_PATTERNS["visual_character"]["flowing_organic"]["pattern"]
    flowing_matches = re.findall(flowing_pattern, text_lower)
    if len(flowing_matches) >= STRATEGIC_PATTERNS["visual_character"]["flowing_organic"]["threshold"]:
        return (
            "flowing_organic",
            STRATEGIC_PATTERNS["visual_character"]["flowing_organic"]["confidence"],
            [f"Flowing organization: {flowing_matches[:5]}"]
        )
    
    # Interlocking layered
    interlock_pattern = STRATEGIC_PATTERNS["visual_character"]["interlocking_layered"]["pattern"]
    interlock_matches = re.findall(interlock_pattern, text_lower)
    if len(interlock_matches) >= STRATEGIC_PATTERNS["visual_character"]["interlocking_layered"]["threshold"]:
        return (
            "interlocking_layered",
            STRATEGIC_PATTERNS["visual_character"]["interlocking_layered"]["confidence"],
            [f"Interlocking organization: {interlock_matches[:5]}"]
        )
    
    return None, 0.0, []


def detect_chemical_communication(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect strategic intent patterns."""
    text_lower = text.lower()
    
    # Attractant broadcast
    attract_pattern = STRATEGIC_PATTERNS["chemical_communication"]["attractant_broadcast"]["pattern"]
    attract_matches = re.findall(attract_pattern, text_lower)
    if len(attract_matches) >= STRATEGIC_PATTERNS["chemical_communication"]["attractant_broadcast"]["threshold"]:
        return (
            "attractant_broadcast",
            STRATEGIC_PATTERNS["chemical_communication"]["attractant_broadcast"]["confidence"],
            [f"Attractant intent: {attract_matches[:5]}"]
        )
    
    # Defensive protective
    defensive_pattern = STRATEGIC_PATTERNS["chemical_communication"]["defensive_protective"]["pattern"]
    defensive_matches = re.findall(defensive_pattern, text_lower)
    if len(defensive_matches) >= STRATEGIC_PATTERNS["chemical_communication"]["defensive_protective"]["threshold"]:
        return (
            "defensive_protective",
            STRATEGIC_PATTERNS["chemical_communication"]["defensive_protective"]["confidence"],
            [f"Defensive intent: {defensive_matches[:5]}"]
        )
    
    # Territorial
    territorial_pattern = STRATEGIC_PATTERNS["chemical_communication"]["territorial"]["pattern"]
    territorial_matches = re.findall(territorial_pattern, text_lower)
    if len(territorial_matches) >= STRATEGIC_PATTERNS["chemical_communication"]["territorial"]["threshold"]:
        return (
            "territorial",
            STRATEGIC_PATTERNS["chemical_communication"]["territorial"]["confidence"],
            [f"Territorial intent: {territorial_matches[:5]}"]
        )
    
    return None, 0.0, []


def detect_saturation_luminosity(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect resource intensity patterns."""
    text_lower = text.lower()
    
    # High intensity
    high_intensity_pattern = STRATEGIC_PATTERNS["saturation_luminosity"]["high_intensity"]["pattern"]
    high_intensity_matches = re.findall(high_intensity_pattern, text_lower)
    if len(high_intensity_matches) >= STRATEGIC_PATTERNS["saturation_luminosity"]["high_intensity"]["threshold"]:
        return (
            "high_intensity",
            STRATEGIC_PATTERNS["saturation_luminosity"]["high_intensity"]["confidence"],
            [f"High resource intensity: {high_intensity_matches[:5]}"]
        )
    
    # Low intensity
    low_intensity_pattern = STRATEGIC_PATTERNS["saturation_luminosity"]["low_intensity"]["pattern"]
    low_intensity_matches = re.findall(low_intensity_pattern, text_lower)
    if len(low_intensity_matches) >= STRATEGIC_PATTERNS["saturation_luminosity"]["low_intensity"]["threshold"]:
        return (
            "low_intensity",
            STRATEGIC_PATTERNS["saturation_luminosity"]["low_intensity"]["confidence"],
            [f"Low resource intensity: {low_intensity_matches[:5]}"]
        )
    
    return None, 0.0, []


def detect_edge_quality(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect execution clarity patterns."""
    text_lower = text.lower()
    
    # Crisp sharp
    crisp_pattern = STRATEGIC_PATTERNS["edge_quality"]["crisp_sharp"]["pattern"]
    crisp_matches = re.findall(crisp_pattern, text_lower)
    if len(crisp_matches) >= STRATEGIC_PATTERNS["edge_quality"]["crisp_sharp"]["threshold"]:
        return (
            "crisp_sharp",
            STRATEGIC_PATTERNS["edge_quality"]["crisp_sharp"]["confidence"],
            [f"Crisp execution clarity: {crisp_matches[:5]}"]
        )
    
    # Soft blurred
    soft_pattern = STRATEGIC_PATTERNS["edge_quality"]["soft_blurred"]["pattern"]
    soft_matches = re.findall(soft_pattern, text_lower)
    if len(soft_matches) >= STRATEGIC_PATTERNS["edge_quality"]["soft_blurred"]["threshold"]:
        return (
            "soft_blurred",
            STRATEGIC_PATTERNS["edge_quality"]["soft_blurred"]["confidence"],
            [f"Soft execution boundaries: {soft_matches[:5]}"]
        )
    
    return None, 0.0, []


def analyze_strategy_document(strategy_text: str) -> Dict[str, Any]:
    """
    Analyze strategy document through terpene aesthetic dimensions.
    
    Pure Layer 2 deterministic pattern matching - zero LLM cost.
    
    Maps:
    - Volatility/Persistence → Strategic timeline stability
    - Visual Character → Organizational architecture
    - Chemical Communication → Strategic intent/positioning  
    - Saturation/Luminosity → Resource investment level
    - Edge Quality → Execution clarity/role definition
    """
    findings = []
    
    # Run all 5 detectors
    detectors = [
        ("volatility_persistence", detect_volatility_persistence),
        ("visual_character", detect_visual_character),
        ("chemical_communication", detect_chemical_communication),
        ("saturation_luminosity", detect_saturation_luminosity),
        ("edge_quality", detect_edge_quality)
    ]
    
    for dimension_name, detector_func in detectors:
        pattern, confidence, evidence = detector_func(strategy_text)
        if pattern:
            # Get categorical family from pattern
            if dimension_name == "volatility_persistence":
                cat_family = STRATEGIC_PATTERNS["volatility_persistence"][pattern]["categorical_family"]
            elif dimension_name == "visual_character":
                cat_family = STRATEGIC_PATTERNS["visual_character"][pattern]["categorical_family"]
            elif dimension_name == "chemical_communication":
                cat_family = STRATEGIC_PATTERNS["chemical_communication"][pattern]["categorical_family"]
            elif dimension_name == "saturation_luminosity":
                cat_family = STRATEGIC_PATTERNS["saturation_luminosity"][pattern]["categorical_family"]
            else:  # edge_quality
                cat_family = STRATEGIC_PATTERNS["edge_quality"][pattern]["categorical_family"]
            
            findings.append({
                "dimension": dimension_name,
                "pattern": pattern,
                "confidence": confidence,
                "evidence": evidence,
                "categorical_family": cat_family
            })
    
    return {
        "domain": "terpene_mcp",
        "findings": findings,
        "total_findings": len(findings),
        "methodology": "deterministic_pattern_matching",
        "llm_cost_tokens": 0
    }


@mcp.tool()
def analyze_strategy_document_tool(strategy_text: str) -> str:
    """
    Analyze a strategy document through terpene aesthetic dimensions.
    
    This is the tomographic domain projection tool - it projects strategic
    text through terpene vocabulary to detect structural patterns.
    
    Zero LLM cost - pure deterministic pattern matching.
    
    Args:
        strategy_text: Full text of the strategy document to analyze
    
    Returns:
        JSON string with findings format:
        {
            "domain": "terpene_mcp",
            "findings": [
                {
                    "dimension": "volatility_persistence",
                    "pattern": "high_volatility",
                    "confidence": 0.80,
                    "evidence": ["High volatility indicators: ['urgent', 'immediate', ...]"],
                    "categorical_family": "constraints"
                },
                ...
            ],
            "total_findings": 3,
            "methodology": "deterministic_pattern_matching",
            "llm_cost_tokens": 0
        }
    
    Example:
        >>> result = analyze_strategy_document_tool(strategy_pdf_text)
        >>> findings = json.loads(result)["findings"]
    
    Cost: 0 tokens (deterministic pattern matching)
    """
    result = analyze_strategy_document(strategy_text)
    return json.dumps(result, indent=2)

# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    mcp.run()
