"""
Terpene Visual Vocabulary MCP Server

Deterministic mapping of terpene compounds to visual parameters for image generation.
This server handles all taxonomy lookups and parameter mapping - no LLM tokens required.

The server provides:
- Terpene metadata (smell profiles, visual character, color palettes)
- Temporal stage modifiers (Fresh, Active, Fading, Traces)
- Master prompts (complete terpene descriptors)
- Intensity parameter handling
- Multi-terpene composition rules
"""

from fastmcp import FastMCP
from typing import Optional, Literal
import json

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

if __name__ == "__main__":
    mcp.run()
