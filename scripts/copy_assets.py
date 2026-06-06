"""
资源迁移脚本：将原模组 (FixPasterDream) 的纹理、模型、blockstate 文件
复制到新模组 (NeoPasterDream) 并完成中文拼音 → 英文名的重命名。

用法：python scripts/copy_assets.py
"""

import json
import os
import shutil
from pathlib import Path

# ============================================================
# 路径配置
# ============================================================
SOURCE_ROOT = Path(r"C:\Users\97128\Documents\GitHub\NeoPasterDream1\libs\FixPasterDream-main\src\main\resources\assets\pasterdream")
TARGET_ROOT = Path(r"C:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\assets\pasterdream")

# ============================================================
# 方块纹理映射（textures/block/）：原文件名 → 目标文件名
# 注意：映射的值不含路径，仅为文件名
# ============================================================
BLOCK_TEXTURE_MAP = {
    "tai_kuai_.png":                             "titanium_block.png",
    "raw_tai_kuai_.png":                          "raw_titanium_block.png",
    "ran_meng_shi_ying_kuai_.png":                "moltengold_block.png",
    "shou_hu_zhe_fang_kuai_.png":                 "blackmetal_block.png",
    "ying_jue_0.png":                             "charged_amethyst_block.png",
    "wind_iron_block.png":                        "wind_iron_block.png",
    "shen_ceng_tai_kuang_shi_.png":               "deepslate_titanium_ore.png",
    "ran_meng_shi_ying_kuang_shi_.png":           "moltengold_ore.png",
    "ling_hun_kuang_shi_.png":                    "soul_ore.png",
    "pebble_0.png":                               "pebble_0.png",
    "shadow_light_0.png":                         "shadow_light_0.png",
    "zhi_yan_jin_kuai_.png":                      "vine_0.png",
    "zhong_xing_ran_meng_jing_ya_.png":           "goldenrod.png",
    "crop_0a.png":                                "crop_0a.png",
    "crop_1a.png":                                "crop_1a.png",
    "crop_3a.png":                                "crop_3a.png",
    "crop_4a.png":                                "crop_4a.png",
    "jungle_spore.png":                           "jungle_spore.png",
    "meltdream_liquid_bucket.png":                "meltdream_liquid_bucket.png",
    "pinkegg.png":                                "pinkegg.png",
    "pliers.png":                                 "pliers.png",
    "pebble.png":                                 "pebble_0_particle.png",
    "cu_tai_kuai_.png":                           "raw_titanium_block_side.png",
    "ran_meng_dong_xue_teng_man_.png":            "vine_0.png",
    "qiu_qi_lin_.png":                            "goldenrod_cross.png",
    "ying_deng_.png":                             "shadow_light_0_side.png",
    "ying_deng__top.png":                         "shadow_light_0_top.png",
}

# 需要创建的普通方块列表（cube_all 类型）
SIMPLE_BLOCKS = [
    "titanium_block",
    "raw_titanium_block",
    "moltengold_block",
    "blackmetal_block",
    "charged_amethyst_block",
    "wind_iron_block",
    "deepslate_titanium_ore",
    "moltengold_ore",
    "soul_ore",
]

# 需要特殊处理的方块（从原模组复制模型并重命名纹理引用）
SPECIAL_BLOCKS = [
    "pebble_0",
    "shadow_light_0",
    "vine_0",
    "goldenrod",
    "crop_0a",
    "crop_1a",
    "crop_3a",
    "crop_4a",
]

# 物品纹理列表（从 source 的 textures/block 复制到 target 的 textures/item）
ITEM_TEXTURES = [
    "titanium_block.png",
    "raw_titanium_block.png",
    "moltengold_block.png",
    "blackmetal_block.png",
    "charged_amethyst_block.png",
    "wind_iron_block.png",
    "deepslate_titanium_ore.png",
    "moltengold_ore.png",
    "soul_ore.png",
    "pebble_0.png",
    "shadow_light_0.png",
    "vine_0.png",
    "goldenrod.png",
    "crop_0a.png",
    "crop_1a.png",
    "crop_2a.png",
    "crop_3a.png",
    "crop_4a.png",
    "jungle_spore.png",
    "meltdream_liquid_bucket.png",
    "pinkegg.png",
    "pliers.png",
]

