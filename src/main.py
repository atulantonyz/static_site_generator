import shutil
import os
from copystatic import copy_content
from gencontent import generate_page

def main():
    SRC_DIR = "./static"
    DST_DIR = "./public"
    print("Deleting public directory...")
    if os.path.exists(DST_DIR):
        shutil.rmtree(DST_DIR)
    print("Copying static content to public directory...")
    copy_content(SRC_DIR, DST_DIR)

    print("Generating page...")
    generate_page("content/index.md","template.html","public/index.html")





if __name__ == "__main__":
    main()

