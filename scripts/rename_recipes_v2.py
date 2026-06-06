"""
配方文件批量重命名脚本 v2 - 安全版
处理已存在文件名冲突，使用临时目录避免覆盖
"""
import json, os, re, shutil, tempfile

recipe_dir = r'c:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\data\pasterdream\recipe'

files = [f for f in os.listdir(recipe_dir) if f.endswith('.json')]

# Step 1: 解析所有配方，生成新文件名映射
rename_map = {}
new_name_counts = {}

for fname in sorted(files):
    fpath = os.path.join(recipe_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    recipe_type = data.get('type', '')
    result_id = data.get('result', {}).get('id', '') or data.get('result', '')
    
    if ':' in str(result_id):
        result_name = result_id.split(':')[-1]
    else:
        result_name = str(result_id) if result_id else 'unknown'
    
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
    
    type_map = {
        'minecraft:stonecutting': '_stonecutting',
        'minecraft:smelting': '_smelting',
        'minecraft:blasting': '_blasting',
        'minecraft:campfire_cooking': '_campfire',
        'minecraft:smoking': '_smoking',
    }
    suffix = type_map.get(recipe_type, '')
    
    if ingredient_names and recipe_type in type_map:
        new_name = f'{result_name}_from_{ingredient_names[0]}{suffix}'
    elif ingredient_names and not suffix:
        new_name = f'{result_name}_from_{ingredient_names[0]}'
    else:
        new_name = result_name
    
    new_name = new_name.replace('/', '_').replace(' ', '_') + '.json'
    rename_map[fname] = new_name
    new_name_counts[new_name] = new_name_counts.get(new_name, 0) + 1

# Step 2: 处理重名冲突
final_map = {}
counter = {}
for fname in sorted(files):
    new_name = rename_map[fname]
    if new_name_counts[new_name] > 1:
        idx = counter.get(new_name, 0) + 1
        counter[new_name] = idx
        base = new_name.replace('.json', '')
        final_map[fname] = f'{base}_{idx}.json'
    else:
        final_map[fname] = new_name

# Step 3: 检测冲突（新文件名是否与已有文件冲突）
existing_files = set(files)
safe_rename_map = {}
for old, new in final_map.items():
    if old == new:
        continue
    if new in existing_files and old != new:
        # 目标文件已存在！使用中间临时文件名
        temp_name = f'_temp_{old}'
        safe_rename_map[old] = temp_name
        # 把已有的目标文件也重命名
        if new not in [v for v in safe_rename_map.values()]:
            safe_rename_map[new] = new  # 标记，稍后处理
    else:
        safe_rename_map[old] = new

print(f'共 {len(final_map)} 个配方文件')
print(f'其中 {sum(1 for o,n in final_map.items() if o != n)} 个需要重命名')
print()
print('预览新文件名:')
print('=' * 60)

count = 0
for old, new in sorted(final_map.items()):
    if old == new:
        continue
    count += 1
    if count <= 20:
        print(f'  {old:<30} → {new}')
    elif count == 21:
        print(f'  ... 还有 {sum(1 for o,n in final_map.items() if o != n) - 20} 个 ...')

print()
print(f'需要重命名 {count} 个文件')
print(f'确认重命名？(y/n): ', end='')

confirm = input().strip().lower()
if confirm != 'y':
    print('❌ 已取消')
    exit(0)

# Step 4: 安全执行重命名
# 先处理所有需要移动的目标文件（已有的文件先移到temp）
temp_moves = {}
for old, new in final_map.items():
    if old == new:
        continue
    new_path = os.path.join(recipe_dir, new)
    if os.path.exists(new_path) and new != old:
        temp_name = f'_backup_{new}'
        temp_path = os.path.join(recipe_dir, temp_name)
        os.rename(new_path, temp_path)
        temp_moves[temp_name] = new

# 再执行重命名
for old, new in sorted(final_map.items()):
    if old == new:
        continue
    old_path = os.path.join(recipe_dir, old)
    new_path = os.path.join(recipe_dir, new)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

# 最后恢复被覆盖的目标文件（用新的唯一名称）
for temp_name, original_name in temp_moves.items():
    temp_path = os.path.join(recipe_dir, temp_name)
    original_path = os.path.join(recipe_dir, original_name)
    if os.path.exists(temp_path):
        # 目标名已被占用，使用序号后缀
        base = original_name.replace('.json', '')
        idx = 2
        while os.path.exists(os.path.join(recipe_dir, f'{base}_{idx}.json')):
            idx += 1
        new_unique = f'{base}_{idx}.json'
        os.rename(temp_path, os.path.join(recipe_dir, new_unique))
        print(f'  ⚠️  {original_name} → {new_unique} (原文件冲突)')

print()
print(f'✅ 重命名完成！共处理 {count} 个文件')