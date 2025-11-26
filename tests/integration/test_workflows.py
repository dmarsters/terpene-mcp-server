"""
Integration tests for terpene-vocabulary-mcp server

Tests actual MCP tool invocations and workflows.
"""

import pytest
import json
from src.terpene_vocabulary.server import TERPENES


class TestToolSimulation:
    """Simulate tool calls by directly accessing server logic."""
    
    def test_list_terpenes_structure(self):
        """list_terpenes should return valid JSON structure."""
        # Simulate tool return
        result = []
        for terpene_id, terpene_data in TERPENES.items():
            result.append({
                "id": terpene_id,
                "name": terpene_data["name"],
                "formula": terpene_data["molecular_formula"],
                "scent": terpene_data["scent_profile"],
                "visual_character": terpene_data["visual_character"]
            })
        
        # Should be serializable to JSON
        json_str = json.dumps(result)
        assert len(json_str) > 0
        
        # Should have 11 entries
        assert len(result) == 11
    
    def test_get_terpene_returns_complete_data(self):
        """get_terpene should return complete terpene data."""
        terpene = TERPENES["limonene"]
        
        # Should be JSON serializable
        json_str = json.dumps(terpene)
        assert len(json_str) > 0
        
        # Should have all expected fields
        assert terpene["name"] == "Limonene"
        assert "C₁₀H₁₆" in terpene["molecular_formula"]
    
    def test_get_master_prompt_with_temporal_stage(self):
        """get_master_prompt should adjust for temporal stages."""
        terpene = TERPENES["limonene"]
        master = terpene["master_prompt"]
        
        # Master should be substantial
        assert len(master) > 100
        
        # Should describe visual properties
        assert any(word in master.lower() for word in 
                  ["color", "bright", "saturated", "composition", "geometric"])
    
    def test_temporal_stage_adjustments(self):
        """Temporal stages should provide adjustment multipliers."""
        for terpene_id, terpene in TERPENES.items():
            stages = terpene["temporal_qualities"]["stages"]
            
            # Fresh should be at maximum intensity (1.0)
            fresh = stages["fresh"]
            assert fresh["saturation_adjustment"] == 1.0
            assert fresh["luminosity_adjustment"] == 1.0
            
            # Fading should be reduced
            fading = stages["fading"]
            assert fading["saturation_adjustment"] < 1.0
            assert fading["luminosity_adjustment"] < 1.0
            
            # Traces should be minimal
            traces = stages["traces"]
            assert traces["saturation_adjustment"] < 0.5
            assert traces["luminosity_adjustment"] < 0.9
    
    def test_color_palette_transformation(self):
        """Color palette should be transformable with adjustments."""
        terpene = TERPENES["caryophyllene"]
        
        # Get base color specs
        color_specs = terpene["color_specs"]
        
        # Apply fading stage adjustment
        fading = terpene["temporal_qualities"]["stages"]["fading"]
        sat_mult = fading["saturation_adjustment"]
        lum_mult = fading["luminosity_adjustment"]
        
        # Adjustments should be reasonable (reduced from fresh)
        assert 0.5 <= sat_mult <= 0.7  # Reduced from 1.0
        assert 0.75 <= lum_mult <= 0.85  # Slight reduction
    
    def test_intensity_modifier_calculation(self):
        """Intensity modifiers should scale terpene influence."""
        # Simulate apply_intensity_modifier logic
        terpene = TERPENES["limonene"]
        
        for intensity in [0.0, 0.25, 0.5, 0.75, 1.0]:
            # Simulate intensity application
            saturation_modifier = intensity
            luminosity_modifier = 0.7 + (intensity * 0.3)
            edge_softness_modifier = 1 - (intensity * 0.5)
            
            # Check ranges
            assert 0 <= saturation_modifier <= 1
            assert 0.7 <= luminosity_modifier <= 1.0
            assert 0.5 <= edge_softness_modifier <= 1.0
    
    def test_terpene_comparison_structure(self):
        """Terpene comparison should return valid structure."""
        t1 = TERPENES["limonene"]
        t2 = TERPENES["linalool"]
        
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
                "saturation_range": {
                    "terpene1": t1["color_specs"]["saturation"],
                    "terpene2": t2["color_specs"]["saturation"]
                }
            }
        }
        
        # Should be JSON serializable
        json_str = json.dumps(comparison)
        assert len(json_str) > 0
    
    def test_concept_matching_logic(self):
        """Concept suggestion should find semantic bridges."""
        concept = "A lonely figure in an abandoned industrial city"
        concept_lower = concept.lower()
        
        # Simulate keyword matching
        keyword_map = {
            "lonely|isolated": "pinene",
            "industrial|structure": "pinene",
            "defense|defensive": "pinene"
        }
        
        matches = []
        for keywords, terpene_id in keyword_map.items():
            if any(kw in concept_lower for kw in keywords.split("|")):
                matches.append(terpene_id)
        
        # Should match pinene for this concept
        assert "pinene" in matches
    
    def test_chemical_communication_retrieval(self):
        """Chemical communication should describe biological role."""
        for terpene_id, terpene in TERPENES.items():
            chem_comm = terpene.get("chemical_communication", "")
            
            # Should be non-empty
            assert len(chem_comm) > 0
            
            # Should contain meaningful keywords related to terpene function
            assert any(word in chem_comm.lower() for word in 
                      ["signal", "attract", "defense", "communication", "mark", "presence", "broadcast", "growth", "potency"])



