"""
生成配方详情审查报告 —— 输出原始配方的完整内容
按产物分组，并标记是否已移植
"""
import os
import json
from collections import defaultdict

RECIPES_DIR = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1\libs\FixPasterDream-main\src\main\resources\data\pasterdream\recipes"
OUTPUT_FILE = r"c:\Users\97128\Documents\GitHub\NeoPasterDream1\scripts\recipe_detail_report.txt"

# ==================== 已移植物品列表（简化版） ====================
PORTED_ITEMS = {
    # 材料类
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
    "shadow_dungeon_key", "shadow_hilt", "silver_bell", "sorbent", "soul_dust", "soul_essence",
    "spool", "star_wish_rod_embryo", "sword_embryo_0", "terrasword_embryo", "titanium_nugget",
    "titanium_upgrade", "unknownnotes_0", "white_corolla", "white_crystal", "white_sword_embryo",
    "wind_iron_ingot", "wind_plant_extract", "windrunner_crystal", "yeast", "dyedream_ingot",
    "glass_cup", "dough", "copper_axe", "copper_shovel", "copper_hoe", "fourleaf_clover_curio",
    "broken_hero_sword",
    # 阴影侵蚀工具胚胎
    "shadow_erosion_axe_embryo", "shadow_erosion_hoe_embryo", "shadow_erosion_pickaxe_embryo",
    "shadow_erosion_shovel_embryo", "shadow_erosion_sword_embryo", "shadow_sword_embryo",
    # 剑类
    "copper_sword", "creative_sword", "desert_sword", "dyedream_sword_0", "dyedream_sword",
    "grass_sword", "iceshadow_hammer", "moltengold_sword", "shadow_erosion_sword", "shadow_sword",
    "terra_sword", "thermal_dagger", "tide_sword", "titanium_sword", "true_desert_sword",
    "true_grass_sword", "true_moltengold_sword", "true_tide_sword", "truest_moltengold_sword",
    "white_sword",
    # 工具类
    "copper_pickaxe", "dyedream_hammer", "dyedream_pickaxe", "meltdream_pickaxe",
    "moltengold_pickaxe", "shadow_erosion_pickaxe", "titanium_pickaxe", "true_moltengold_pickaxe",
    # 食物类
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
    # Curio饰品
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
    # 唱片
    "sweetdream_disc", "snowfalldream_disc", "aaroncos_disc", "wind_journey_disc",
    "dream_meadow_disc", "dream_heath_disc", "dream_taiga_disc", "dream_delta_disc",
    # 已有配方 JSON 的方块
    "dyedream_block", "dyedream_planks", "dyedream_glass", "dyedream_ice",
    "dyedreamquartz_block", "smooth_dyedreamquartz_block", "bricks_dyedreamquartz_block",
    "chiseled_dyedreamquartz_block", "pillar_dyedreamquartz_block",
    "dyedream_bud_block", "pinkslime_block", "icestone",
    "dyedream_planks_stairs", "dyedream_bud_stairs", "dyedreamquartz_block_stairs",
    "dyedream_planks_slab", "dyedream_bud_slab", "dyedreamquartz_block_slab",
    "dyedream_bud_wall", "dyedreamquartz_block_wall",
    "dyedream_planks_fence", "dyedream_planks_fencegate", "dyedream_planks_door",
    "dyedream_planks_trapdoor", "dyedream_planks_pressure_plate", "dyedream_planks_button",
    "dyedream_glasspane", "carve_dyedream_glasspane", "gold_carve_dyedream_glasspane",
    "dyedream_lartern", "dyedream_planks_pane",
}


def extract_item_id(item_id):
    if not item_id:
        return None
    if ":" in item_id:
        return item_id.split(":", 1)[1]
    return item_id

