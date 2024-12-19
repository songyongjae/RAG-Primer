from robustness.html_loader import load_html_file
from robustness.section_extractor import extract_sections
from robustness.chunk_processor import process_section
from robustness.chunk_categorizer import categorize_chunks
from sentence_transformers import SentenceTransformer
import os

def TASK_4():
    """
    Task 4: Process a 10-K document into categorized chunks and generate a financial primer.
    """
    print("=" * 80, "\nTask 4")
    print("=" * 80)

    resources_dir = "datasets"
    ticker = "ge"
    fiscal_year = 20231231
    output_dir = f"chunk_{ticker}-{fiscal_year}"
    os.makedirs(output_dir, exist_ok=True)

    file_path = f"{resources_dir}/{ticker.lower()}-{fiscal_year}.html"
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Step 1: Load HTML content
    document_text = load_html_file(file_path)

    # Step 2: Extract sections
    sections = extract_sections(document_text, model)

    # Step 3: Process sections into chunks
    chunk_files = []
    for section_name, content in sections.items():
        section_result = process_section(ticker, fiscal_year, section_name, content, output_dir)
        chunk_files.extend(section_result["chunk_files"])

    # Step 4: Categorize chunks into sections
    keywords = {
        "ITEM 1.": "Description of Business",
        "ITEM 1A.": "Risk Factors",
        "ITEM 7.": "Management's Discussion and Analysis of Financial Condition and Results of Operations"
    }
    categorize_chunks(chunk_files, output_dir, model, keywords)

if __name__ == "__main__":
    TASK_4()