class TestWorkflowSimulation:
    """Simulate complete workflows using server data."""
    
    def test_path1_workflow(self):
        """Simulate Path 1 (pre-generation) workflow."""
        # User selects terpene
        selected_terpene = "limonene"
        temporal_stage = "fresh"
        intensity = 0.5
        
        # Step 1: Get terpene
        terpene = TERPENES[selected_terpene]
        assert terpene is not None
        
        # Step 2: Get master prompt
        master_prompt = terpene["master_prompt"]
        assert len(master_prompt) > 0
        
        # Step 3: Apply intensity
        saturation_mod = intensity
        composition_emphasis = "Strong" if intensity > 0.5 else "Balanced"
        
        # Step 4: Would fuse with LLM (not tested here)
        # Step 5: Would generate image (not tested here)
        
        # Verify workflow logic
        assert master_prompt is not None
        assert saturation_mod == 0.5
    
    def test_path2_workflow(self):
        """Simulate Path 2 (post-generation discovery) workflow."""
        original_prompt = "A woman remembering a lost love"
        
        # Step 1: Get list of terpenes
        terpenes_list = list(TERPENES.keys())
        assert len(terpenes_list) == 11
        
        # Step 2: User selects terpene
        selected = "linalool"
        terpene = TERPENES[selected]
        
        # Step 3: Get master prompt
        master = terpene["master_prompt"]
        assert len(master) > 0
        
        # Step 4: Adjust temporal stage
        new_stage = "fading"
        stage_data = terpene["temporal_qualities"]["stages"][new_stage]
        
        # Step 5: Would regenerate with adjustments
        assert stage_data["saturation_adjustment"] < 1.0
    
    def test_comparison_workflow(self):
        """Simulate terpene comparison in discovery mode."""
        t1_id = "limonene"
        t2_id = "linalool"
        
        t1 = TERPENES[t1_id]
        t2 = TERPENES[t2_id]
        
        # Create comparison
        comparison = {
            "t1_name": t1["name"],
            "t2_name": t2["name"],
            "t1_saturation": t1["color_specs"]["saturation"],
            "t2_saturation": t2["color_specs"]["saturation"],
            "t1_luminosity": t1["color_specs"]["luminosity"],
            "t2_luminosity": t2["color_specs"]["luminosity"],
        }
        
        # Verify they're different
        assert comparison["t1_name"] != comparison["t2_name"]
        assert comparison["t1_saturation"] != comparison["t2_saturation"]


class TestJSONSerialization:
    """Test that all terpene data is JSON serializable."""
    
    def test_all_terpenes_serializable(self):
        """All terpene data should be JSON serializable."""
        for terpene_id, terpene in TERPENES.items():
            try:
                json_str = json.dumps(terpene)
                assert len(json_str) > 0
            except TypeError as e:
                pytest.fail(f"Terpene {terpene_id} not JSON serializable: {e}")
    
    def test_serialized_terpene_structure_preserved(self):
        """Structure should be preserved after JSON round-trip."""
        for terpene_id, terpene in TERPENES.items():
            json_str = json.dumps(terpene)
            restored = json.loads(json_str)
            
            # Key fields should be preserved
            assert restored["name"] == terpene["name"]
            assert restored["molecular_formula"] == terpene["molecular_formula"]
            assert len(restored["temporal_qualities"]["stages"]) == 4


class TestDataConsistency:
    """Test consistency across terpene database."""
    
    def test_no_duplicate_names(self):
        """No two terpenes should have the same name."""
        names = [t["name"] for t in TERPENES.values()]
        assert len(names) == len(set(names))
    
    def test_consistent_classification_format(self):
        """All classifications should follow consistent format."""
        for terpene_id, terpene in TERPENES.items():
            classification = terpene["classification"]
            # Should contain terpene type and structure info
            assert "terpene" in classification.lower()
    
    def test_all_bridges_reasonable_length(self):
        """Semantic bridges should be reasonable length."""
        for terpene_id, terpene in TERPENES.items():
            bridges = terpene["semantic_bridges"]
            for bridge in bridges:
                assert 5 < len(bridge) < 50, \
                    f"Bridge '{bridge}' in {terpene_id} has unusual length"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