# ============================================================
# 特殊方块的模型纹理重命名规则
# key = 方块名, value = (旧纹理引用 → 新纹理引用) 映射
# ============================================================
BLOCK_MODEL_TEXTURE_FIXES = {
    "pebble_0": {
        "pebble": "pebble_0_particle",
    },
    "shadow_light_0": {
        "ying_deng__top": "shadow_light_0_top",
        "ying_deng_": "shadow_light_0_side",
    },
    "vine_0": {
        "ran_meng_dong_xue_teng_man_": "vine_0",
    },
    "goldenrod": {
        "qiu_qi_lin_": "goldenrod_cross",
    },
    "crop_0a": {
        "meng_ran_cha_hua_": "crop_0a",
    },
    "crop_1a": {
        "cang_bai_xue_lian_": "crop_1a",
    },
    "crop_3a": {
        "ling_yun_hua_": "crop_3a",
    },
    "crop_4a": {
        "mian_hua_": "crop_4a",
    },
}

# 特殊方块的 item 模型纹理重命名规则
ITEM_MODEL_TEXTURE_FIXES = {
    "pebble_0": {
        "pebble_item": "pebble_0",
    },
    "vine_0": {
        "ran_meng_dong_xue_teng_man_": "vine_0",
    },
    "goldenrod": {
        "qiu_qi_lin_": "goldenrod_cross",
    },
    "crop_0a": {
        "meng_ran_cha_hua_": "crop_0a",
    },
    "crop_1a": {
        "cang_bai_xue_lian_": "crop_1a",
    },
    "crop_3a": {
        "ling_yun_hua_": "crop_3a",
    },
    "crop_4a": {
        "mian_hua_": "crop_4a",
    },
}


def ensure_dir(path):
    """确保目标目录存在，如果不存在则创建"""
    path.mkdir(parents=True, exist_ok=True)


def copy_and_rename_file(src_dir, dst_dir, src_name, dst_name):
    """
    复制并重命名文件。如果源文件不存在则返回 False。
    """
    src_path = src_dir / src_name
    dst_path = dst_dir / dst_name
    if not src_path.exists():
        return False, f"源文件不存在: {src_path}"
    ensure_dir(dst_dir)
    shutil.copy2(src_path, dst_path)
    return True, f"已复制: {src_name} → {dst_name}"


def create_json_file(path, data):
    """创建 JSON 文件"""
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_json_file(path):
    """读取 JSON 文件"""
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fix_texture_references(data, fix_map):
    """
    递归遍历 JSON 对象，将所有以 "pasterdream:block/" 或 "pasterdream:item/" 开头的
    纹理引用中的旧名称替换为新名称。
    """
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if isinstance(v, str):
                for old_key, new_key in fix_map.items():
                    # 替换纹理路径中的旧引用
                    if f":block/{old_key}" in v:
                        v = v.replace(f":block/{old_key}", f":block/{new_key}")
                    elif f":item/{old_key}" in v:
                        v = v.replace(f":item/{old_key}", f":item/{new_key}")
            new_dict[k] = fix_texture_references(v, fix_map)
        return new_dict
    elif isinstance(data, list):
        return [fix_texture_references(item, fix_map) for item in data]
    return data


