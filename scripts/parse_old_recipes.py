"""
解析原模组 (FixPasterDream) 的所有配方 JSON 文件
输出按产物物品 ID 分类的完整配方清单
"""
import os
import json
from collections import defaultdict

# 原模组配方目录
RECIPES_DIR = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1\libs\FixPasterDream-main\src\main\resources\data\pasterdream\recipes"
# 新模组已注册的物品列表（从 PDItems.java 中提取）
NEW_MOD_ITEMS = [
    "titanium_ingot", "dyedream_dust", "magic_stone", "pink_slimeball", "dyedreamquartz",
    "basalt_snail_shell", "black_beetle_carapace", "black_beetle_vocalcord", "blackmetal_grain",
    "blackmetal_ingot", "blackstick", "blue_heart_of_the_sea", "brokennotes_0", "charged_amethyst",
    "coarse_salt", "congeal_wind", "cotton", "dream_aurorian_steel", "dream_meter", "dreamwish",
    "dyedream_base", "dyedream_bud_nugget", "dyedream_corolla", "dyedream_dust_piece", "dyedream_dye",
    "dyedream_nugget", "dyedream_upgrade", "eggdough", "elder_guardian_scale", "enhance_stone_0",
    "enhance_stone_1", "fabric", "flour", "iceshadow_hammer_embryo", "manadust", "moltengold_dust",
    "moltengold_ingot", "moltengold_nugget", "mortar", "nightmare_fuel", "pen_and_ink", "pergamyn",
    "protect_deck", "pulse_windrunner_crystal", "pure_horror", "raw_moltengold", "raw_titanium",
    "reedrod", "rust_black_metal_grain", "ryeseed", "salt", "sculk_heart", "sculk_upgrade",
    "shadow_dungeon_key", "shadow_erosion_axe_embryo", "shadow_erosion_hoe_embryo",
    "shadow_erosion_pickaxe_embryo", "shadow_erosion_shovel_embryo", "shadow_erosion_sword_embryo",
    "shadow_hilt", "shadow_sword_embryo", "silver_bell", "sorbent", "soul_dust", "soul_essence",
    "spool", "star_wish_rod_embryo", "sword_embryo_0", "terrasword_embryo", "titanium_nugget",
    "titanium_upgrade", "unknownnotes_0", "white_corolla", "white_crystal", "white_sword_embryo",
    "wind_iron_ingot", "wind_plant_extract", "windrunner_crystal", "yeast", "dyedream_ingot",
    "glass_cup", "dough", "copper_axe", "copper_shovel", "copper_hoe", "fourleaf_clover_curio",
    "broken_hero_sword", "copper_sword", "creative_sword", "desert_sword", "dyedream_sword_0",
    "dyedream_sword", "grass_sword", "iceshadow_hammer", "moltengold_sword", "shadow_erosion_sword",
    "shadow_sword", "terra_sword", "thermal_dagger", "tide_sword", "titanium_sword",
    "true_desert_sword", "true_grass_sword", "true_moltengold_sword", "true_tide_sword",
    "truest_moltengold_sword", "white_sword", "copper_pickaxe", "dyedream_hammer", "dyedream_pickaxe",
    "meltdream_pickaxe", "moltengold_pickaxe", "shadow_erosion_pickaxe", "titanium_pickaxe",
    "true_moltengold_pickaxe",
    "apple_juice", "bacone_egg", "berry_buncake", "bubble_gum", "candy_cane", "chocolate",
    "chocolate_matcha_cake", "cream_buncake", "dream_cotton_candy", "dyedream_flower_tea",
    "dyedream_fruit_buncake", "dyedream_juice", "dyedream_popsicle", "fried_egg", "gingerbread_man",
    "glow_berry_buncake", "goldenrod_tea", "honey_juice", "jellyfish_jello", "jellyfish_mud",
    "legend_dragon_horn_ice_cream", "light_organ", "melon_buncake", "meltdream_elixir_bottle",
    "milk_glassjar", "odd_bacone_egg", "pineapple_love_sea", "potato_buncake", "pumpkin_buncake",
    "queer_soup", "rage_elixir_0", "ricecake", "sandwich", "stuffed_wafer_cookies", "swiss_roll",
    "uncooked_dyedream_flower_tea", "water_glassjar", "watermelon_juice", "silver_fox_cotton_candy",
    "amber_candy", "blue_dew", "bread_slice", "bubble_tea", "cake_base", "cradle_in_ones_arms",
    "dream_coin_0", "dream_coin_1", "dream_fertilizer", "dyedream_fruit", "dyedream_teleport_crystal",
    "dyedream_perfume", "elixir_bottle", "fig", "glassjar", "guiding_drug", "heart_chocolate_0",
    "heart_chocolate_1", "heart_chocolate_2", "light_moss_phantom_membrane", "meltdream_crystal_0",
    "memento_item_01", "memory_gem_0", "moss_phantom_membrane", "popping_candy", "red_dew_0",
    "shadow_breath", "squeal_wave", "strawberry_heart", "wafer_biscuit",
    "angel_wing", "calais_spice_bottle_curio", "carapax_charm", "ceciliacare_charm", "counter_ring",
    "dark_alllegory_curio", "embryo_belt", "embryo_charm", "embryo_necklace", "embryo_ring",
    "forsakens_wing", "ghost_face_head", "ground_wing", "hithard_0_ring", "hithard_1_ring",
    "machine_wing", "pale_boneneedle", "red_dew_0_ring", "red_dew_1_ring", "red_dew_2_ring",
    "red_dew_3_ring", "sea_charm", "wind_knight_flag", "wings_of_fang",
    "allkinds_ring", "boboji_curio", "bright_butterfly_curio", "cross_necklace", "degenerate_bodys",
    "dream_traveler_belt", "duke_coin_curio", "endeye_charm", "evasion_cloak", "feather_necklace",
    "fire_0_necklace", "garland", "gold_charm", "health_0_necklace", "hiyori_head", "iceshadow_curio",
    "light_butterfly_curio", "nature_belt", "paper_plane", "qym_head", "rabbit_0_necklace",
    "snow_vow_head", "terra_charm", "test_curio", "traveler_belt", "turnback_cloak",
    "white_flower_body", "worldtree_seedpod",
    "sweetdream_disc", "snowfalldream_disc", "aaroncos_disc", "wind_journey_disc",
    "dream_meadow_disc", "dream_heath_disc", "dream_taiga_disc", "dream_delta_disc",
    # BlockItems (方块物品，名称可能与注册名不同)
    "dream_accumulator", "dyedream_desk", "life_crystal", "shadow_chest",
    "dyedream_block", "dyedream_dirt", "dyedream_sand", "dyedream_planks", "dyedream_glass",
    "dyedream_ice", "dyedream_packed_ice", "dyedreamquartz_block", "smooth_dyedreamquartz_block",
    "bricks_dyedreamquartz_block", "chiseled_dyedreamquartz_block", "dyedream_bud_block",
    "pinkslime_block", "icestone", "dyedream_leaves", "dyedream_worldtree_leaves",
    "dyedreamquartz_ore", "dyedreamdust_ore", "amber_candy_ore", "carve_dyedream_glass",
    "gold_carve_dyedream_glass", "dyedream_grass", "dyedream_log", "dyedream_wood",
    "stripped_dyedream_log", "stripped_dyedream_wood", "pillar_dyedreamquartz_block",
    "dyedream_planks_stairs", "dyedream_bud_stairs", "dyedreamquartz_block_stairs",
    "dyedream_planks_slab", "dyedream_bud_slab", "dyedreamquartz_block_slab",
    "dyedream_bud_wall", "dyedreamquartz_block_wall",
    "dyedream_planks_fence", "dyedream_planks_fencegate", "dyedream_planks_door",
    "dyedream_planks_trapdoor", "dyedream_planks_pressure_plate", "dyedream_planks_button",
    "dyedream_glasspane", "carve_dyedream_glasspane", "gold_carve_dyedream_glasspane",
    "dyedream_lartern", "dyedream_planks_pane",
    "pinkagaric_0", "pinkagaric_1", "pinkagaric_2", "pinkagaric_3",
    "dyedream_bud_0", "dyedream_bud_1", "dyedream_bud_2", "ice_bud_0",
    "dyedream_lily_pad", "dyedream_lotus", "dyedream_seagrass", "dyedream_sapling", "dyedream_crack",
    "cloud", "dark_cloud", "thick_cloud",
    "flower_1", "flower_2", "flower_3", "flower_5", "flower_6", "flower_7", "flower_8", "flower_9",
    "flower_10", "flower_11", "flower_12", "flower_13", "flower_14", "flower_15", "flower_16",
    "flower_17", "flower_18",
    "grass_1", "grass_2", "grass_3", "grass_4", "grass_5", "grass_6", "grass_7", "grass_8",
    "grass_9", "grass_10", "grass_11", "grass_12", "grass_13", "grass_14", "grass_15",
]

