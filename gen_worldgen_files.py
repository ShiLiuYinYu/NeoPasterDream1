"""
批量生成 flower_N / grass_N 的 worldgen configured_feature 和 placed_feature JSON 文件
"""
import os
import json

CF_DIR = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\data\pasterdream\worldgen\configured_feature"
PF_DIR = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\data\pasterdream\worldgen\placed_feature"

FLOWERS = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
GRASS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


def gen_configured_feature(name):
    return {
        "type": "minecraft:random_patch",
        "config": {
            "tries": 48,
            "xz_spread": 7,
            "y_spread": 3,
            "feature": {
                "type": "minecraft:simple_block",
                "config": {
                    "to_place": {
                        "type": "minecraft:simple_state_provider",
                        "state": {
                            "Name": f"pasterdream:{name}"
                        }
                    }
                }
            }
        }
    }


def gen_placed_feature(name, use_rarity=True):
    placement = []
    if use_rarity:
        placement.append({"type": "minecraft:rarity_filter", "chance": 32})
    else:
        placement.append({"type": "minecraft:count", "count": 7})
    placement.append({"type": "minecraft:in_square"})
    placement.append({"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"})
    placement.append({
        "type": "minecraft:block_predicate_filter",
        "predicate": {
            "type": "minecraft:matching_blocks",
            "offset": [0, -1, 0],
            "blocks": [
                "pasterdream:dyedream_grass",
                "pasterdream:dyedream_dirt",
                "pasterdream:dyedream_sand",
                "pasterdream:dyedream_block"
            ]
        }
    })
    placement.append({"type": "minecraft:biome"})
    return {"feature": f"pasterdream:{name}", "placement": placement}


def save_json(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [OK] {os.path.basename(filepath)}")


print("=== 花的 configured/placed feature ===")
for i in FLOWERS:
    name = f"flower_{i}"
    save_json(os.path.join(CF_DIR, f"{name}.json"), gen_configured_feature(name))
    save_json(os.path.join(PF_DIR, f"{name}.json"), gen_placed_feature(name, use_rarity=True))

print("\n=== 草的 configured/placed feature ===")
for i in GRASS:
    name = f"grass_{i}"
    save_json(os.path.join(CF_DIR, f"{name}.json"), gen_configured_feature(name))
    save_json(os.path.join(PF_DIR, f"{name}.json"), gen_placed_feature(name, use_rarity=False))

print(f"\n完成！")