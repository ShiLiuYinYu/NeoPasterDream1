"""
配方文件批量重命名脚本 v3 - 最安全版
先把所有文件移到 temp 目录，再移回来，彻底避免冲突
"""
import json, os, shutil

recipe_dir = r'c:\Users\97128\Documents\GitHub\NeoPasterDream1\src\main\resources\data\pasterdream\recipe'
temp_dir = os.path.join(recipe_dir, '_temp_rename')

# Step 1: 创建临时目录
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

# Step 2: 解析所有配方
files = [f for f in os.listdir(recipe_dir) if f.endswith('.json') and not f.startswith('_')]

type_map = {
    'minecraft:stonecutting': '_stonecutting',
    'minecraft:smelting': '_smelting',
    'minecraft:blasting': '_blasting',
    'minecraft:campfire_cooking': '_campfire',
    'minecraft:smoking': '_smoking',
}

rename_map = {}
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
    
    suffix = type_map.get(recipe_type, '')
    
    if ingredient_names and recipe_type in type_map:
        new_name = f'{result_name}_from_{ingredient_names[0]}{suffix}'
    elif ingredient_names and not suffix:
        new_name = f'{result_name}_from_{ingredient_names[0]}'
    else:
        new_name = result_name
    
    new_name = new_name.replace('/', '_').replace(' ', '_') + '.json'
    rename_map[fname] = new_name

# Step 3: 处理重名
counter = {}
new_name_counts = {}
for new_name in rename_map.values():
    new_name_counts[new_name] = new_name_counts.get(new_name, 0) + 1

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

# Step 4: 显示预览
renames = [(o, n) for o, n in sorted(final_map.items()) if o != n]
no_changes = [(o, n) for o, n in sorted(final_map.items()) if o == n]

print(f'共 {len(files)} 个配方文件')
print(f'无需改名: {len(no_changes)} 个')
print(f'需要改名: {len(renames)} 个')
print()

if renames:
    print('更改预览 (前30个):')
    print('=' * 70)
    for i, (old, new) in enumerate(renames[:30]):
        print(f'  {old:<30} → {new}')
    if len(renames) > 30:
        print(f'  ... 还有 {len(renames) - 30} 个 ...')
    
    print()
    print(f'确认执行重命名？(y/n): ', end='')
    confirm = input().strip().lower()
    if confirm != 'y':
        print('❌ 已取消')
        shutil.rmtree(temp_dir)
        exit(0)
    
    # Step 5: 安全的批量重命名
    # 5a. 先全部移到 temp
    moved_count = 0
    for fname in files:
        src = os.path.join(recipe_dir, fname)
        dst = os.path.join(temp_dir, fname)
        shutil.move(src, dst)
        moved_count += 1
    print(f'📦 已移动 {moved_count} 个文件到临时目录')
    
    # 5b. 从 temp 用新名称移回来
    restored_count = 0
    for old_name, new_name in sorted(final_map.items()):
        src = os.path.join(temp_dir, old_name)
        dst = os.path.join(recipe_dir, new_name)
        if os.path.exists(src):
            shutil.move(src, dst)
            restored_count += 1
    
    # 清理 temp
    shutil.rmtree(temp_dir)
    
    print(f'📋 已完成 {restored_count} 个文件重命名！')
    print(f'   ({len(no_changes)} 个保持不变)')
    
    # 检查是否有文件遗漏
    final_files = [f for f in os.listdir(recipe_dir) if f.endswith('.json')]
    still_numbered = [f for f in final_files if any(f.startswith(p) for p in ['crafting_', 'smelting_', 'smithing_', 'stonecutting_', 'crafying_', 'cooking_'])]
    if still_numbered:
        print(f'⚠️  仍有 {len(still_numbered)} 个编号文件未被重命名！')
        for f in still_numbered[:10]:
            print(f'    {f}')
    else:
        print(f'🎉 所有文件已重命名完毕！')

# 列出新文件名
print()
print('新文件列表预览 (前20个):')
new_files = sorted([final_map[f] for f in files])
for f in new_files[:20]:
    print(f'  {f}')
if len(new_files) > 20:
    print(f'  ... 共 {len(new_files)} 个')