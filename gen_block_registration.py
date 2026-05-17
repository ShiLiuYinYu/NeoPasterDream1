"""
生成 PDBlocks.java 和 PDItems.java 的批量花草注册代码
"""

# 单格花（使用 DyedreamFlowerBlock）
SINGLE_FLOWERS = [1, 2, 3, 5, 6, 8, 9, 13, 14, 15, 16, 17]
# 双层花（使用 DyedreamDoublePlantBlock）
DOUBLE_FLOWERS = [7, 10, 11, 12, 18]
# 单格草（使用 DyedreamFlowerBlock）
SINGLE_GRASS = [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14]
# 双层草（使用 DyedreamDoublePlantBlock）
DOUBLE_GRASS = [4, 10, 15]


def gen_pdblocks_code():
    lines = []
    lines.append("    // ==================== 染梦花草（移植自原版模组） ====================")
    lines.append("")
    lines.append("    private static BlockBehaviour.Properties flowerProps() {")
    lines.append("        return BlockBehaviour.Properties.of()")
    lines.append("                .mapColor(MapColor.PLANT)")
    lines.append("                .sound(SoundType.GRASS)")
    lines.append("                .instabreak()")
    lines.append("                .noCollission()")
    lines.append("                .offsetType(BlockBehaviour.OffsetType.XZ)")
    lines.append("                .pushReaction(PushReaction.DESTROY);")
    lines.append("    }")
    lines.append("")
    lines.append("    private static BlockBehaviour.Properties doublePlantProps() {")
    lines.append("        return BlockBehaviour.Properties.of()")
    lines.append("                .mapColor(MapColor.PLANT)")
    lines.append("                .sound(SoundType.GRASS)")
    lines.append("                .instabreak()")
    lines.append("                .noCollission()")
    lines.append("                .offsetType(BlockBehaviour.OffsetType.XZ)")
    lines.append("                .pushReaction(PushReaction.DESTROY);")
    lines.append("    }")
    lines.append("")
    lines.append("    // ========== 单格花（DyedreamFlowerBlock） ==========")
    for i in SINGLE_FLOWERS:
        name = f"flower_{i}"
        const_name = f"FLOWER_{i}"
        lines.append(f"    public static final DeferredBlock<DyedreamFlowerBlock> {const_name} = BLOCKS.registerBlock(\"{name}\",")
        lines.append(f"            p -> new DyedreamFlowerBlock(() -> MobEffects.HUNGER, 100, p), flowerProps());")
    lines.append("")
    lines.append("    // ========== 双层花（DyedreamDoublePlantBlock） ==========")
    for i in DOUBLE_FLOWERS:
        name = f"flower_{i}"
        const_name = f"FLOWER_{i}"
        lines.append(f"    public static final DeferredBlock<DyedreamDoublePlantBlock> {const_name} = BLOCKS.registerBlock(\"{name}\",")
        lines.append(f"            p -> new DyedreamDoublePlantBlock(p), doublePlantProps());")
    lines.append("")
    lines.append("    // ========== 单格草（DyedreamFlowerBlock） ==========")
    for i in SINGLE_GRASS:
        name = f"grass_{i}"
        const_name = f"GRASS_{i}"
        lines.append(f"    public static final DeferredBlock<DyedreamFlowerBlock> {const_name} = BLOCKS.registerBlock(\"{name}\",")
        lines.append(f"            p -> new DyedreamFlowerBlock(() -> MobEffects.MOVEMENT_SLOWDOWN, 100, p), flowerProps());")
    lines.append("")
    lines.append("    // ========== 双层草（DyedreamDoublePlantBlock） ==========")
    for i in DOUBLE_GRASS:
        name = f"grass_{i}"
        const_name = f"GRASS_{i}"
        lines.append(f"    public static final DeferredBlock<DyedreamDoublePlantBlock> {const_name} = BLOCKS.registerBlock(\"{name}\",")
        lines.append(f"            p -> new DyedreamDoublePlantBlock(p), doublePlantProps());")
    return "\n".join(lines)


def gen_pditems_code():
    lines = []
    lines.append("    // ==================== 染梦花草 BlockItem ====================")
    all_flowers = sorted(SINGLE_FLOWERS + DOUBLE_FLOWERS)
    for i in all_flowers:
        name = f"flower_{i}"
        const_name = f"FLOWER_{i}"
        lines.append(f"    public static final DeferredItem<BlockItem> {const_name} = ITEMS.registerSimpleBlockItem(\"{name}\", PDBlocks.{const_name});")
    all_grass = sorted(SINGLE_GRASS + DOUBLE_GRASS)
    for i in all_grass:
        name = f"grass_{i}"
        const_name = f"GRASS_{i}"
        lines.append(f"    public static final DeferredItem<BlockItem> {const_name} = ITEMS.registerSimpleBlockItem(\"{name}\", PDBlocks.{const_name});")
    return "\n".join(lines)


print("=== PDBlocks.java 注册代码 ===")
print(gen_pdblocks_code())
print("\n\n=== PDItems.java 注册代码 ===")
print(gen_pditems_code())