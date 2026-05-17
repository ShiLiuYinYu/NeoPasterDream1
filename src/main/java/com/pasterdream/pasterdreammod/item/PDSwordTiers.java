package com.pasterdream.pasterdreammod.item;

import net.minecraft.tags.BlockTags;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.common.SimpleTier;

/**
 * PasterDream 模组剑类物品的 Tier 常量定义
 * 所有剑类物品共享同一个 SimpleTier 实例，避免重复定义
 */
public final class PDSwordTiers {

    private PDSwordTiers() {}

    /**
     * 基础石级 Tier
     * 用于模组中大部分剑类物品的基础材料等级
     */
    public static final Tier STONE_LEVEL = new SimpleTier(
        BlockTags.INCORRECT_FOR_STONE_TOOL,
        131, 4.0f, 1.0f, 5,
        () -> Ingredient.of(Items.COBBLESTONE)
    );

    /**
     * 基础木级 Tier
     * 用于铜剑等更低等级的剑类物品
     */
    public static final Tier WOOD_LEVEL = new SimpleTier(
        BlockTags.INCORRECT_FOR_WOODEN_TOOL,
        59, 2.0f, 0.0f, 15,
        () -> Ingredient.of(Items.OAK_PLANKS)
    );
}
