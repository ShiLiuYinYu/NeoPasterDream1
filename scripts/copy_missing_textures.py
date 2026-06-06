"""
复制缺失的纹理文件：从原模组 (FixPasterDream) 复制并重命名为英文
"""
import shutil
from pathlib import Path

OLD_MOD = Path(r"C:\Users\97128\Documents\GitHub\NeoPasterDream1\libs\FixPasterDream-main\src\main\resources\assets\pasterdream")
NEW_MOD = Path(r"C:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\assets\pasterdream")

# (源文件名, 目标目录, 目标文件名)
COPY_TASKS = [
    # 方块纹理
    ("ning_feng_tie_kuai_.png",  "textures/block", "wind_iron_block.png"),
    ("ling_hun_kuang_tu_.png",   "textures/block", "soul_ore.png"),
    ("cu_tai_kuai_.png",         "textures/block", "raw_titanium_block.png"),

    # 物品纹理
    ("cong_lin_bao_zi_.png",     "textures/item",  "jungle_spore.png"),
    ("fen_hong_dan_.png",        "textures/item",  "pinkegg.png"),
    ("yuan_yi_qian_.png",        "textures/item",  "pliers.png"),
]

print("=" * 60)
print("📦 复制缺失的纹理文件")
print("=" * 60)

copied = 0
skipped = 0
for src_name, rel_dir, dst_name in COPY_TASKS:
    src_path = OLD_MOD / rel_dir / src_name
    dst_path = NEW_MOD / rel_dir / dst_name

    dst_path.parent.mkdir(parents=True, exist_ok=True)

    if not src_path.exists():
        print(f"  ⚠️  源文件不存在: {src_path}")
        skipped += 1
        continue

    shutil.copy2(src_path, dst_path)
    copied += 1
    print(f"  ✅ {src_name} → {dst_name}")

print(f"\n📊 结果：复制 {copied} 个，跳过 {skipped} 个")

# 为 meltdream_liquid_bucket 生成一个简单的占位纹理
# 使用熔岩桶风格：类似蓝色液体在桶中
print("\n📦 生成 meltdream_liquid_bucket.png 占位纹理...")
try:
    from PIL import Image, ImageDraw

    bucket_path = NEW_MOD / "textures/item" / "meltdream_liquid_bucket.png"
    if not bucket_path.exists():
        # 创建 16x16 像素的桶纹理（蓝色熔岩桶风格）
        img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 桶身（灰色边框）
        bucket_color = (100, 100, 100, 255)  # 灰色铁桶
        liquid_color = (50, 150, 255, 220)   # 蓝色液体

        # 桶的外形：简单矩形桶
        # 桶沿
        draw.rectangle([2, 0, 13, 2], fill=bucket_color)
        # 桶身
        draw.rectangle([1, 2, 14, 12], fill=bucket_color)
        # 桶内（液体）
        draw.rectangle([3, 3, 12, 11], fill=(80, 80, 80, 255))
        # 液体表面
        draw.rectangle([3, 3, 12, 8], fill=liquid_color)
        # 桶把
        draw.rectangle([5, 0, 10, 0], fill=bucket_color)
        # 高光
        draw.rectangle([3, 3, 4, 8], fill=(100, 180, 255, 180))
        # 手柄
        draw.arc([4, -3, 11, 3], 0, 180, fill=bucket_color, width=1)

        img.save(bucket_path)
        print(f"  ✅ 已生成占位纹理: textures/item/meltdream_liquid_bucket.png")
    else:
        print(f"  ⚠️  纹理已存在，跳过生成")
except ImportError:
    print("  ⚠️  PIL 未安装，无法生成图片，将创建空白纹理")
    # 创建简单的 1x1 PNG
    bucket_path = NEW_MOD / "textures/item" / "meltdream_liquid_bucket.png"
    if not bucket_path.exists():
        import struct
        import zlib
        def create_png(width, height, r, g, b, a=255):
            raw = b""
            for y in range(height):
                raw += b"\x00"  # filter byte
                for x in range(width):
                    raw += struct.pack("BBBB", r, g, b, a)
            def chunk(chunk_type, data):
                c = chunk_type + data
                return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
            ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
            return (b"\x89PNG\r\n\x1a\n"
                    + chunk(b"IHDR", ihdr)
                    + chunk(b"IDAT", zlib.compress(raw))
                    + chunk(b"IEND", b""))
        data = create_png(16, 16, 50, 150, 255)
        with open(bucket_path, "wb") as f:
            f.write(data)
        print(f"  ✅ 已生成占位纹理: textures/item/meltdream_liquid_bucket.png")
    else:
        print(f"  ⚠️  纹理已存在，跳过生成")

print("\n🎉 完成！")