# 新模组中对应方块的不同注册名映射
BLOCK_REGISTRY_NAMES = {
    # 方块类型: 对应的物品注册名（有时是 pasterdream:xxx 形式）
    "dyedream_block": "pasterdream:dyedream_block",
    "dyedream_planks": "pasterdream:dyedream_planks",
    "dyedream_glass": "pasterdream:dyedream_glass",
    "dyedream_ice": "pasterdream:dyedream_ice",
    "dyedreamquartz_block": "pasterdream:dyedreamquartz_block",
    "dyedream_bud_block": "pasterdream:dyedream_bud_block",
    "pinkslime_block": "pasterdream:pinkslime_block",
    "icestone": "pasterdream:icestone",
    "dyedream_leaves": "pasterdream:dyedream_leaves",
    "dyedreamquartz_ore": "pasterdream:dyedreamquartz_ore",
    "dyedreamdust_ore": "pasterdream:dyedreamdust_ore",
    "dyedream_sapling": "pasterdream:dyedream_sapling",
    "dyedream_log": "pasterdream:dyedream_log",
    "dyedream_wood": "pasterdream:dyedream_wood",
    "stripped_dyedream_log": "pasterdream:stripped_dyedream_log",
    "stripped_dyedream_wood": "pasterdream:stripped_dyedream_wood",
    "dyedream_planks_stairs": "pasterdream:dyedream_planks_stairs",
    "dyedream_planks_slab": "pasterdream:dyedream_planks_slab",
    "dyedream_planks_fence": "pasterdream:dyedream_planks_fence",
    "dyedream_planks_fencegate": "pasterdream:dyedream_planks_fencegate",
    "dyedream_planks_door": "pasterdream:dyedream_planks_door",
    "dyedream_planks_trapdoor": "pasterdream:dyedream_planks_trapdoor",
    "dyedream_planks_pressure_plate": "pasterdream:dyedream_planks_pressure_plate",
    "dyedream_planks_button": "pasterdream:dyedream_planks_button",
    "dyedream_glasspane": "pasterdream:dyedream_glasspane",
    "dyedream_lartern": "pasterdream:dyedream_lartern",
    "pillar_dyedreamquartz_block": "pasterdream:pillar_dyedreamquartz_block",
}

