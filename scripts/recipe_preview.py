"""
配方审查助手 —— 展示随机配方预览 + 列出有问题的配方
"""
import os
import json
import random
import re
from collections import defaultdict

BASE_DIR = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1"
RECIPE_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "data", "pasterdream", "recipe")
PD_PATH = os.path.join(BASE_DIR, "src", "main", "java",
                       "com", "pasterdream", "pasterdreammod", "registry", "PDItems.java")

# 加载已注册物品
def load_ported_items():
    items = set()
    if os.path.exists(PD_PATH):
        with open(PD_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        patterns = [
            r'register\("(\w+)"',
            r'registerSimpleItem\("(\w+)"',
            r'registerSimpleBlockItem\("(\w+)"',
            r'simpleItem\("(\w+)"',
            r'foodItem\("(\w+)"',
            r'toolItem\("(\w+)"',
            r'curioItem\("(\w+)"',
            r'registerCustom\("(\w+)"',
            r'registerBlockItem\("(\w+)"',
        ]
        for pat in patterns:
            for m in re.finditer(pat, content):
                items.add(m.group(1))
    return items

def check_item_id(item_id, ported_items):
    """检查物品是否已注册"""
    if not item_id:
        return "空的物品 ID"
    if ":" in item_id:
        ns, name = item_id.split(":", 1)
        if ns == "minecraft":
            return None  # 原版物品总有效
        if ns in ("forge", "c"):
            return None  # 标签
        if ns == "pasterdream":
            # 去除 NBT/组件后缀
            base_name = name.split("[")[0].split("{")[0]
            if base_name not in ported_items:
                return f"未注册: {item_id}"
        else:
            return f"外部模组: {item_id}"
    return None

TYPE_NAMES = {
    "minecraft:crafting_shaped": "🛠️ 有序合成",
    "minecraft:crafting_shapeless": "🔄 无序合成",
    "minecraft:smelting": "🔥 熔炉冶炼",
    "minecraft:blasting": "💥 高炉冶炼",
    "minecraft:smithing_transform": "🔧 锻造台转换",
    "minecraft:stonecutting": "🔪 切石机加工",
    "minecraft:campfire_cooking": "🔥 营火烹饪",
    "minecraft:smoking": "💨 烟熏烹饪",
}

def main():
    ported_items = load_ported_items()
    files = sorted(os.listdir(RECIPE_DIR))
    
    warning_files = []
    clean_files = []
    
    # 扫描所有配方
    for fname in files:
        if not fname.endswith('.json'):
            continue
        fp = os.path.join(RECIPE_DIR, fname)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            continue
        
        # 收集所有引用
        all_refs = []
        
        # result
        result = data.get("result", {})
        if isinstance(result, dict) and "id" in result:
            all_refs.append(result["id"])
        
        # ingredients
        for ing in data.get("ingredients", []):
            if isinstance(ing, dict):
                all_refs.append(ing.get("item") or ing.get("tag") or "")
        
        # ingredient (熔炉/切石机)
        ing = data.get("ingredient", {})
        if isinstance(ing, dict):
            all_refs.append(ing.get("item") or ing.get("tag") or "")
        
        # key (有序合成)
        for k, v in data.get("key", {}).items():
            if isinstance(v, dict):
                all_refs.append(v.get("item") or v.get("tag") or "")
        
        # smithing
        for key in ("base", "addition", "template"):
            v = data.get(key, {})
            if isinstance(v, dict):
                all_refs.append(v.get("item") or v.get("tag") or "")
        
        # 检查
        issues = []
        for ref in all_refs:
            if not ref:
                continue
            err = check_item_id(ref, ported_items)
            if err:
                issues.append((ref, err))
        
        if issues:
            warning_files.append((fname, data.get("type", ""), issues))
        else:
            clean_files.append(fname)
    
    # ==================== 1. 随机预览 ====================
    print("=" * 80)
    print("  📖 随机配方预览")
    print("=" * 80)
    
    sample = random.sample(clean_files, min(8, len(clean_files)))
    for fname in sample:
        with open(os.path.join(RECIPE_DIR, fname), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        rtype = data.get("type", "")
        result = data.get("result", {})
        result_str = f"{result.get('count', 1)}x {result.get('id', '?')}" if isinstance(result, dict) else "?"
        
        print(f"\n  📄 {fname}")
        print(f"  ─{'─' * 70}")
        print(f"     类型: {TYPE_NAMES.get(rtype, rtype)}")
        print(f"     产物: {result_str}")
        print(f"     JSON: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print()
    
    # ==================== 2. 问题文件列表 ====================
    print("=" * 80)
    print(f"  ⚠️  引用了未移植材料的配方文件（共 {len(warning_files)} 个）")
    print("=" * 80)
    
    for fname, rtype, issues in sorted(warning_files):
        result_id = "?"
        with open(os.path.join(RECIPE_DIR, fname), 'r', encoding='utf-8') as f:
            d = json.load(f)
        r = d.get("result", {})
        if isinstance(r, dict):
            result_id = r.get("id", "?")
        
        type_short = TYPE_NAMES.get(rtype, rtype.split(":")[-1])
        print(f"\n  ⚠️  {fname}")
        print(f"     类型: {type_short}  |  产物: {result_id}")
        for ref, err in issues:
            print(f"     材料: {ref}  ← {err}")
    
    print(f"\n{'─' * 80}")
    print(f"  总结: 共 {len(files)} 个配方 | ✅ 干净: {len(clean_files)} | ⚠️ 有警告: {len(warning_files)}")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    random.seed(42)
    main()