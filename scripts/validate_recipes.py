"""
配方 JSON 验证器 —— 检查所有生成的 recipe JSON 文件
1. JSON 语法有效性
2. 结构性检查（必填字段、类型）
3. 物品 ID 引用检查（是否在新模组中注册）
4. 与 Minecraft 1.21 配方格式规范对比
"""
import os
import json
import re

BASE_DIR = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1"
RECIPE_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "data", "pasterdream", "recipe")

# 旧配方目录（用于对比格式差异）
OLD_RECIPE_DIR = os.path.join(BASE_DIR, "libs", "FixPasterDream-main", "src", "main", "resources", "data", "pasterdream", "recipes")

# 从 PDItems.java 提取已注册的物品 ID（简化版）
REGISTERED_ITEMS = set()

def load_pd_items():
    """从 PDItems.java 中提取所有已注册的物品注册名"""
    pd_path = os.path.join(BASE_DIR, "src", "main", "java", "com", "pasterdream", "pasterdreammod", "registry", "PDItems.java")
    if not os.path.exists(pd_path):
        print(f"  ⚠️ 找不到 PDItems.java: {pd_path}")
        return
    
    with open(pd_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配所有 ITEMS.register("xxx", ...) 或 API Builder 或 registerSimpleItem 等模式
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
            REGISTERED_ITEMS.add(m.group(1))
    
    print(f"  从 PDItems.java 提取了 {len(REGISTERED_ITEMS)} 个已注册物品")

def validate_recipe(filepath):
    """验证单个配方文件，返回 (is_valid, issues_list)"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        issues.append(f"❌ JSON 语法错误: {e}")
        return False, issues
    except Exception as e:
        issues.append(f"❌ 读取失败: {e}")
        return False, issues
    
    recipe_type = data.get("type", "")
    if not recipe_type:
        issues.append("❌ 缺少 type 字段")
        return False, issues
    
    # 根据类型检查必填字段
    if recipe_type == "minecraft:crafting_shaped":
        if "pattern" not in data:
            issues.append("❌ 有序合成缺少 pattern")
        if "key" not in data:
            issues.append("❌ 有序合成缺少 key")
        if "result" not in data:
            issues.append("❌ 缺少 result")
        # 检查 pattern 格式
        if "pattern" in data:
            pattern = data["pattern"]
            if not isinstance(pattern, list):
                issues.append("❌ pattern 必须是数组")
            elif len(pattern) > 3:
                issues.append("❌ pattern 行数不能超过 3")
            else:
                for i, row in enumerate(pattern):
                    if len(row) > 3:
                        issues.append(f"❌ pattern 第 {i+1} 行过长 ({len(row)} 字符)")
                    # 检查 key 是否覆盖了 pattern 中的所有字符
                    if "key" in data and row:
                        for ch in row:
                            if ch != ' ' and ch not in data.get("key", {}):
                                issues.append(f"❌ pattern 字符 '{ch}' 未在 key 中定义")
        if "category" not in data:
            issues.append("⚠️ 建议添加 category 字段")
    
    elif recipe_type == "minecraft:crafting_shapeless":
        if "ingredients" not in data:
            issues.append("❌ 无序合成缺少 ingredients")
        elif not isinstance(data["ingredients"], list) or len(data["ingredients"]) == 0:
            issues.append("❌ ingredients 必须为非空数组")
        if "result" not in data:
            issues.append("❌ 缺少 result")
        if "category" not in data:
            issues.append("⚠️ 建议添加 category 字段")
    
    elif recipe_type in ("minecraft:smelting", "minecraft:blasting", "minecraft:campfire_cooking", "minecraft:smoking"):
        if "ingredient" not in data:
            issues.append(f"❌ {recipe_type} 缺少 ingredient")
        if "result" not in data:
            issues.append("❌ 缺少 result")
        if "experience" not in data:
            issues.append("⚠️ 建议添加 experience")
        if "cookingtime" not in data:
            issues.append("⚠️ 建议添加 cookingtime")
    
    elif recipe_type == "minecraft:stonecutting":
        if "ingredient" not in data:
            issues.append("❌ 切石机缺少 ingredient")
        if "result" not in data:
            issues.append("❌ 缺少 result")
    
    elif recipe_type == "minecraft:smithing_transform":
        if "base" not in data:
            issues.append("❌ 锻造台缺少 base")
        if "addition" not in data:
            issues.append("❌ 锻造台缺少 addition")
        if "template" not in data:
            issues.append("❌ 锻造台缺少 template")
        if "result" not in data:
            issues.append("❌ 缺少 result")
    
    else:
        issues.append(f"⚠️ 未知配方类型: {recipe_type}")
    
    # 检查 result 格式
    result = data.get("result")
    if result is not None:
        if isinstance(result, dict):
            if "id" not in result:
                issues.append("❌ result 对象缺少 id 字段")
            else:
                rid = result["id"]
                check_item_id(rid, issues)
        elif isinstance(result, str):
            # 旧格式 result 是字符串
            issues.append("⚠️ result 为字符串（MCreator 旧格式），建议改为对象格式")
            check_item_id(result, issues)
        else:
            issues.append("❌ result 类型不正确")
    
    # 检查所有引用的物品 ID
    for key in ["ingredient", "base", "addition", "template"]:
        val = data.get(key)
        if val and isinstance(val, dict):
            item_id = val.get("item") or val.get("tag")
            if item_id:
                check_item_id(item_id, issues, is_tag="tag" in val)
    
    ingredients = data.get("ingredients", [])
    if isinstance(ingredients, list):
        for ing in ingredients:
            if isinstance(ing, dict):
                item_id = ing.get("item") or ing.get("tag")
                if item_id:
                    check_item_id(item_id, issues, is_tag="tag" in ing)
    
    key_data = data.get("key", {})
    if isinstance(key_data, dict):
        for k, v in key_data.items():
            if isinstance(v, dict):
                item_id = v.get("item") or v.get("tag")
                if item_id:
                    check_item_id(item_id, issues, is_tag="tag" in v)
    
    return len(issues) == 0, issues

def check_item_id(item_id, issues, is_tag=False):
    """检查物品 ID 是否有效"""
    if not item_id:
        issues.append("❌ 空的物品 ID")
        return
    
    # 提取注册名（去掉命名空间）
    if ":" in item_id:
        namespace, name = item_id.split(":", 1)
    else:
        namespace = ""
        name = item_id
    
    # Minecraft 原版物品总是有效的
    if namespace == "minecraft":
        return
    
    # Tag 引用不需要检查注册
    if is_tag:
        return
    
    # Forge 标签
    if namespace == "forge" or namespace == "c":
        return
    
    # 模组物品检查
    if namespace == "pasterdream":
        base_name = name.split("[")[0].split("{")[0]  # 去掉 NBT/组件后缀
        if base_name not in REGISTERED_ITEMS and len(REGISTERED_ITEMS) > 0:
            issues.append(f"⚠️ 可能未注册的物品: {item_id}（未在 PDItems.java 中找到）")
    else:
        # 其他模组的物品
        if namespace not in ("pasterdream", "minecraft", "forge", "c"):
            issues.append(f"ℹ️ 外部模组物品: {item_id}")


def main():
    print("=" * 70)
    print("  🔍 配方 JSON 验证器")
    print("=" * 70)
    
    # 加载已注册物品列表
    load_pd_items()
    print()
    
    # 检查新生成的配方文件
    if not os.path.exists(RECIPE_DIR):
        print(f"❌ 配方目录不存在: {RECIPE_DIR}")
        return
    
    new_files = sorted([f for f in os.listdir(RECIPE_DIR) if f.endswith('.json')])
    print(f"📁 新配方目录: {RECIPE_DIR}")
    print(f"   共 {len(new_files)} 个文件\n")
    
    # 逐个验证
    total_issues = 0
    total_errors = 0
    total_warnings = 0
    clean_count = 0
    
    for fname in new_files:
        filepath = os.path.join(RECIPE_DIR, fname)
        is_valid, issues = validate_recipe(filepath)
        
        if is_valid:
            clean_count += 1
            print(f"  ✅ {fname}")
        else:
            print(f"  ⚠️ {fname}")
            for issue in issues:
                print(f"    {issue}")
                if issue.startswith("❌"):
                    total_errors += 1
                elif issue.startswith("⚠️") or issue.startswith("ℹ️"):
                    total_warnings += 1
            total_issues += len(issues)
    
    # 与旧配方对比
    if os.path.exists(OLD_RECIPE_DIR):
        old_files = set(f for f in os.listdir(OLD_RECIPE_DIR) if f.endswith('.json'))
        new_file_set = set(new_files)
        print(f"\n📊 新旧对比:")
        print(f"   旧配方: {len(old_files)} 个")
        print(f"   新配方: {len(new_files)} 个")
        print(f"   待移植: {len(old_files - new_file_set)} 个")
    
    print(f"\n{'=' * 70}")
    print(f"  验证完毕!")
    print(f"  ✅ 完全正确: {clean_count}/{len(new_files)}")
    print(f"  ❌ 错误数: {total_errors}")
    print(f"  ⚠️ 警告数: {total_warnings}")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()