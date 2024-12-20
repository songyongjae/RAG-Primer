import os
import json
import openai

class get_finance_value:
    def __init__(self):
        self.merged_data = {}

    def read_documents(self, folder_paths, filter_items):
        """
        Reads JSON files from the specified folder paths and filters them by the filter_items.
        """
        documents = []
        for folder_path in folder_paths:
            print(f"Checking folder path: {folder_path}")
            if os.path.isdir(folder_path):
                files = os.listdir(folder_path)
                for file in files:
                    if file.endswith('.json') and any(item.lower() in file.lower() for item in filter_items):
                        file_path = os.path.join(folder_path, file)
                        try:
                            with open(file_path, 'r') as f:
                                content = json.load(f)
                                if 'chunk' not in content:
                                    print(f"Warning: 'chunk' key missing in {file}")
                                documents.append(content)
                        except Exception as e:
                            print(f"Error loading file {file}: {e}")
            else:
                print(f"Error: Folder path {folder_path} does not exist.")
        return documents

    def analyze_financials(self, documents, prompt_years):
        """
        Extract financial data for specific years from GPT's response.
        """
        all_content = "\n\n".join([doc.get('chunk', '') for doc in documents])

        if not all_content.strip():
            print("Error: No content provided to GPT for analysis.")
            return {}

        prompt = f"""
        You are a financial analyst. Based on the following content from chunks, extract financial metrics for the years {', '.join(prompt_years)}.
        - For ranges (e.g., "$8.00 to $10.00 billion"), calculate the average value.
        - If specific values for some years are missing, infer trends or use "N/A" if absolutely necessary.
        - Calculate YoY (Year-over-Year) percentage changes for Revenue.
        - Calculate margin percentages for Gross Profit, Operating Profit, and Net Profit where applicable.

        Instructions:
        1. Strictly return the output in JSON format.
        2. Do not include any additional explanations or commentary.
        3. Assume all dollar values are in billions unless stated otherwise.

        Example JSON format:
        {{
            "Revenue": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }},
            "Revenue's % yoy": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }},
            "Gross Profit": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }},
            "Gross Profit's % margin": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }},
            "Operating Profit": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }},
            "Operating Profit's % margin": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }},
            "Net Profit": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }},
            "Net Profit's % margin": {{ {', '.join(f'"{year}": <value>' for year in prompt_years)} }}
        }}

        Filtered Content:
        {all_content}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert Financial assistant."},
                    {"role": "user", "content": prompt}
                ],
            )
            content = response['choices'][0]['message']['content'].strip()

            # Attempt to parse JSON, but fallback gracefully if it fails
            try:
                response_json = json.loads(content)
                return response_json
            except json.JSONDecodeError:
                print("Warning: JSON decoding failed. Attempting partial parsing.")

                # Extract only JSON-like substrings and return partial results
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    json_like_content = content[start_idx:end_idx + 1]
                    try:
                        partial_response_json = json.loads(json_like_content)
                        return partial_response_json
                    except json.JSONDecodeError:
                        print("Error: Unable to parse JSON-like content. Returning empty result.")
                else:
                    print("Error: No valid JSON structure detected.")
                return {}
        except Exception as e:
            print(f"Unexpected GPT API error: {e}")
            return {}

    def merge_financial_data(self, main_data, sub_data):
        """
        Merge financial data by averaging values for overlapping years.
        Track the number of updates for each cell to calculate the final average correctly.
        """
        all_keys = set(main_data.keys()).union(sub_data.keys())

        for key in all_keys:
            main_values = main_data.get(key, {})
            sub_values = sub_data.get(key, {})

            if key not in self.merged_data:
                self.merged_data[key] = {}  # Initialize merged data for this key
                self.merged_data[key]['update_count'] = {}  # Track update counts for each year

            merged_yearly_data = self.merged_data[key]  # Reference merged data for this key

            for year in ["2021", "2022", "2023"]:
                main_val = main_values.get(year, "0")
                sub_val = sub_values.get(year, "0")

                try:
                    main_val = float(main_val) if main_val != "N/A" and main_val is not None else 0.0
                except ValueError:
                    main_val = 0.0
                try:
                    sub_val = float(sub_val) if sub_val != "N/A" and sub_val is not None else 0.0
                except ValueError:
                    sub_val = 0.0

                # Calculate new average if valid values exist
                if main_val != 0.0 or sub_val != 0.0:
                    current_value = merged_yearly_data.get(year, 0.0)
                    current_count = merged_yearly_data['update_count'].get(year, 0)

                    # Update cumulative value and increment update count
                    new_value = current_value * current_count + main_val + sub_val
                    new_count = current_count + (1 if main_val != 0 else 0) + (1 if sub_val != 0 else 0)

                    # Store updated values
                    merged_yearly_data[year] = round(new_value / new_count, 3)
                    merged_yearly_data['update_count'][year] = new_count
                else:
                    # Keep existing value if no new data is available
                    merged_yearly_data[year] = merged_yearly_data.get(year, 0.0)

        return self.merged_data

    def find_missing_values(self, merged_data):
        """
        Identify metrics and years with missing values (i.e., 0 or 'N/A') in the merged data.
        """
        missing_entries = []
        for metric, yearly_data in merged_data.items():
            for year, value in yearly_data.items():
                if value in (0, 'N/A'):
                    missing_entries.append((metric, year))
        return missing_entries

    def re_analyze_missing_data(self, documents, missing_entries):
        """
        Re-analyze missing financial data for specific metrics and years using GPT.
        """
        all_content = "\n\n".join([doc.get('chunk', '') for doc in documents])

        if not all_content.strip():
            print("Error: No content provided to GPT for analysis.")
            return {}

        # Group missing entries by metrics
        metrics_by_year = {}
        for metric, year in missing_entries:
            if year not in metrics_by_year:
                metrics_by_year[year] = []
            metrics_by_year[year].append(metric)

        prompt = f"""
        You are a financial analyst. Based on the following content from chunks, extract only the missing financial metrics for specific years.
        - For ranges (e.g., "$8.00 to $10.00 billion"), calculate the average value.
        - If specific values for some years are missing, infer trends or use "N/A" if absolutely necessary.
        - Calculate YoY (Year-over-Year) percentage changes for Revenue.
        - Calculate margin percentages for Gross Profit, Operating Profit, and Net Profit where applicable.
        Focus exclusively on the following:
        {', '.join([f"{year}: {', '.join(metrics)}" for year, metrics in metrics_by_year.items()])}.

        Instructions:
        1. Strictly return the output in JSON format.
        2. Do not include any additional explanations or commentary.
        3. Assume all dollar values are in billions unless stated otherwise.
        Example JSON format:
        {{
            {', '.join([f'"{metric}": {{"{year}": <value>}}' for year, metrics in metrics_by_year.items() for metric in metrics])}
        }}

        Filtered Content:
        {all_content}
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst."},
                    {"role": "user", "content": prompt}
                ],
            )
            content = response['choices'][0]['message']['content'].strip()
            print("Raw GPT Response Content:\n", content)

            # Parse JSON response
            try:
                response_json = json.loads(content)
                return response_json
            except json.JSONDecodeError:
                print("Error: Failed to parse JSON. Attempting partial recovery.")
                # Extract JSON-like data
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    json_like_content = content[start_idx:end_idx + 1]
                    try:
                        partial_response_json = json.loads(json_like_content)
                        print("Partially Parsed JSON:\n", json.dumps(partial_response_json, indent=4))
                        return partial_response_json
                    except json.JSONDecodeError:
                        print("Error: Unable to parse JSON-like content.")
                return {}
        except Exception as e:
            print(f"Unexpected GPT API error: {e}")
            return {}

    # Main loop for handling missing values
    def handle_missing_values(self, main_documents, sub_documents):
        """
        Continuously check for missing values and re-analyze until no missing values remain.
        """
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Iteration {iteration}: Checking for missing values ---")
            missing_entries = self.find_missing_values(self.merged_data)

            if not missing_entries:
                print("No missing values remaining. Analysis complete.")
                break

            print(f"Found missing values: {missing_entries}")

            # Determine which documents to use based on missing years
            main_years = [year for _, year in missing_entries if year in ["2022", "2023"]]
            sub_years = [year for _, year in missing_entries if year in ["2021", "2022"]]

            if main_years:
                print(f"Re-analyzing missing data for years {main_years} using main documents.")
                new_data = self.re_analyze_missing_data(main_documents, missing_entries)
                self.merged_data = self.merge_financial_data(self.merged_data, new_data)

            if sub_years:
                print(f"Re-analyzing missing data for years {sub_years} using sub documents.")
                new_data = self.re_analyze_missing_data(sub_documents, missing_entries)
                self.merged_data = self.merge_financial_data(self.merged_data, new_data)

        return self.merged_data


    def generate_tabular(self, main_paths, sub_paths):
        """
        Finially, generate numeric data of financial metrics. The integrated function.
        """
        documents_main = self.read_documents(main_paths, ['ITEM 7.'])
        documents_sub = self.read_documents(sub_paths, ['ITEM 7.'])

        # Request 1: Analyze financials for 2022, 2023 from main paths
        data_2022_2023 = self.analyze_financials(documents_main, ["2022", "2023"])

        # Request 2: Analyze financials for 2021, 2022 from sub paths
        data_2021_2022 = self.analyze_financials(documents_sub, ["2021", "2022"])

        # Merge the two datasets
        _ = self.merge_financial_data(data_2022_2023, data_2021_2022)

        result = self.handle_missing_values(documents_main, documents_sub)

        return result