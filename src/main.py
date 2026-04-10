import shutil
import os

def main():
    SRC_DIR = "./static"
    DST_DIR = "./public"
    print("Deleting public directory...")
    if os.path.exists(DST_DIR):
        shutil.rmtree(DST_DIR)
    print("Copying static content to public directory...")
    copy_content(SRC_DIR, DST_DIR)

def copy_content(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    children = os.listdir(src_dir)
    for child_name in children:
        child_path = os.path.join(src_dir, child_name)
        dst_child_path = os.path.join(dst_dir, child_name)
        print(f" * {child_path} -> {dst_child_path}")
        if os.path.isfile(child_path):
            shutil.copy(child_path, dst_dir)
        else:
            copy_content(child_path, dst_child_path)



if __name__ == "__main__":
    main()

