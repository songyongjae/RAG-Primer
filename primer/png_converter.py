import subprocess

def html_to_png(html_file, output_path):
    """
    Convert an HTML file to a PNG image using wkhtmltoimage.

    :param html_file: Path to the input HTML file.
    :param output_path: Path to the output PNG file.
    """
    try:
        options = [
            '--enable-local-file-access',
            '--format', 'png',
            '--width', '1240',
            '--height', '1300',
            '--quality', '100'
        ]
        subprocess.run(
            ['wkhtmltoimage'] + options + [html_file, output_path],
            check=True
        )
        print(f"PNG successfully generated: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during image generation: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
