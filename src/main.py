import shutil
import os
from copystatic import copy_content
from gencontent import generate_pages_recursive
import sys

def main():
    SRC_DIR = "./static"
    DST_DIR = "./docs"
    args = sys.argv[1:]
    base_path = "/"
    if len(args) > 0:
        base_path = args[0]


    print("Deleting public directory...")
    if os.path.exists(DST_DIR):
        shutil.rmtree(DST_DIR)
    print("Copying static content to public directory...")

    copy_content(SRC_DIR,DST_DIR)

    print("Generating page...")
    generate_pages_recursive(base_path,"content","template.html","docs")





if __name__ == "__main__":
    main()

