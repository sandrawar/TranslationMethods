import os
import shutil
from comet import download_model

model_ckpt_path = download_model("Unbabel/wmt22-comet-da")

model_root_dir = os.path.dirname(os.path.dirname(model_ckpt_path))

target_dir = "models/comet"

shutil.copytree(model_root_dir, target_dir, dirs_exist_ok=True)

print(f"Model skopiowany do: {target_dir}")