from source.model import ChunkProcessor
from source.config import RESOURCES_DIR, MODEL_NAME, PCA_COMPONENTS, DBSCAN_EPS, DBSCAN_MIN_SAMPLES
from primer.model import get_overview, get_finance_value, get_primer
from figure.model import get_pie_chart
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from tqdm import tqdm

def TASK_4():
    ge_data = [
        {"ticker": "ge", "fiscal_year": 20231231},
        {"ticker": "ge", "fiscal_year": 20221231}
    ]
    processor = ChunkProcessor(RESOURCES_DIR, MODEL_NAME, PCA_COMPONENTS, DBSCAN_EPS, DBSCAN_MIN_SAMPLES)
    for ge in tqdm(ge_data, desc="Processing Files"):
        results = processor.process_file([ge])

if __name__ == "__main__":
    print('='*80, '\nTask 4')
    print('='*80)

    legends_pie = [
        "Aerospace and Defense Systems",
        "Renewable Energy Solutions",
        "Automotive Sales",
        "Automotive Leasing",
        "Power Generation Technologies"
    ]

    directory = os.path.abspath("./chunk_ge-20231231/ITEM 7.")

    API_KEY = "your_api_key_here"  # Ensure to replace with the actual API key
    pie_chart_png = get_pie_chart(API_KEY, legends_pie, directory, 'ge')
    pie_chart_png.generate_pie_chart()

    print('='*80, '\nGE Primer')
    print('='*80)
    paths_overview = [
        os.path.abspath('./chunk_ge-20231231/ITEM 1.'),
        os.path.abspath('./chunk_ge-20231231/ITEM 1A.')
    ]

    text_processor = get_overview()
    subtitle, overview_content = text_processor.generate_abstract(paths_overview)

    main_paths = [os.path.abspath('./chunk_ge-20231231/ITEM 7.')]
    sub_paths = [os.path.abspath('./chunk_ge-20221231/ITEM 7.')]

    tabular_processor = get_finance_value()
    finance_content = tabular_processor.generate_tabular(main_paths, sub_paths)

    pie_chart_path = os.path.abspath('../figure/segment_performance_ge.png')

    primer = get_primer(subtitle, overview_content, finance_content, pie_chart_path, 'ge')
    primer.generate_primer_png()
    img = mpimg.imread('./ge-primer-report.png')
    plt.figure(figsize=(16, 12))
    plt.imshow(img)
    plt.axis('off')
    plt.show()