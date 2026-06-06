"""
配方文件批量重命名脚本
将 crafting_1.json / smelting_2.json 等数字编号文件名
重命名为 {result_item}_from_{source}.json 等有意义名称
"""
import json, os, re

recipe_dir = r'c:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\data\pasterdream\recipe'

# 读取所有配方文件
files = [f for f in os.listdir(recipe_dir) if f.endswith('.json')]

rename_map = {}
duplicate_check = {}

for fname in sorted(files):
    fpath = os.path.join(recipe_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    recipe_type = data.get('type', '')
    result_id = data.get('result', {}).get('id', '') or data.get('result', '')
    
    # 提取 result 的物品名（去掉命名空间）
    if ':' in str(result_id):
        result_name = result_id.split(':')[-1]
    else:
        result_name = str(result_id) if result_id else 'unknown'
    
    # 如果是 stonecutting，结果可能来自 ingredient
    ingredient_names = []
    if 'ingredient' in data:
        ing = data['ingredient']
        if isinstance(ing, dict) and 'id' in ing:
            ing_id = ing['id']
            if ':' in str(ing_id):
                ingredient_names.append(ing_id.split(':')[-1])
        elif isinstance(ing, list):
            for i in ing:
                if isinstance(i, dict) and 'id' in i:
                    ing_id = i['id']
                    if ':' in str(ing_id):
                        ingredient_names.append(ing_id.split(':')[-1])
    
    if recipe_type == 'minecraft:stonecutting':
        suffix = '_stonecutting'
    elif recipe_type == 'minecraft:smelting':
        suffix = '_smelting'
    elif recipe_type == 'minecraft:blasting':
        suffix = '_blasting'
    elif recipe_type == 'minecraft:campfire_cooking':
        suffix = '_campfire'
    elif recipe_type == 'minecraft:smoking':
        suffix = '_smoking'
    else:
        suffix = ''
    
    if ingredient_names and recipe_type in ['minecraft:smelting', 'minecraft:blasting',
                                             'minecraft:campfire_cooking', 'minecraft:smoking',
                                             'minecraft:stonecutting']:
        new_name = f'{result_name}_from_{ingredient_names[0]}{suffix}'
    elif ingredient_names and suffix == '':
        new_name = f'{result_name}_from_{ingredient_names[0]}'
    else:
        new_name = f'{result_name}{suffix}'
    
    new_name = new_name.replace('/', '_').replace(' ', '_')
    new_name = new_name + '.json'
    
    # 处理重名冲突
    if new_name in duplicate_check:
        idx = 2
        while f'{new_name.replace(".json", "")}_{idx}.json' in duplicate_check:
            idx += 1
        new_name = f'{new_name.replace(".json", "")}_{idx}.json'
    
    duplicate_check[new_name] = fname
    rename_map[fname] = new_name

print(f'共 {len(rename_map)} 个配方文件需要重命名')
print('=' * 70)
print(f'{"原始文件名":<25} {"→ 新文件名":<45}')
print('=' * 70)

for old, new in sorted(rename_map.items()):
    print(f'{old:<25} → {new:<45}')

print()
print('确认重命名？(y/n): ', end='')
confirm = input().strip().lower()
if confirm == 'y':
    for old, new in rename_map.items():
        old_path = os.path.join(recipe_dir, old)
        new_path = os.path.join(recipe_dir, new)
        os.rename(old_path, new_path)
    print(f'✅ 已完成 {len(rename_map)} 个文件重命名！')
else:
    print('❌ 已取消重命名')