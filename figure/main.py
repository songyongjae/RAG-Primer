import os
from model import get_pie_chart

def TASK_2():
    print('='*80, '\nTask 2', '\n' + '='*80)

    API_KEY = "YOUR_OPENAI_API_KEY"  # Replace with your API key
    legends_pie = [
        "Automotive Sales",
        "Services and Other",
        "Energy Generation and Storage",
        "Automotive Leasing",
        "Automotive Regulatory Credits"
    ]

    # 현재 실행 위치 기준으로 source 디렉토리로의 절대 경로 생성
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.abspath(os.path.join(base_dir, "../source/main_tsla-20231231/ITEM 7."))

    pie_chart_generator = get_pie_chart(API_KEY, legends_pie, directory, "tsla")
    pie_chart_generator.generate_pie_chart()

if __name__ == "__main__":
    TASK_2()
