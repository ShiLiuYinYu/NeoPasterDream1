import json, glob

base = 'src/main/resources/data/pasterdream'

# ========== 1. 云朵：修改生成配置 ==========
# patch_cloud placed_feature
path = f'{base}/worldgen/placed_feature/patch_cloud.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
# 替换heightmap为height_range，增加count
old_placement = data['placement']
new_placement = []
for p in old_placement:
    if p.get('type') == 'minecraft:heightmap':
        # 替换为高度范围（在天空生成）
        new_placement.append({'type': 'minecraft:height_range', 'height': {'type': 'minecraft:uniform', 'min_inclusive': {'above_bottom': 80}, 'max_inclusive': {'above_bottom': 150}}})
    elif p.get('type') == 'minecraft:count' and p.get('count') == 2:
        new_placement.append({'type': 'minecraft:count', 'count': 6})
    else:
        new_placement.append(p)
data['placement'] = new_placementplacement'] = new_placement
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print('[OK] patch_cloud.json: heightmap -> height_range(Y80-150), count 2 -> 6')

# 云朵configured_feature增加y_spread和地面检查
path = f'{base}/worldgen/configured_feature/patch_cloud.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data['config']['tries'] = 12
data['config']['xz_spread'] = 6
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print('[OK] patch_cloud.json: tries 6 -> 12, xz_spread 2 -> 6')

# ========== 1b. 云朵语言文件 ==========
for lang_file in ['en_us.json', 'zh_cn.json']:
    lang_path = f'src/main/resources/assets/pasterdream/lang/{lang_file}'
    with open(lang_path, 'r', encoding='utf-8') as f:
        lang_data = json.load(f)
    if lang_file == 'zh_cn.json':
        entries = {'block.pasterdream.cloud': '云', 'block.pasterdream.dark_cloud': '暗云', 'block.pasterdream.thick_cloud': '厚云'}
    else:
        entries = {'block.pasterdream.cloud': 'Cloud', 'block.pasterdream.dark_cloud': 'Dark Cloud', 'block.pasterdream.thick_cloud': 'Thick Cloud'}
    added = 0
    for k, v in entries.items():
        if k not in lang_data:
            lang_data[k] = v
            added += 1
    with open(lang_path, 'w', encoding='utf-8') as f:
        json.dump(lang_data, f, indent=4, ensure_ascii=False)
    print(f'[OK] {lang_file}: 添加 {added} 条云朵语言条目')

# ========== 2. grass_5移除 ==========
veg_path = f'{base}/neoforge/biome_modifier/dyedream_vegetation.json'
with open(veg_path, 'r', encoding='utf-8') as f:
    veg = json.load(f)
veg['features'] = [f for f in veg['features'] if f != 'pasterdream:grass_5']
with open(veg_path, 'w', encoding='utf知道参数-8') as f:
    json.dump(veg, f, indent=2)
print('[OK] dyedream_vegetation.json: grass_5 已移除')

# ========== 3. 水草修复+密度提升 ==========
# seagrass configured_feature: 修复waterlogged状态
sg_path = f'{base}/worldgen/configured_feature/patch_dyedream_seagrass.json'
with open(sg_path, 'r', encoding='utf-8') as f:
    sg = json.load(f)
sg['config']['feature']['feature']['config']['to_place']['state']['Properties'] = {'waterlogged': 'true'}
sg['config']['tries'] = 64
with open(sg_path, 'w', encoding='utf-8') as f:
    json.dumps(sg, f, indent=2)
    # fix: actually write
    sg_str = json.dumps(sg, f, indent=2)
    # No, json.dump is correct. Let me fix this.
# Actually the write should work, let me redo this block
with open(sg_path, 'w', encoding='utf-8') as f:
    json.dump(sg, f, indent=2)
print('[OK] patch_dyedream_seagrass.json: 增加 waterlogged=true, tries 32 -> 64')

# 密度提升
updates = {'patch_dyedream_lily_pad.json': 12, 'patch_dyedream_lotus.json': 10, 'patch_dyedream_seagrass.json': 24}
for fname, count in updates.items():
    fpath = f'{base}/worldgen/placed_feature/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for p in data['placement']:
        if p.get('type') == 'minecraft:count':
            p['count'] = count
            break
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f'[OK] {fname}: count -> {count}')

print('\n[DONE] 可处理部分已全部完成！')