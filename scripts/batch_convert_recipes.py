"""
批量配方转换脚本
读取原模组 (FixPasterDream) 的旧格式配方 JSON，转换为标准 Minecraft 1.21 格式，
只转换已移植物品的配方，保存到 src/main/resources/data/pasterdream/recipe/

处理格式差异：
  - 旧版: "result": "item_id" 或 "result": {"item": "id", "count": N}
  - 新版: "result": {"id": "item_id", "count": N}
  - 旧版: "count": N 在顶层 → 新版: 在 result 对象内
  - 为 crafting 配方自动添加 category 字段
"""
import os
import json
import re
import shutil
from collections import defaultdict

BASE_DIR = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1"
OLD_RECIPE_DIR = os.path.join(BASE_DIR, "libs", "FixPasterDream-main", "src", "main", "resources", "data", "pasterdream", "recipes")
NEW_RECIPE_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "data", "pasterdream", "recipe")

# 配方类型 → Minecraft 1.21 recipe book category 映射
TYPE_CATEGORY_MAP = {
    "minecraft:crafting_shaped": {
        "equipment": {"sword", "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate",
                      "leggings", "boots", "sword_", "pickaxe_", "axe_", "shovel_", "hoe_",
                      "helmet_", "chestplate_", "leggings_", "boots_", "armor"},
        "building": {"stairs", "slab", "wall", "fence", "fence_gate", "trapdoor", "door",
                     "planks", "block", "bricks", "glass", "pane", "button", "pressure_plate"},
        "redstone": {"redstone", "comparator", "repeater", "piston", "observer", "dispenser",
                     "dropper", "rail", "lamp", "lamp_", "lever"},
        "food": {"cake", "cookie", "bread", "pie", "soup", "stew"},
    },
}

# 默认 category 映射（按物品名关键词）
CATEGORY_KEYWORDS = {
    "building": ["_stairs", "_slab", "_wall", "_fence", "_fence_gate", "_trapdoor", "_door",
                 "_button", "_pressure_plate", "_pane", "_block", "_bricks", "_planks",
                 "dyedream_block", "pinkslime_block", "icestone", "cloud", "glass"],
    "equipment": ["sword", "pickaxe", "axe", "shovel", "hoe", "hammer", "dagger", "helmet",
                  "chestplate", "leggings", "boots", "curio", "ring", "necklace", "charm",
                  "belt", "wing", "cloak", "head"],
    "food": ["juice", "tea", "cake", "cookie", "bread", "pie", "soup", "stew", "buncake",
             "candy", "popsicle", "jello", "chocolate", "sandwich", "egg", "ricecake",
             "wafer", "biscuit", "ice_cream", "elixir", "bottle", "fruit", "juice"],
    "redstone": ["redstone", "comparator", "repeater", "piston", "observer", "dispenser",
                 "dropper", "rail", "lamp"],
}


# ==================== 已移植物品列表（从 PDItems.java 读取） ====================
def load_ported_items():
    """从 PDItems.java 提取所有已注册的物品注册名"""
    pd_path = os.path.join(BASE_DIR, "src", "main", "java",
                           "com", "pasterdream", "pasterdreammod", "registry", "PDItems.java")
    items = set()
    if not os.path.exists(pd_path):
        print(f"  ❌ 找不到 {pd_path}")
        return items

    with open(pd_path, 'r', encoding='utf-8') as f:
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


def is_item_ported(item_id, ported_items):
    """检查物品是否已移植"""
    if not item_id:
        return False
    if ":" in item_id:
        ns, name = item_id.split(":", 1)
        if ns != "pasterdream":
            return True  # minecraft/forge 物品不需要移植
        return name in ported_items
    return True  # 无命名空间默认认为有效


def guess_category(item_id):
    """根据物品名猜测 recipe book category"""
    if not item_id:
        return "misc"
    name = item_id.split(":")[-1].lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in name:
                return cat
    return "misc"


def convert_result(result, top_count):
    """
    转换 result 字段格式
    
    旧格式:
      "result": "pasterdream:xxx"          → 新版: {"id": "pasterdream:xxx", "count": N}
      "result": {"item": "xxx", "count": 1} → 新版: {"id": "xxx", "count": 1}
    
    参数:
      result: 原始 result 字段值
      top_count: 顶层 count 值（旧版可能在此）
    """
    count = top_count or 1
    if isinstance(result, str):
        return {"id": result, "count": count}
    elif isinstance(result, dict):
        result_id = result.get("id") or result.get("item") or result.get("Item", "")
        result_count = result.get("count") or count
        return {"id": result_id, "count": result_count}
    return result


def convert_ingredient(ing):
    """转换单个材料（旧格式可能使用 Item 大写 E）"""
    if not isinstance(ing, dict):
        return ing
    converted = {}
    for key in ("item", "tag", "Item", "Tag"):
        if key in ing:
            target_key = "item" if key.lower() == "item" else "tag"
            converted[target_key] = ing[key]
    return converted


