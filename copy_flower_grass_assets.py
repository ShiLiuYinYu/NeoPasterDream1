"""
批量复制 flower_N / grass_N 的资源文件从 libs 到主项目
"""
import os
import shutil
import glob

# 路径配置
LIBS_ASSETS = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1\libs\FixPasterDream-main\src\main\resources\assets\pasterdream"
MAIN_ASSETS = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\assets\pasterdream"

# 需要复制的文件类型和目录映射
COPY_TASKS = [
    # (源目录, 目标目录, 文件名匹配模式)
    (os.path.join(LIBS_ASSETS, "blockstates"), os.path.join(MAIN_ASSETS, "blockstates"), "flower_*.json"),
    (os.path.join(LIBS_ASSETS, "blockstates"), os.path.join(MAIN_ASSETS, "blockstates"), "grass_*.json"),
    (os.path.join(LIBS_ASSETS, "models", "block"), os.path.join(MAIN_ASSETS, "models", "block"), "flower_*.json"),
    (os.path.join(LIBS_ASSETS, "models", "block"), os.path.join(MAIN_ASSETS, "models", "block"), "grass_*.json"),
    (os.path.join(LIBS_ASSETS, "models", "item"), os.path.join(MAIN_ASSETS, "models", "item"), "flower_*.json"),
    (os.path.join(LIBS_ASSETS, "models", "item"), os.path.join(MAIN_ASSETS, "models", "item"), "grass_*.json"),
]

# 收集所有模型的纹理引用，找出需要复制的纹理文件
def find_referenced_textures():
    textures_needed = set()
    for src_dir, _, pattern in COPY_TASKS:
        if "models" in src_dir:
            for f in glob.glob(os.path.join(src_dir, pattern)):
                with open(f, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                    # 提取 texture 引用: "cross": "pasterdream:block/xxx"
                    import re
                    for match in re.finditer(r'"pasterdream:block/([^"]+)"', content):
                        textures_needed.add(match.group(1) + ".png")
    return textures_needed


def copy_files():
    copied = 0
    for src_dir, dst_dir, pattern in COPY_TASKS:
        os.makedirs(dst_dir, exist_ok=True)
        for f in glob.glob(os.path.join(src_dir, pattern)):
            dst = os.path.join(dst_dir, os.path.basename(f))
            if not os.path.exists(dst):
                shutil.copy2(f, dst)
                copied += 1
                print(f"  [COPY] {os.path.basename(f)}")
            else:
                print(f"  [SKIP] {os.path.basename(f)} (已存在)")
    return copied


def copy_textures(textures_needed):
    src_tex = os.path.join(LIBS_ASSETS, "textures", "block")
    dst_tex = os.path.join(MAIN_ASSETS, "textures", "block")
    os.makedirs(dst_tex, exist_ok=True)
    copied = 0
    for tex_name in sorted(textures_needed):
        src = os.path.join(src_tex, tex_name)
        dst = os.path.join(dst_tex, tex_name)
        if os.path.exists(src):
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                copied += 1
                print(f"  [COPY texture] {tex_name}")
            else:
                print(f"  [SKIP texture] {tex_name} (已存在)")
        else:
            print(f"  [MISS] {tex_name} (源文件不存在)")
    return copied


print("=== 第1步: 分析模型文件引用的纹理 ===")
textures = find_referenced_textures()
print(f"发现 {len(textures)} 个纹理引用")

print("\n=== 第2步: 复制模型/blockstate JSON 文件 ===")
model_count = copy_files()
print(f"复制了 {model_count} 个JSON文件")

print("\n=== 第3步: 复制纹理 PNG 文件 ===")
tex_count = copy_textures(textures)
print(f"复制了 {tex_count} 个纹理文件")

print("\n=== 完成! ===")
print(f"总共复制: {model_count} 个JSON + {tex_count} 个纹理")