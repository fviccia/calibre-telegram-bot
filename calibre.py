import subprocess


def add_ebook_to_calibre(save_path, calibre_adress, calibre_user, calibre_pwd):
    try:
        # Command to add ebook to Calibre library with specific library and authentication
        result = subprocess.run(
            [
                "calibredb",
                "--with-library",
                calibre_adress,
                "--username",
                calibre_user,
                "--password",
                calibre_pwd,
                "add",
                save_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Success:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
    return result.stdout