def copy_block_textures():
    """
    复制方块纹理并重命名。
    """
    src_dir = SOURCE_ROOT / "textures" / "block"
    dst_dir = TARGET_ROOT / "textures" / "block"
    stats = {"copied": 0, "skipped": 0, "warnings": []}

    print("=" * 60)
    print("📦 复制方块纹理 (textures/block/)")
    print("=" * 60)

    for src_name, dst_name in BLOCK_TEXTURE_MAP.items():
        success, msg = copy_and_rename_file(src_dir, dst_dir, src_name, dst_name)
        if success:
            stats["copied"] += 1
            print(f"  ✅ {msg}")
        else:
            stats["skipped"] += 1
            stats["warnings"].append(msg)
            print(f"  ⚠️  {msg}")

    return stats


def copy_item_textures():
    """
    复制物品纹理（从 source textures/block 复制到 target textures/item）。
    首先尝试从 textures/block 找，如果找不到再从 textures/item 找。
    """
    src_block_dir = SOURCE_ROOT / "textures" / "block"
    src_item_dir = SOURCE_ROOT / "textures" / "item"
    dst_dir = TARGET_ROOT / "textures" / "item"
    stats = {"copied": 0, "skipped": 0, "warnings": []}

    print("\n" + "=" * 60)
    print("📦 复制物品纹理 (textures/item/)")
    print("=" * 60)

    for fname in ITEM_TEXTURES:
        # 先尝试从 textures/block/ 找
        src_path = src_block_dir / fname
        if not src_path.exists():
            # 再尝试从 textures/item/ 找
            src_path = src_item_dir / fname

        dst_path = dst_dir / fname
        if not src_path.exists():
            stats["skipped"] += 1
            warn_msg = f"纹理文件未找到 (block 和 item 目录均无): {fname}"
            stats["warnings"].append(warn_msg)
            print(f"  ⚠️  {warn_msg}")
            continue

        ensure_dir(dst_dir)
        shutil.copy2(src_path, dst_path)
        stats["copied"] += 1
        print(f"  ✅ 已复制: {fname} (来自 {src_path.parent.name}/)")

    return stats


def create_simple_blockstates():
    """
    为普通方块创建 blockstate JSON（variants 格式）。
    """
    dst_dir = TARGET_ROOT / "blockstates"
    stats = {"created": 0}

    print("\n" + "=" * 60)
    print("📦 创建 blockstate JSON")
    print("=" * 60)

    for name in SIMPLE_BLOCKS:
        data = {
            "variants": {
                "": {
                    "model": f"pasterdream:block/{name}"
                }
            }
        }
        path = dst_dir / f"{name}.json"
        create_json_file(path, data)
        stats["created"] += 1
        print(f"  ✅ 已创建: blockstates/{name}.json")

    return stats


def create_simple_block_models():
    """
    为普通方块创建 block 模型 JSON（cube_all 类型）。
    """
    dst_dir = TARGET_ROOT / "models" / "block"
    stats = {"created": 0}

    print("\n" + "=" * 60)
    print("📦 创建方块模型 (models/block/)")
    print("=" * 60)

    for name in SIMPLE_BLOCKS:
        data = {
            "parent": "block/cube_all",
            "textures": {
                "all": f"pasterdream:block/{name}"
            }
        }
        path = dst_dir / f"{name}.json"
        create_json_file(path, data)
        stats["created"] += 1
        print(f"  ✅ 已创建: models/block/{name}.json")

    return stats


def create_simple_item_models():
    """
    为普通方块创建 item 模型 JSON（parent 指向 block 模型）。
    """
    dst_dir = TARGET_ROOT / "models" / "item"
    stats = {"created": 0}

    print("\n" + "=" * 60)
    print("📦 创建物品模型 (models/item/)")
    print("=" * 60)

    for name in SIMPLE_BLOCKS:
        data = {
            "parent": f"pasterdream:block/{name}"
        }
        path = dst_dir / f"{name}.json"
        create_json_file(path, data)
        stats["created"] += 1
        print(f"  ✅ 已创建: models/item/{name}.json")

    return stats


