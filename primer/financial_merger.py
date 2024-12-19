def merge_financial_data(merged_data, main_data, sub_data):
    """
    Merge financial data by averaging values for overlapping years.

    :param merged_data: Dictionary to store merged data.
    :param main_data: Financial data from main documents.
    :param sub_data: Financial data from sub documents.
    :return: Updated merged_data.
    """
    all_keys = set(main_data.keys()).union(sub_data.keys())

    for key in all_keys:
        main_values = main_data.get(key, {})
        sub_values = sub_data.get(key, {})

        if key not in merged_data:
            merged_data[key] = {}
            merged_data[key]['update_count'] = {}

        for year in ["2021", "2022", "2023"]:
            main_val = main_values.get(year, 0)
            sub_val = sub_values.get(year, 0)

            main_val = float(main_val) if isinstance(main_val, (float, int)) else 0.0
            sub_val = float(sub_val) if isinstance(sub_val, (float, int)) else 0.0

            if main_val or sub_val:
                current_value = merged_data[key].get(year, 0.0)
                current_count = merged_data[key]['update_count'].get(year, 0)

                new_value = current_value * current_count + main_val + sub_val
                new_count = current_count + (1 if main_val else 0) + (1 if sub_val else 0)

                merged_data[key][year] = round(new_value / new_count, 3)
                merged_data[key]['update_count'][year] = new_count

    return merged_data


def find_missing_values(merged_data):
    """
    Identify metrics and years with missing values in the merged data.

    :param merged_data: Merged financial data.
    :return: List of missing entries as (metric, year) tuples.
    """
    missing_entries = []
    for metric, yearly_data in merged_data.items():
        for year, value in yearly_data.items():
            if value in (0, 'N/A'):
                missing_entries.append((metric, year))
    return missing_entries