def parse_recipe_json(filepath):
    """解析单个配方 JSON 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return None, str(e)

    recipe_type = data.get("type", "unknown")

    # 提取结果物品（兼容 MCreator 格式：result 可能是字符串或对象）
    result_id = None
    result_count = data.get("count", 1)  # 部分旧版配方 count 在顶层
    result = data.get("result", {})
    if isinstance(result, str):
        result_id = result
    elif isinstance(result, dict):
        result_id = result.get("item") or result.get("id")
        result_count = result.get("count", result_count)

    # 提取材料
    ingredients = []
    if "ingredients" in data:
        for ing in data["ingredients"]:
            if isinstance(ing, dict):
                item_id = ing.get("item") or ing.get("tag")
                ingredients.append(item_id)
    elif "key" in data:
        for key_char, key_data in data["key"].items():
            if isinstance(key_data, dict):
                item_id = key_data.get("item") or key_data.get("tag")
                if item_id not in ingredients:
                    ingredients.append(item_id)
    elif "ingredient" in data:
        ing = data["ingredient"]
        if isinstance(ing, dict):
            item_id = ing.get("item") or ing.get("tag")
            ingredients.append(item_id)
    # Smithing 配方
    if "base" in data:
        base = data.get("base", {})
        if isinstance(base, dict):
            ingredients.append(f"base:{base.get('item', '?')}")
    if "addition" in data:
        addition = data.get("addition", {})
        if isinstance(addition, dict):
            ingredients.append(f"addition:{addition.get('item', '?')}")
    if "template" in data:
        template = data.get("template", {})
        if isinstance(template, dict):
            ingredients.append(f"template:{template.get('item', '?')}")

    # 提取烧炼经验/时间
    experience = data.get("experience")
    cooking_time = data.get("cookingtime")

    # 提取 Pattern
    pattern = data.get("pattern")

    return {
        "type": recipe_type,
        "result_id": result_id,
        "result_count": result_count,
        "ingredients": ingredients,
        "experience": experience,
        "cooking_time": cooking_time,
        "pattern": pattern,
    }, None


def extract_item_name(item_id):
    """从物品 ID 中提取不含命名空间的部分"""
    if not item_id:
        return None
    if ":" in item_id:
        return item_id.split(":", 1)[1]
    return item_id


def main():
    # 收集所有配方 JSON 文件
    recipe_files = sorted([f for f in os.listdir(RECIPES_DIR) if f.endswith('.json')])
    print(f"找到 {len(recipe_files)} 个配方文件\n")

    # 按产物分类
    by_result = defaultdict(list)
    # 按配方类型分类
    by_type = defaultdict(list)
    # 未解析的文件
    failed = []

    for filename in recipe_files:
        filepath = os.path.join(RECIPES_DIR, filename)
        parsed, error = parse_recipe_json(filepath)
        if error or parsed is None:
            failed.append((filename, error))
            continue

        result_name = extract_item_name(parsed["result_id"]) or "unknown"
        by_result[result_name].append((filename, parsed))
        by_type[parsed["type"]].append((filename, parsed))

    # ====== 输出统计 ======
    print("=" * 70)
    print("📊  配方统计")
    print("=" * 70)
    print(f"  总配方数: {len(recipe_files)}")
    print(f"  成功解析: {len(recipe_files) - len(failed)}")
    print(f"  失败: {len(failed)}")
    if failed:
        for f, err in failed:
            print(f"    ❌ {f}: {err}")

    print(f"\n  配方类型分布:")
    type_names = {
        "minecraft:crafting_shaped": "有序合成",
        "minecraft:crafting_shapeless": "无序合成",
        "minecraft:smelting": "熔炉冶炼",
        "minecraft:blasting": "高炉冶炼",
        "minecraft:smithing_transform": "锻造台转换",
        "minecraft:stonecutting": "切石机",
        "minecraft:campfire_cooking": "营火烹饪",
        "minecraft:smoking": "烟熏炉",
    }
    for rtype in sorted(by_type.keys()):
        count = len(by_type[rtype])
        ch_name = type_names.get(rtype, rtype)
        print(f"    {rtype} ({ch_name}): {count} 个")

    # ====== 输出按产物分类的配方（只显示新模组已持有的物品） ======
    print("\n" + "=" * 70)
    print("🎯 已移植物品 → 对应配方（按产物分类）")
    print("=" * 70)
    matched_count = 0
    for result_name in sorted(by_result.keys()):
        # 检查物品是否在新模组中已注册
        if result_name in NEW_MOD_ITEMS:
            matched_count += 1
            entries = by_result[result_name]
            print(f"\n  ✅ {result_name} ({len(entries)} 个配方)")
            for filename, parsed in entries:
                rtype_short = parsed["type"].split(":")[-1]
                ings = ", ".join(parsed["ingredients"]) if parsed["ingredients"] else "无"
                extras = ""
                if parsed["experience"] is not None:
                    extras += f", exp={parsed['experience']}"
                if parsed["cooking_time"] is not None:
                    extras += f", time={parsed['cooking_time']}"
                print(f"      [{filename}] {rtype_short} → {parsed['result_count']}x{parsed['result_id']}{extras}")
                print(f"        材料: {ings}")
                if parsed.get("pattern"):
                    print(f"        模板: {parsed['pattern']}")

    print(f"\n  共 {matched_count} 个已移植物品有对应的原配方")

    # ====== 输出未移植物品的配方（供参考，用于决定后续移植） ======
    print("\n" + "=" * 70)
    print("⏳ 未移植物品 → 配方摘要（仅列出配方数>0的）")
    print("=" * 70)
    unmatched = []
    for result_name in sorted(by_result.keys()):
        if result_name not in NEW_MOD_ITEMS:
            entries = by_result[result_name]
            types = set(p["type"] for _, p in entries)
            unmatched.append((result_name, len(entries), types))
    for name, count, types in unmatched:
        print(f"  {name}: {count} 个配方 ({', '.join(types)})")

    # ====== 输出未移植物品的切石机配方摘要 ======
    stonecutting_unmatched = {}
    for result_name in sorted(by_result.keys()):
        if result_name not in NEW_MOD_ITEMS:
            entries = by_result[result_name]
            for filename, parsed in entries:
                if parsed["type"] == "minecraft:stonecutting":
                    ings = ", ".join(parsed["ingredients"])
                    if result_name not in stonecutting_unmatched:
                        stonecutting_unmatched[result_name] = set()
                    stonecutting_unmatched[result_name].add(ings)
    print(f"\n⏳ 未移植且涉及切石机的方块材料类: {len(stonecutting_unmatched)} 种")
    for name in sorted(stonecutting_unmatched.keys()):
        print(f"  {name}")


if __name__ == "__main__":
    main()