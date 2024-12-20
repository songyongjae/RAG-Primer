import os
import json
import openai

class get_overview:
    def __init__(self):
        self.system_message = {"role": "system", "content": "You are an expert Financial assistant."}

    def read_documents(self, folder_paths, filter_items):
        """
        Reads JSON files from the specified folder paths and filters them by the filter_items.
        """
        documents = []
        for folder_path in folder_paths:
            self._process_folder(folder_path, filter_items, documents)
        return documents

    def _process_folder(self, folder_path, filter_items, documents):
        """
        Helper function to process each folder and filter files.
        """
        if not os.path.isdir(folder_path):
            print(f"Error: Folder path {folder_path} does not exist.")
            return

        for file in os.listdir(folder_path):
            if file.endswith('.json') and any(item.lower() in file.lower() for item in filter_items):
                self._load_file(os.path.join(folder_path, file), documents)

    def _load_file(self, file_path, documents):
        """
        Helper function to load a JSON file and append its content if valid.
        """
        try:
            with open(file_path, 'r') as f:
                content = json.load(f)
                if 'chunk' not in content:
                    print(f"Warning: 'chunk' key missing in {os.path.basename(file_path)}")
                documents.append(content)
        except Exception as e:
            print(f"Error loading file {os.path.basename(file_path)}: {e}")


    def analyze_overview(self, documents):
        """
        Generate the Overview section using text from ITEM 1 and ITEM 1A sections.
        """
        all_content = self._combine_content(documents)

        subtitle_prompt = self._generate_subtitle_prompt(all_content)
        overview_prompt = self._generate_overview_prompt(all_content)

        subtitle = self._generate_response(subtitle_prompt)
        overview_text = self._generate_response(overview_prompt)

        return subtitle, overview_text

    def _combine_content(self, documents):
        """
        Combines the 'chunk' content from all documents into a single string.
        """
        return "\n\n".join(doc.get('chunk', '') for doc in documents)

    def _generate_subtitle_prompt(self, content):
        """
        Generates a prompt for creating the subtitle.
        """
        return f"""
        Based on the following content about a company, create a short one-line subtitle (10 words or fewer)
        that describes the company's identity (e.g., "vehicle manufacturer") and specialties
        (e.g., "renewable energy solutions" or "solar energy systems").

        Content:
        {content}
        """

    def _generate_overview_prompt(self, content):
        """
        Returns the overview prompt as is.
        """
        return f"""
        You are a financial analyst. Based on the following content, summarize the company in a concise paragraph of 5 sentences or less.
        The paragraph should:
        1. Start with a one-liner explaining the company's identity and specialties.
        2. Describe how the company generates revenue, who they sell to, and the distribution of sales across their customer base.
        3. Provide key context about their business model. This is most important.

        Content:
        {content}
        """

    def _generate_response(self, prompt):
        """
        Uses OpenAI API to generate a response for the given prompt.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[self.system_message, {"role": "user", "content": prompt}],
        )
        return response['choices'][0]['message']['content'].strip()

    def generate_abstract(self, main_folder_paths):
        """
        Main function to generate the subtitle and overview content.
        """
        documents_main_overview = self.read_documents(main_folder_paths, ['ITEM 1.', 'ITEM 1A.'])

        subtitle, overview_content = self.analyze_overview(documents_main_overview)

        return subtitle, overview_content