"""
找出缺失材料的清单
"""
import json, os, re

base_dir = r'c:\Users\97128\Documents\GitHub\NeoPasterDream1'
recipe_dir = os.path.join(base_dir, 'src', 'main', 'resources', 'data', 'pasterdream', 'recipe')

# 读取 PDItems.java
with open(os.path.join(base_dir, 'src', 'main', 'java', 'com', 'pasterdream', 'pasterdreammod', 'registry', 'PDItems.java'), 'r', encoding='utf-8') as f:
    items_code = f.read()

# 读取 PDBlocks.java
with open(os.path.join(base_dir, 'src', 'main', 'java', 'com', 'pasterdream', 'pasterdreammod', 'registry', 'PDBlocks.java'), 'r', encoding='utf-8') as f:
    blocks_code = f.read()

# 提取所有已注册物品名（包括 API 注册模式）
registered = set()
# PDItems 中的 register / registerSimpleItem / registerSimpleBlockItem 模式
for m in re.finditer(r'register\w*\s*\(\s*"(\w+)"', items_code):
    registered.add(m.group(1))
# PDItems 中的 API simpleItem / foodItem / toolItem / curioItem 模式
for m in re.finditer(r'(?:simpleItem|foodItem|toolItem|curioItem)\s*\(\s*"(\w+)"', items_code):
    registered.add(m.group(1))
# PDItems 中的 registerCustom 模式
for m in re.finditer(r'registerCustom\s*\(\s*"(\w+)"', items_code):
    registered.add(m.group(1))
# PDBlocks 中的 register / registerSimpleBlock 模式
for m in re.finditer(r'register\w*\s*\(\s*"(\w+)"', blocks_code):
    registered.add(m.group(1))
# 特殊：从原配方转化脚本中查找已知已注册物品
# 通过原始模组 ID 匹配
known_registered = {
    'titanium_ingot', 'dyedream_dust', 'magic_stone', 'pink_slimeball', 'dyedreamquartz',
    'glass_cup', 'dough', 'copper_axe', 'copper_shovel', 'copper_hoe', 'fourleaf_clover_curio',
    'copper_sword', 'copper_pickaxe', 'broken_hero_sword', 'creative_sword', 'desert_sword',
    'dyedream_sword_0', 'dyedream_sword', 'grass_sword', 'iceshadow_hammer', 'moltengold_sword',
    'shadow_erosion_sword', 'shadow_sword', 'terra_sword', 'thermal_dagger', 'tide_sword',
    'titanium_sword', 'true_desert_sword', 'true_grass_sword', 'true_moltengold_sword',
    'true_tide_sword', 'truest_moltengold_sword', 'white_sword',
    'dyedream_hammer', 'dyedream_pickaxe', 'meltdream_pickaxe', 'moltengold_pickaxe',
    'shadow_erosion_pickaxe', 'titanium_pickaxe', 'true_moltengold_pickaxe',
    'apple_juice', 'honey_juice', 'watermelon_juice', 'sandwich',
    'sweetdream_disc', 'snowfalldream_disc', 'aaroncos_disc', 'wind_journey_disc',
    'dream_meadow_disc', 'dream_heath_disc', 'dream_taiga_disc', 'dream_delta_disc',
}
registered.update(known_registered)

# 原版物品白名单
vanilla_items = {
    'air', 'stone', 'dirt', 'grass_block', 'cobblestone', 'iron_ingot', 'gold_ingot',
    'diamond', 'stick', 'iron_nugget', 'gold_nugget', 'copper_ingot', 'netherite_ingot',
    'redstone', 'coal', 'lapis_lazuli', 'emerald', 'quartz', 'flint', 'bone', 'string',
    'feather', 'gunpowder', 'paper', 'book', 'egg', 'sugar', 'wheat', 'bread',
    'apple', 'potato', 'carrot', 'beetroot', 'pumpkin', 'melon', 'sweet_berries',
    'glow_berries', 'milk_bucket', 'water_bucket', 'lava_bucket', 'bucket',
    'glass', 'glass_pane', 'iron_block', 'gold_block', 'diamond_block',
    'copper_block', 'netherite_block', 'coal_block', 'redstone_block',
    'lapis_block', 'emerald_block', 'quartz_block', 'smooth_quartz',
    'quartz_slab', 'quartz_stairs', 'stone_slab', 'stone_stairs',
    'cobblestone_slab', 'cobblestone_stairs', 'oak_planks', 'spruce_planks',
    'birch_planks', 'jungle_planks', 'acacia_planks', 'dark_oak_planks',
    'mangrove_planks', 'cherry_planks', 'bamboo_planks', 'crimson_planks',
    'warped_planks', 'polished_calcite',
}

# 扫描所有配方，找出缺失材料
unported_by_recipe = {}
unique_unported = set()

for fname in os.listdir(recipe_dir):
    if not fname.endswith('.json'):
        continue
    with open(os.path.join(recipe_dir, fname), 'r', encoding='utf-8') as f:
        data = json.load(f)
    content = json.dumps(data)
    for m in re.finditer(r'"pasterdream:(\w+)"', content):
        item = m.group(1)
        if item not in registered and item not in vanilla_items:
            if item not in unique_unported:
                unique_unported.add(item)
                unported_by_recipe[item] = []
            unported_by_recipe[item].append(fname)

print(f'已注册物品/方块总数: {len(registered)}')
print()
print(f'发现 {len(unique_unported)} 个唯一缺失材料:')
print('=' * 60)

# 分类：物品 vs 方块
maybe_items = []
maybe_blocks = []
for item in sorted(unique_unported):
    if item.endswith('_block') or item.endswith('_ore') or item == 'charged_amethyst_block':
        maybe_blocks.append(item)
    else:
        maybe_items.append(item)

if maybe_blocks:
    print(f'\n📦 可能是方块（需要 PDBlocks 注册）:')
    for item in maybe_blocks:
        recipes = unported_by_recipe[item]
        print(f'  🔴 {item} ({len(recipes)} 个配方)')
        for r in sorted(recipes):
            print(f'       - {r}')

if maybe_items:
    print(f'\n🧩 可能是物品（需要 PDItems 注册）:')
    for item in maybe_items:
        recipes = unported_by_recipe[item]
        print(f'  🔴 {item} ({len(recipes)} 个配方)')
        for r in sorted(recipes):
            print(f'       - {r}')