from primer.financial_data_reader import read_documents
from primer.financial_analysis import analyze_financials
from primer.financial_merger import merge_financial_data, find_missing_values

class FinancialManager:
    def __init__(self):
        self.merged_data = {}

    def handle_financial_data(self, main_paths, sub_paths):
        documents_main = read_documents(main_paths, ['ITEM 7.'])
        documents_sub = read_documents(sub_paths, ['ITEM 7.'])

        data_main = analyze_financials(documents_main, ["2022", "2023"])
        data_sub = analyze_financials(documents_sub, ["2021", "2022"])

        self.merged_data = merge_financial_data(self.merged_data, data_main, data_sub)

        missing_values = find_missing_values(self.merged_data)
        print("Missing values:", missing_values)

        return self.merged_data
