from html_section_processor.processor import get_sources_10k

def TASK_1():
    print("=" * 80, "\nTask 1")
    print("=" * 80)

    main_metadata = [{"ticker": "tsla", "fiscal_year": 20231231}]
    sub_metadata = [{"ticker": "tsla", "fiscal_year": 20221231}]

    chunk_processor = get_sources_10k()

    def generate_chunk(files_metadata):
        chunk_processor.process_file(files_metadata)
        summary = chunk_processor.classify_files(files_metadata)
        print(summary)

    generate_chunk(main_metadata)
    generate_chunk(sub_metadata)

if __name__ == "__main__":
    TASK_1()