def convert_recipe(data):
    """
    将旧格式配方转换为 Minecraft 1.21 标准格式
    
    返回: (new_data, unported_items_set) 
    """
    new_data = {}
    unported = set()

    # 1. type
    recipe_type = data.get("type", "")
    new_data["type"] = recipe_type

    # 2. category（仅 crafting 类型需要）
    if recipe_type in ("minecraft:crafting_shaped", "minecraft:crafting_shapeless"):
        new_data["category"] = guess_category(
            (data.get("result") or {}).get("item") or
            (data.get("result") if isinstance(data.get("result"), str) else "") or
            ""
        )

    # 3. pattern（有序合成）
    if "pattern" in data:
        new_data["pattern"] = data["pattern"]

    # 4. key（有序合成）
    if "key" in data:
        new_data["key"] = {}
        for k, v in data["key"].items():
            new_data["key"][k] = convert_ingredient(v)

    # 5. ingredients（无序合成）
    if "ingredients" in data:
        new_data["ingredients"] = [convert_ingredient(i) for i in data["ingredients"]]

    # 6. ingredient（熔炉/切石机/营火）
    if "ingredient" in data:
        new_data["ingredient"] = convert_ingredient(data["ingredient"])

    # 7. smithing 配方
    for key in ("base", "addition", "template"):
        if key in data:
            new_data[key] = convert_ingredient(data[key])

    # 8. experience / cookingtime
    for key in ("experience", "cookingtime"):
        if key in data:
            new_data[key] = data[key]

    # 9. result（关键转换）
    top_count = data.get("count", 1)
    old_result = data.get("result", {})
    new_data["result"] = convert_result(old_result, top_count)

    return new_data, unported


def main():
    print("=" * 70)
    print("  🔄 批量配方转换器")
    print("=" * 70)

    # 加载已移植物品
    ported_items = load_ported_items()
    print(f"  ✅ 已移植物品: {len(ported_items)} 个")

    # 检查目录
    if not os.path.exists(OLD_RECIPE_DIR):
        print(f"  ❌ 旧配方目录不存在: {OLD_RECIPE_DIR}")
        return
    os.makedirs(NEW_RECIPE_DIR, exist_ok=True)

    # 读取所有旧配方
    old_files = sorted([f for f in os.listdir(OLD_RECIPE_DIR) if f.endswith('.json')])
    print(f"  📂 旧配方总数: {len(old_files)} 个\n")

    # 统计变量
    converted = 0
    skipped_not_ported = 0
    skipped_already_exists = 0
    errors = []
    ported_skip_reasons = defaultdict(list)

    # 处理每个配方
    for fname in old_files:
        src_path = os.path.join(OLD_RECIPE_DIR, fname)

        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            errors.append((fname, str(e)))
            continue

        # 检查产物是否已移植
        old_result = old_data.get("result", {})
        top_count = old_data.get("count", 1)

        if isinstance(old_result, str):
            result_id = old_result
        elif isinstance(old_result, dict):
            result_id = old_result.get("item") or old_result.get("id")
        else:
            result_id = None

        if not result_id:
            skipped_not_ported += 1
            ported_skip_reasons["无产物 ID"].append(fname)
            continue

        # 提取物品名（不含命名空间）
        if ":" in result_id:
            ns, name = result_id.split(":", 1)
        else:
            ns, name = "", result_id

        # 只有 pasterdream 模组的物品需要检查移植状态
        if ns == "pasterdream" and name not in ported_items:
            skipped_not_ported += 1
            ported_skip_reasons["未移植"].append(f"{fname} → {result_id}")
            continue

        # 检查是否已存在（避免覆盖已有的手动调整过的配方）
        dest_path = os.path.join(NEW_RECIPE_DIR, fname)
        if os.path.exists(dest_path):
            skipped_already_exists += 1
            continue

        # 转换配方
        new_data, _ = convert_recipe(old_data)

        # 保存
        try:
            with open(dest_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            converted += 1
        except IOError as e:
            errors.append((fname, f"写入失败: {e}"))

    # ==================== 输出统计 ====================
    print("=" * 70)
    print("  📊 转换统计")
    print("=" * 70)
    print(f"  ✅ 成功转换:     {converted} 个")
    print(f"  ⏭  已存在跳过:   {skipped_already_exists} 个")
    print(f"  ⏭  未移植跳过:   {skipped_not_ported} 个")
    print(f"  ❌ 错误:         {len(errors)} 个")

    if errors:
        print(f"\n  📋 错误详情:")
        for fname, err in errors[:10]:
            print(f"     ❌ {fname}: {err}")
        if len(errors) > 10:
            print(f"     ... 还有 {len(errors) - 10} 个错误")

    print(f"\n  📋 未移植跳过的配方分类:")
    for reason, files in sorted(ported_skip_reasons.items()):
        print(f"     {reason}: {len(files)} 个")
        for f in files[:5]:
            print(f"       • {f}")
        if len(files) > 5:
            print(f"       ... 还有 {len(files) - 5} 个")

    # 列出新目录的最终文件
    new_files = [f for f in os.listdir(NEW_RECIPE_DIR) if f.endswith('.json')]
    print(f"\n  📂 新配方目录最终共 {len(new_files)} 个文件")

    # 按类型统计
    type_counts = defaultdict(int)
    for fname in new_files:
        fp = os.path.join(NEW_RECIPE_DIR, fname)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                d = json.load(f)
            type_counts[d.get("type", "unknown")] += 1
        except:
            pass
    print(f"  📈 配方类型分布:")
    type_names = {
        "minecraft:crafting_shaped": "有序合成",
        "minecraft:crafting_shapeless": "无序合成",
        "minecraft:smelting": "熔炉",
        "minecraft:blasting": "高炉",
        "minecraft:smithing_transform": "锻造台",
        "minecraft:stonecutting": "切石机",
        "minecraft:campfire_cooking": "营火",
        "minecraft:smoking": "烟熏炉",
    }
    for t, c in sorted(type_counts.items()):
        cn = type_names.get(t, t)
        print(f"     {cn}: {c} 个")

    print(f"\n  ✅ 完成！")


if __name__ == "__main__":
    main()