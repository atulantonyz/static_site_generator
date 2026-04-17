import shutil
import os
from copystatic import copy_content
from gencontent import generate_pages_recursive

def main():
    SRC_DIR = "./static"
    DST_DIR = "./public"
    print("Deleting public directory...")
    if os.path.exists(DST_DIR):
        shutil.rmtree(DST_DIR)
    print("Copying static content to public directory...")
    copy_content(SRC_DIR, DST_DIR)

    print("Generating page...")
    generate_pages_recursive("content","template.html","public")





if __name__ == "__main__":
    main()