def parse_recipe(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return None

    recipe_type = data.get("type", "unknown")
    result_id = None
    result_count = data.get("count", 1)
    result = data.get("result", {})
    if isinstance(result, str):
        result_id = result
    elif isinstance(result, dict):
        result_id = result.get("item") or result.get("id")
        result_count = result.get("count", result_count)

    ingredients = []
    if "ingredients" in data:
        for ing in data["ingredients"]:
            if isinstance(ing, dict):
                ingredients.append(ing.get("item") or ing.get("tag") or "?")
    elif "key" in data:
        for k, v in data["key"].items():
            if isinstance(v, dict):
                ingredients.append(f"'{k}': {v.get('item') or v.get('tag') or '?'}")
    elif "ingredient" in data:
        ing = data["ingredient"]
        if isinstance(ing, dict):
            ingredients.append(ing.get("item") or ing.get("tag") or "?")

    if "base" in data:
        b = data["base"]
        ingredients.append(f"base:{b.get('item','?')}" if isinstance(b, dict) else "base:?")
    if "addition" in data:
        a = data["addition"]
        ingredients.append(f"add:{a.get('item','?')}" if isinstance(a, dict) else "add:?")
    if "template" in data:
        t = data["template"]
        ingredients.append(f"tmpl:{t.get('item','?')}" if isinstance(t, dict) else "tmpl:?")

    return {
        "type": recipe_type,
        "result_id": result_id,
        "result_count": result_count,
        "ingredients": ingredients,
        "pattern": data.get("pattern"),
        "experience": data.get("experience"),
        "cooking_time": data.get("cookingtime"),
    }


def format_recipe_type(t):
    names = {
        "minecraft:crafting_shaped": "🛠️ 有序合成",
        "minecraft:crafting_shapeless": "🔄 无序合成",
        "minecraft:smelting": "🔥 熔炉",
        "minecraft:blasting": "💥 高炉",
        "minecraft:smithing_transform": "🔧 锻造台",
        "minecraft:stonecutting": "🔪 切石机",
        "minecraft:campfire_cooking": "🔥 营火",
        "minecraft:smoking": "💨 烟熏炉",
    }
    return names.get(t, t)


def main():
    files = sorted([f for f in os.listdir(RECIPES_DIR) if f.endswith('.json')])

    # 按产物分组
    by_result = defaultdict(list)
    for fname in files:
        parsed = parse_recipe(os.path.join(RECIPES_DIR, fname))
        if parsed:
            rid = extract_item_id(parsed["result_id"]) or "unknown"
            by_result[rid].append((fname, parsed))

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write("=" * 90 + "\n")
        out.write("  📋 原模组配方详情审查报告\n")
        out.write(f"  总配方数: {len(files)}  |  涉及物品数: {len(by_result)}\n")
        out.write("=" * 90 + "\n\n")

        # A) 已移植 → 按产物排序
        out.write("=" * 90 + "\n")
        out.write("  ✅ 已移植物品 → 配方详情\n")
        out.write("=" * 90 + "\n")
        ported_count = 0
        for result_name in sorted(by_result.keys()):
            if result_name not in PORTED_ITEMS:
                continue
            ported_count += 1
            entries = by_result[result_name]
            out.write(f"\n{'─' * 90}\n")
            out.write(f"  📦 {result_name}  |  {len(entries)} 个配方(们)\n")
            out.write(f"{'─' * 90}\n")
            for fname, p in sorted(entries, key=lambda x: x[1]["type"]):
                out.write(f"\n  📄 {fname}\n")
                out.write(f"     类型: {format_recipe_type(p['type'])}  |  产物: {p['result_count']}x {p['result_id']}\n")
                if p.get("pattern"):
                    out.write(f"     模板: {p['pattern']}\n")
                for ing in p["ingredients"]:
                    out.write(f"     材料: {ing}\n")
                if p.get("experience") is not None:
                    out.write(f"     经验: {p['experience']}  |  时间: {p.get('cooking_time')} tick\n")
            out.write("\n")
        out.write(f"\n  ✅ 共 {ported_count} 个已移植物品\n")

        # B) 未移植 → 按类型汇总
        out.write("\n\n" + "=" * 90 + "\n")
        out.write("  ⏳ 未移植物品 → 配方汇总\n")
        out.write("=" * 90 + "\n")
        unmatched = defaultdict(list)
        for result_name in sorted(by_result.keys()):
            if result_name in PORTED_ITEMS:
                continue
            entries = by_result[result_name]
            for fname, p in entries:
                unmatched[result_name].append((fname, p))

        # 按类型分组
        by_category = defaultdict(list)
        for rname in sorted(unmatched.keys()):
            types = set(p["type"] for _, p in unmatched[rname])
            by_category[", ".join(sorted(types))].append(rname)

        for cat, items in sorted(by_category.items()):
            out.write(f"\n  📂 配方类型: {cat}  ({len(items)} 种物品)\n")
            for item in items:
                entries = unmatched[item]
                total_recipes = len(entries)
                materials = set()
                for _, p in entries:
                    for ing in p["ingredients"]:
                        materials.add(ing)
                out.write(f"    ├ {item} ({total_recipes} 配方)  材料: {', '.join(sorted(materials))}\n")
            out.write(f"  {'─' * 85}\n")

        # C) 原始完整内容
        out.write("\n\n" + "=" * 90 + "\n")
        out.write("  📜 完整原始配方内容（按文件名排序）\n")
        out.write("=" * 90 + "\n\n")
        for fname in files:
            p = parse_recipe(os.path.join(RECIPES_DIR, fname))
            if not p:
                out.write(f"  ❌ {fname}: 解析失败\n\n")
                continue
            rid = extract_item_id(p["result_id"]) or "???"
            mark = "✅" if rid in PORTED_ITEMS else "⏳"
            out.write(f"  {mark} {fname}\n")
            out.write(f"     类型={format_recipe_type(p['type'])} 产物={p['result_count']}x {p['result_id']}\n")
            if p.get("pattern"):
                out.write(f"     模板={p['pattern']}\n")
            for ing in p["ingredients"]:
                out.write(f"     材料={ing}\n")
            if p.get("experience") is not None:
                out.write(f"     经验={p['experience']} 时间={p.get('cooking_time')}\n")
            out.write("\n")

    print(f"报告已生成: {OUTPUT_FILE}")
    print(f"共 {len(files)} 个配方, {len(by_result)} 种产物")
    print(f"已移植: {ported_count} 种物品")

if __name__ == "__main__":
    main()