def copy_special_blockstates():
    """
    复制特殊方块的 blockstate JSON，无需修改纹理引用（blockstate 只引用模型路径）。
    """
    stats = {"copied": 0, "skipped": 0, "warnings": []}

    for name in SPECIAL_BLOCKS:
        src_path = SOURCE_ROOT / "blockstates" / f"{name}.json"
        dst_path = TARGET_ROOT / "blockstates" / f"{name}.json"
        if not src_path.exists():
            stats["skipped"] += 1
            stats["warnings"].append(f"源 blockstate 不存在: {name}.json")
            print(f"  ⚠️  源 blockstate 不存在: {name}.json")
            continue
        data = read_json_file(src_path)
        if data is None:
            stats["skipped"] += 1
            stats["warnings"].append(f"无法读取源 blockstate: {name}.json")
            print(f"  ⚠️  无法读取源 blockstate: {name}.json")
            continue
        create_json_file(dst_path, data)
        stats["copied"] += 1
        print(f"  ✅ 已复制: blockstates/{name}.json")

    return stats


def copy_special_block_models():
    """
    复制特殊方块的 block 模型 JSON，并更新纹理引用。
    对于 pebble_0，还需要复制 custom/pebble.json。
    """
    dst_dir = TARGET_ROOT / "models" / "block"
    stats = {"copied": 0, "skipped": 0, "warnings": []}

    # 处理 pebble_0 的自定义模型
    if "pebble_0" in SPECIAL_BLOCKS:
        custom_src = SOURCE_ROOT / "models" / "custom" / "pebble.json"
        custom_dst = TARGET_ROOT / "models" / "custom" / "pebble.json"
        if custom_src.exists():
            data = read_json_file(custom_src)
            if data is not None:
                # pebble 自定义模型使用 #0 引用纹理，由父模型传入，所以无需修改
                create_json_file(custom_dst, data)
                print(f"  ✅ 已复制: models/custom/pebble.json")
            else:
                stats["warnings"].append("无法读取 custom/pebble.json")
                print(f"  ⚠️  无法读取 custom/pebble.json")
        else:
            stats["warnings"].append("源 custom/pebble.json 不存在")
            print(f"  ⚠️  源 custom/pebble.json 不存在")

    for name in SPECIAL_BLOCKS:
        src_path = SOURCE_ROOT / "models" / "block" / f"{name}.json"
        dst_path = dst_dir / f"{name}.json"

        if not src_path.exists():
            stats["skipped"] += 1
            stats["warnings"].append(f"源 block 模型不存在: {name}.json")
            print(f"  ⚠️  源 block 模型不存在: {name}.json")
            continue

        data = read_json_file(src_path)
        if data is None:
            stats["skipped"] += 1
            stats["warnings"].append(f"无法读取源 block 模型: {name}.json")
            print(f"  ⚠️  无法读取源 block 模型: {name}.json")
            continue

        # 应用纹理引用重命名
        if name in BLOCK_MODEL_TEXTURE_FIXES:
            data = fix_texture_references(data, BLOCK_MODEL_TEXTURE_FIXES[name])

        create_json_file(dst_path, data)
        stats["copied"] += 1
        print(f"  ✅ 已复制并更新: models/block/{name}.json")

    return stats


