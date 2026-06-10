import hashlib
from pathlib import Path
from src.database.database import init_db, register_document

def seed():
    init_db()
    storage_dir = Path("data/pdfs")
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    # Files we simulated earlier
    files = [
        ("MRV", "MRV_Relatorio_3T25.pdf"),
        ("Cyrela", "Cyrela_Previa_3T25.pdf"),
        ("Cury", "Cury_Resultados_3T25.pdf"),
    ]
    
    # Path to the example file to use as a base
    example_path = Path("exemplo_Boletim_Conjuntura_2025_3T.pdf")
    
    if not example_path.exists():
        print("Error: exemplo_Boletim_Conjuntura_2025_3T.pdf not found!")
        return

    for company, filename in files:
        dest_path = storage_dir / filename
        # Copy example file to simulate a downloaded PDF
        import shutil
        shutil.copy(example_path, dest_path)
        
        # Calculate hash of the content to register in DB
        with open(dest_path, "rb") as f:
            content = f.read()
            file_hash = hashlib.sha256(content).hexdigest()
        
        # Register as a new pending document
        doc_id = register_document(company, f"simulated_url_{filename}", file_hash, filename)
        print(f"Registered {filename} for {company} (ID: {doc_id})")

if __name__ == "__main__":
    seed()
    print("\nDatabase seeded! Now run 'python run_pipeline.py' to process them.")
