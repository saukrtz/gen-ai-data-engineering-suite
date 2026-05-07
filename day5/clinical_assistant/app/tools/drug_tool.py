def check_drug_safety(drug_name: str):
    """
    Checks drug safety and interactions. 
    In a production system, this would call an external Pharmacopeia API.
    """
    # Mock data for demonstration
    drug_db = {
        "lisinopril": {
            "status": "Safe",
            "interactions": ["Potassium supplements", "NSAIDs"],
            "notes": "Monitor kidney function."
        },
        "metformin": {
            "status": "Safe",
            "interactions": ["Contrast dye", "Alcohol"],
            "notes": "Take with meals to reduce GI side effects."
        },
        "warfarin": {
            "status": "Caution",
            "interactions": ["Leafy greens", "Aspirin"],
            "notes": "Requires frequent INR monitoring."
        }
    }
    
    drug_info = drug_db.get(drug_name.lower())
    if drug_info:
        return {"drug": drug_name, "info": drug_info}
    else:
        return {"drug": drug_name, "info": "No specific interaction data found. Please consult standard clinical guidelines."}
