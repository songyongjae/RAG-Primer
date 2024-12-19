from pie_chart_analyzer.analyzer import get_pie_chart
from pie_chart_analyzer.config import API_KEY, LEGENDS, DATASET_DIR

def TASK_2():
    print("=" * 80, "\nTask 2")
    print("=" * 80)

    ticker = "tsla"
    analyzer = get_pie_chart(API_KEY, LEGENDS, DATASET_DIR, ticker)
    analyzer.generate_pie_chart()

if __name__ == "__main__":
    TASK_2()
