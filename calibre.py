import subprocess


def add_ebook_to_calibre(ebook_path):
    try:
        # Command to add ebook to Calibre library with specific library and authentication
        result = subprocess.run(
            [
                "calibredb",
                "--with-library",
                "http://192.168.68.81:8091/",
                "--username",
                "franco",
                "--password",
                "123456",
                "add",
                ebook_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Success:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
    return result.stdout


# Path to your eBook file
# ebook_path = "path/to/your/ebook.epub"  # Replace with the actual path to your eBook
# add_ebook_to_calibre(ebook_path)
