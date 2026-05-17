"""
生成更新后的 dyedream_vegetation.json 内容
"""
import json

FLOWERS = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
GRASS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

features = [
    "pasterdream:dyedream_trees",
    "pasterdream:patch_dyedream_buds",
    "pasterdream:patch_pinkagaric",
    "pasterdream:patch_dyedream_lily_pad",
    "pasterdream:patch_dyedream_lotus",
    "pasterdream:patch_dyedream_seagrass",
]

# 添加所有花
for i in FLOWERS:
    features.append(f"pasterdream:flower_{i}")

# 添加所有草
for i in GRASS:
    features.append(f"pasterdream:grass_{i}")

data = {
    "type": "neoforge:add_features",
    "biomes": "#pasterdream:is_dyedream",
    "features": features,
    "step": "vegetal_decoration"
}

print(json.dumps(data, indent=2, ensure_ascii=False))
print(f"\n总共 {len(features)} 个特征")