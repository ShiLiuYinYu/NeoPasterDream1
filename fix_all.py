import json, glob

base = 'src/main/resources/data/pasterdream'

# ========== 1. 云朵生成 + 语言文件 ==========
# placed_feature: 替换heightmap为height_range，count 2->6
path = f'{base}/worldgen/placed_feature/patch_cloud.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
new_placement = []
for p in data['placement']:
    if p.get('type') == 'minecraft:heightmap':
        data['placement'].append({'type': 'minecraft:height_range', 'height': {'type': 'minecraft:uniform', 'min_inclusive': {'above_bottom': 80}, 'max_inclusive': {'above_bottom': 150}}})
    elif p.get('type') == 'minecraft:count' and p.get('count') == 2:
        data['placement'].append({'type': 'minecraft:count', 'count': 6})
    elif p.get('type') != 'minecraft:heightmap':
        data['placement'].append(p)
This is getting messy. Let me just rewrite the whole placement list.
data['placement = [
    {"type": "minecraft:count", "count": 6},
    {"type": "minecraft:in_square"},
    {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"above_bottom": 80}, "max_inclusive": {"above_bottom": 150}}},
    {"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:matching_blocks", "blocks": ["minecraft:air", "minecraft:cave_air"]}}
]
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print('[OK] patch_cloud placed_feature: -> height_range Y80-150, count 6')

# configured_feature: 增加聚集度
path = f'{base}/worldgen/configured_feature/patch_cloud.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
data['config']['tries'] = 12
data['config']['xz_spread'] = 6
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print('[OK] patch_cloud configured_feature: tries 6->12, xz_spread 2->6')

# 语言文件
for lang in ['en_us.json', 'zh_cn.json']:
    lang_path = f'src/main/resources/assets/pasterdream/lang/{lang}'
    with open(lang_path, 'r', encoding='utf-8') as f:
        ld = json.load(f)
    entries = {'block.pasterdream.cloud': '云', 'block.pasterdream.dark_cloud': '暗云', 'block.pasterdream.thick_cloud': '厚云'} if lang == 'zh_cn.json' else {'block.pasterdream.cloud': 'Cloud', 'block.pasterdream.dark_cloud': 'Dark Cloud', 'block.pasterdream.thick_cloud': 'Thick Cloud'}
    added = 0
    for k, v in entries.items():
        if k not in ld:
            ld[k] = v
            added += 1
    with open(lang_path, 'w', encoding='utf-8') as f:
        json.dump(ld, f, indent=4, ensure_ascii=False)
    print(f'[OK] {lang}: 添加 {added} 条云朵语言')

# ========== 2. dyedream_vegetation.json: 移除 grass_5 ==========
veg_path = f'{base}/neoforge/biome_modifier/dyedream_vegetation.json'
with open(veg_path, 'r', encoding='utf-8') as f:
    veg = json.load(f)
veg['features'] = [f for f in veg['features'] if f != 'pasterdream:grass_5']
with open(veg_path, 'd', encoding='utf-8') as f:
    json.dump(veg, f, indent=2)
print('[OK] dyedream_vegetation.json: grass_5 已移除')

# ========== 3. 水草：修复seagrass state + 提升密度 ==========
# 修复seagrass：加上 waterlogged=true
sg_path = f'{base}/worldgen/configured_feature/patch_dyedream_seagrass.json'
with open(sg_path, 'r', encoding='utf-8') as f:
    sg = json.load(f)
sg['config']['feature']['feature']['config']['to_place']['state']['Properties'] = {'waterlogged': 'true'}
sg['config']['tries'] = 64
with open(sg_path, 'w', encoding='utf-8') as f:
    json.dump(sg, f, indent=2)
print('[OK] patch_dyedream_seagrass: waterlogged=true, tries 64')

# 密度：lily_pad 8->12, lotus 6->10, seagrass 16->24
for fname, cnt in [('patch_dyedream_lily_pad.json', 12), ('patch_dyedream_lotus.json', 10), ('patch_dyedream_seagrass.json', 24)]:
    fp = f'{base}/worldgen/placed_feature/{fname}'
    with open(fp, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for p in d['placement']:
        if p.get('type') == 'minecraft:count':
            p['count'] = cnt
            break
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)
    print(f'[OK] {fname}: count -> {cnt}')

print('\n[DONE]')