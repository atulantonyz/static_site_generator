import shutil
import os

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