def copy_special_item_models():
    """
    复制特殊方块的 item 模型 JSON，并更新纹理引用。
    """
    dst_dir = TARGET_ROOT / "models" / "item"
    stats = {"copied": 0, "skipped": 0, "warnings": []}

    for name in SPECIAL_BLOCKS:
        src_path = SOURCE_ROOT / "models" / "item" / f"{name}.json"
        dst_path = dst_dir / f"{name}.json"

        if not src_path.exists():
            # 对于 shadow_light_0，item 模型的 parent 是 block 模型，不需要纹理修正
            # 看看是否可以直接创建简单版本
            if name == "shadow_light_0":
                # shadow_light_0 的 item 模型是 parent 指向 block 模型
                # 但源文件存在，尝试读取并修复
                stats["warnings"].append(f"源 item 模型不存在: {name}.json")
                print(f"  ⚠️  源 item 模型不存在: {name}.json")
                continue
            stats["skipped"] += 1
            stats["warnings"].append(f"源 item 模型不存在: {name}.json")
            print(f"  ⚠️  源 item 模型不存在: {name}.json")
            continue

        data = read_json_file(src_path)
        if data is None:
            stats["skipped"] += 1
            stats["warnings"].append(f"无法读取源 item 模型: {name}.json")
            print(f"  ⚠️  无法读取源 item 模型: {name}.json")
            continue

        # 应用纹理引用重命名
        if name in ITEM_MODEL_TEXTURE_FIXES:
            data = fix_texture_references(data, ITEM_MODEL_TEXTURE_FIXES[name])

        create_json_file(dst_path, data)
        stats["copied"] += 1
        print(f"  ✅ 已复制并更新: models/item/{name}.json")

    return stats


def print_summary(all_stats):
    """
    打印操作摘要。
    """
    print("\n" + "=" * 60)
    print("📊 操作摘要")
    print("=" * 60)

    categories = {
        "方块纹理复制": all_stats["block_textures"],
        "物品纹理复制": all_stats["item_textures"],
        "Blockstate JSON 创建": all_stats["simple_blockstates"],
        "方块模型 JSON 创建": all_stats["simple_block_models"],
        "物品模型 JSON 创建": all_stats["simple_item_models"],
        "特殊 Blockstate 复制": all_stats["special_blockstates"],
        "特殊方块模型复制": all_stats["special_block_models"],
        "特殊物品模型复制": all_stats["special_item_models"],
    }

    total_copied = 0
    total_created = 0
    total_skipped = 0
    all_warnings = []

    for label, stat in categories.items():
        copied = stat.get("copied", 0)
        created = stat.get("created", 0)
        skipped = stat.get("skipped", 0)
        warnings = stat.get("warnings", [])
        total_copied += copied
        total_created += created
        total_skipped += skipped
        all_warnings.extend(warnings)
        parts = []
        if copied:
            parts.append(f"复制 {copied} 个")
        if created:
            parts.append(f"创建 {created} 个")
        if skipped:
            parts.append(f"跳过 {skipped} 个")
        print(f"  {label}: {', '.join(parts)}")

    print(f"\n  总计：复制 {total_copied} 个文件，创建 {total_created} 个文件")
    if total_skipped > 0:
        print(f"  跳过：{total_skipped} 个（源文件缺失）")

    if all_warnings:
        print(f"\n⚠️  警告列表 ({len(all_warnings)} 条):")
        for w in all_warnings:
            print(f"    - {w}")


def main():
    print("🚀 开始资源迁移...\n")

    # 1. 复制方块纹理
    block_tex_stats = copy_block_textures()

    # 2. 复制物品纹理
    item_tex_stats = copy_item_textures()

    # 3. 创建普通方块 blockstate
    blockstate_stats = create_simple_blockstates()

    # 4. 创建普通方块 block 模型
    block_model_stats = create_simple_block_models()

    # 5. 创建普通方块 item 模型
    item_model_stats = create_simple_item_models()

    # 6. 复制特殊方块 blockstate
    special_bs_stats = copy_special_blockstates()

    # 7. 复制特殊方块 block 模型
    special_bm_stats = copy_special_block_models()

    # 8. 复制特殊方块 item 模型
    special_im_stats = copy_special_item_models()

    # 汇总
    all_stats = {
        "block_textures": block_tex_stats,
        "item_textures": item_tex_stats,
        "simple_blockstates": blockstate_stats,
        "simple_block_models": block_model_stats,
        "simple_item_models": item_model_stats,
        "special_blockstates": special_bs_stats,
        "special_block_models": special_bm_stats,
        "special_item_models": special_im_stats,
    }

    print_summary(all_stats)

    print("\n🎉 资源迁移完成！")


if __name__ == "__main__":
    main()