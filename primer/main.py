import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from primer.text import get_overview
from primer.numeric import get_finance_value
from primer.model import get_primer

def TASK_3():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    paths_overview = [
        os.path.abspath(os.path.join(base_dir, "../source/main_tsla-20231231/ITEM 1.")),
        os.path.abspath(os.path.join(base_dir, "../source/main_tsla-20231231/ITEM 1A."))
    ]
    text_processor = get_overview()
    subtitle, overview_content = text_processor.generate_abstract(paths_overview)

    main_paths = [os.path.abspath(os.path.join(base_dir, "../source/main_tsla-20231231/ITEM 7."))]
    sub_paths = [os.path.abspath(os.path.join(base_dir, "../source/sub_tsla-20221231/ITEM 7."))]
    tabular_processor = get_finance_value()
    finance_content = tabular_processor.generate_tabular(main_paths, sub_paths)

    pie_chart_path = os.path.abspath(os.path.join(base_dir, "../figure/segment_performance_tsla.png"))

    primer = get_primer(subtitle, overview_content, finance_content, pie_chart_path, "tsla")
    primer.generate_primer_png()
    img = mpimg.imread('./tsla-primer-report.png')
    plt.figure(figsize=(16, 12))
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
if __name__ == "__main__":
    TASK_3()
