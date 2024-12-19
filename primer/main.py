from primer.overview_analyzer import get_overview
from primer.financial_manager import FinancialManager
from primer.markdown_generator import generate_markdown
from primer.html_generator import generate_html
from primer.png_converter import html_to_png
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def TASK_3():
    """
    Task 3: Generate a financial primer and display the resulting PNG.
    """
    print("=" * 80, "\nTask 3")
    print("=" * 80)

    # Step 1: Generate overview
    overview_paths = ['./main_tsla-20231231/ITEM 1.', './main_tsla-20231231/ITEM 1A.']
    overview_processor = get_overview()
    subtitle, overview_content = overview_processor.generate_abstract(overview_paths)

    # Step 2: Generate financial data
    main_paths = ['./main_tsla-20231231/ITEM 7.']
    sub_paths = ['./sub_tsla-20221231/ITEM 7.']
    financial_manager = FinancialManager()
    finance_content = financial_manager.handle_financial_data(main_paths, sub_paths)

    # Step 3: Generate Markdown content
    pie_chart_path = './segment_performance_tsla.png'
    markdown_content = generate_markdown(subtitle, overview_content, finance_content, pie_chart_path, 'tsla')

    # Step 4: Generate HTML content
    html_content = generate_html(markdown_content, 'tsla', pie_chart_path)
    html_file = './tsla_primer_report.html'
    with open(html_file, 'w') as f:
        f.write(html_content)

    # Step 5: Convert HTML to PNG
    png_file = './tsla-primer-report.png'
    html_to_png(html_file, png_file)

    # Step 6: Display the generated PNG
    img = mpimg.imread(png_file)
    plt.figure(figsize=(16, 12))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    TASK_3()
