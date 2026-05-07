import os

def read_clinical_report(filename: str):
    """
    Reads and parses clinical guidelines or unstructured reports from the data directory.
    """
    # Use path relative to the app directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, "../../data/")
    file_path = os.path.normpath(os.path.join(base_path, filename))
    
    if not os.path.exists(file_path):
        return {"error": f"Report '{filename}' not found at {file_path}"}
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        return {"error": str(e)}
