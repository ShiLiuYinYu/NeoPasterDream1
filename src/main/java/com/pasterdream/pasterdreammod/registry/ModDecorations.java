package com.pasterdream.pasterdreammod.registry;

import com.pasterdream.pasterdreammod.worldgen.IceGateGenerator;
import com.pasterdream.pasterdreammod.worldgen.CloudBubbleGenerator;
import com.pasterdream.pasterdreammod.worldgen.IceArchGenerator;
import com.pasterdream.pasterdreammod.worldgen.FloatingIceGenerator;
import com.pasterdream.pasterdreammod.worldgen.decor.DecorationBuilder;
import com.pasterdream.pasterdreammod.worldgen.decor.DecorationRegistry;
import com.pasterdream.pasterdreammod.worldgen.decor.DecorationType;
import net.minecraft.util.random.SimpleWeightedRandomList;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.blockpredicates.BlockPredicate;
import net.minecraft.world.level.levelgen.feature.stateproviders.BlockStateProvider;
import net.minecraft.world.level.levelgen.feature.stateproviders.WeightedStateProvider;
import net.minecraft.tags.BlockTags;

/**
 * 染梦装饰物注册 —— 使用 WorldDecorationAPI 注册所有多方块装饰物
 * <p>
 * 通过 {@link DecorationBuilder} 的流式 API 配置装饰物参数，
 * 替代原有的分散在各 Feature 类中的自定义生成逻辑。
 * 所有注册会记录到 {@link DecorationRegistry} 中，
 * 用于后续的 JSON 数据文件自动生成。
 */
public class ModDecorations {
    // ==================== 新装饰物（5种） ====================

    /**
     * 注册云泡泡装饰物
     * <p>
     * 在染梦海洋（biome_dyedream_3）海面上空生成由云朵构成的球形结构，
     * 内部中空，最低在海面 2 格以上，最高在海面 20 格。
     * 使用 CUSTOM 类型 CloudBubbleGenerator，球壳厚度 1 格。
     */
    private static void registerCloudBubble() {
        SimpleWeightedRandomList<BlockState> cloudBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.CLOUD.get().defaultBlockState(), 75)
                .add(PDBlocks.THICK_CLOUD.get().defaultBlockState(), 20)
                .add(Blocks.WHITE_WOOL.defaultBlockState(), 5)
                .build();

        DecorationRegistry.registerCustomGenerator("cloud_bubble", new CloudBubbleGenerator());

        DecorationBuilder.create()
                .type(DecorationType.CUSTOM)
                .body(new WeightedStateProvider(cloudBodyList))
                .customGenerator("cloud_bubble")
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.CAVE_AIR, Blocks.WATER))
                .biome("pasterdream:biome_dyedream_3")
                .rarity(1)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("cloud_bubble");
    }

    /**
     * 注册浮冰结构装饰物
     * <p>
     * 在染梦海洋（biome_dyedream_3）海面位置生成扁平碟状浮冰，
     * 上层覆雪，下层浸水，仅使用染梦维度冰系方块。
     * 使用 CUSTOM 类型 + FloatingIceGenerator，在海面高度生成。
     */
    private static void registerFloatingIceMound() {
        SimpleWeightedRandomList<BlockState> bodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 60)
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 40)
                .build();

        DecorationRegistry.registerCustomGenerator("floating_ice_mound", new FloatingIceGenerator());

        DecorationBuilder.create()
                .type(DecorationType.CUSTOM)
                .body(new WeightedStateProvider(bodyList))
                .top(Blocks.SNOW_BLOCK)
                .customGenerator("floating_ice_mound")
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.SNOW_BLOCK, PDBlocks.DYEDREAM_ICE.get(), PDBlocks.DYEDREAM_PACKED_ICE.get(), Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .biome("pasterdream:biome_dyedream_3")
                .rarity(2)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("floating_ice_mound");
    }

    /**
     * 注册冰拱门装饰物
     * <p>
     * 在染梦海洋（biome_dyedream_3）水底向上形成巨大的半圆拱形冰结构，
     * 可露出水面 10~30 格不等。水下由冰系方块构成，
     * 水面上可出现覆雪。
     * 使用 CUSTOM 类型 + IceArchGenerator，余弦曲线生成半圆拱形路径。
     */
    private static void registerIceArch() {
        SimpleWeightedRandomList<BlockState> pillarBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 60)
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 40)
                .build();

        SimpleWeightedRandomList<BlockState> topList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 60)
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 40)
                .build();

        DecorationRegistry.registerCustomGenerator("ice_arch", new IceArchGenerator());

        DecorationBuilder.create()
                .type(DecorationType.CUSTOM)
                .body(new WeightedStateProvider(pillarBodyList))
                .top(new WeightedStateProvider(topList))
                .customGenerator("ice_arch")
                .height(20, 35)
                .gateWidth(30, 50)
                .pillarRadius(4)
                .beamThickness(4)
                .decorationChance(0.25f)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SNOW_BLOCK, Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(false)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(12)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("ice_arch");
    }

    /**
     * 注册冰拱门变种装饰物（损坏版本）
     * <p>
     * 中间出现不同程度的损坏，导致中间弧形结构下落在水面上，
     * 形成由冰雪混合的碎冰渣。由冰拱门约 15% 概率改变而来。
     * 使用 CUSTOM 类型 + IceArchGenerator，更小的尺寸配合碎冰散落效果。
     */
    private static void registerIceArchRuined() {
        SimpleWeightedRandomList<BlockState> pillarBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 60)
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 40)
                .build();

        DecorationRegistry.registerCustomGenerator("ice_arch_ruined", new IceArchGenerator());

        DecorationBuilder.create()
                .type(DecorationType.CUSTOM)
                .body(new WeightedStateProvider(pillarBodyList))
                .customGenerator("ice_arch_ruined")
                .height(15, 25)
                .gateWidth(20, 35)
                .pillarRadius(3)
                .beamThickness(3)
                .decorationChance(0.4f)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SNOW_BLOCK, Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(false)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(35)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("ice_arch_ruined");
    }

    /**
     * 注册染梦冰柱装饰物
     * <p>
     * 在染梦深海（biome_dyedream_deep_ocean）水底冒出海面的冰柱，
     * 使用染梦维度纯冰系方块，嵌入冰蕾，基部散落碎冰。
     * 使用 PILLAR 类型，方形截面锥形柱体从海底向上生长至海面以上。
     */
    private static void registerDyedreamIcePillar() {
        SimpleWeightedRandomList<BlockState> bodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 55)
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 35)
                .add(PDBlocks.ICE_BUD_0.get().defaultBlockState(), 10)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.PILLAR)
                .body(new WeightedStateProvider(bodyList))
                .top(Blocks.SNOW_BLOCK)
                .crystal(0.1f, BlockStateProvider.simple(PDBlocks.ICE_BUD_0.get()))
                .debris(PDBlocks.DYEDREAM_PACKED_ICE.get(), 8, 5)
                .height(12, 25)
                .width(3, 1)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.SNOW_BLOCK, PDBlocks.DYEDREAM_ICE.get(), PDBlocks.DYEDREAM_PACKED_ICE.get(), Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(3)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("dyedream_ice_pillar");
    }

    /**
     * 注册海底冰晶丛装饰物
     * <p>
     * 在染梦深海（biome_dyedream_3）海底散布小型冰晶簇，
     * 由冰蕾和染梦冰块混合构成，稀稀拉拉长在沙地上。
     * 使用 SCATTER 类型，集群大小 6，检测悬空防止漂浮。
     */
    private static void registerIceCrystalCluster() {
        SimpleWeightedRandomList<BlockState> crystalBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.ICE_BUD_0.get().defaultBlockState(), 40)
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 35)
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 25)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.SCATTER)
                .body(new WeightedStateProvider(crystalBodyList))
                .clusterSize(6)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(2)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("ice_crystal_cluster");
    }

    /**
     * 注册冰霜尖刺装饰物
     * <p>
     * 在染梦深海（biome_dyedream_3）海底向上生长的小型冰尖刺，
     * 高度 3~8 格，圆形锥形截面，形成海底冰笋景观。
     * 使用 SPIKE 类型，嵌入少量冰蕾。
     */
    private static void registerFrostSpike() {
        SimpleWeightedRandomList<BlockState> spikeBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 60)
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 40)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.SPIKE)
                .body(new WeightedStateProvider(spikeBodyList))
                .top(Blocks.SNOW_BLOCK)
                .crystal(0.1f, BlockStateProvider.simple(PDBlocks.ICE_BUD_0.get()))
                .height(3, 8)
                .radius(2, 0)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SNOW_BLOCK, Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(3)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("frost_spike");
    }

    /**
     * 注册所有装饰物 —— 供模组初始化阶段调用
     * <p>
     * 包含冰刺（SPIKE）、冰之门（GATE）、方解石之柱（PILLAR）、
     * 坠云团块（BLOB）、粉丁菇巨簇（BLOB）、冰晶花园（SCATTER）等类型的配置。
     */
    public static void register() {
        registerIceSpike();
        registerIceGate();
        registerCalcitePillar();
        registerCloudfallMoundDense();
        registerCloudfallMoundSparse();
        registerIceCrystalGarden();
        registerCoralReef();
        registerCoralReefPink();
        registerIceCrystalSpike();
        registerIcePillar();
        registerUnderwaterIceSpike();
        registerSeaIceMound();
        registerCloudBubble();
        registerFloatingIceMound();
        registerIceArch();
        registerIceArchRuined();
        registerDyedreamIcePillar();
        registerIceCrystalCluster();
        registerFrostSpike();
    }

    /**
     * 注册冰刺装饰物
     * <p>
     * 对应原 IceSpikeFeature + IceSpikeConfiguration，
     * 使用 API 内置的 SPIKE 类型，圆形截面锥形尖刺，
     * 开启悬空检测（checkHang）和区域重叠检测（regionCheck）。
     */
    private static void registerIceSpike() {
        SimpleWeightedRandomList<BlockState> iceBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.ICE.defaultBlockState(), 50)
                .add(Blocks.PACKED_ICE.defaultBlockState(), 35)
                .add(Blocks.BLUE_ICE.defaultBlockState(), 15)
                .build();

        SimpleWeightedRandomList<BlockState> oreList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAMQUARTZ_ORE.get().defaultBlockState(), 1)
                .add(PDBlocks.ICE_BUD_0.get().defaultBlockState(), 1)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.SPIKE)
                .body(new WeightedStateProvider(iceBodyList))
                .top(Blocks.SNOW_BLOCK)
                .crystal(0.2f, new WeightedStateProvider(oreList))
                .height(5, 14)
                .radius(3, 0)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SNOW_BLOCK, Blocks.STONE, Blocks.DIRT, Blocks.GRASS_BLOCK, PDBlocks.DYEDREAM_ICE.get(), PDBlocks.DYEDREAM_PACKED_ICE.get(), PDBlocks.ICESTONE.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_2")
                .rarity(2)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("ice_spike");
    }

    /**
     * 注册冰之门装饰物（完整+倒塌变种合并）
     * <p>
     * 使用 CUSTOM 类型 + IceGateGenerator 自定义生成逻辑。
     * 当两根支柱都能找到坚实地面时 → 完整的双柱+横梁冰门；
     * 当只有一根支柱能找到坚实地面时 → 倒塌变种（倾斜版或断柱版）。
     * <p>
     * 在 biome_2（冰雪陆地）中通常双柱都有地面 → 完整冰门；
     * 在 biome_3（寒冷海洋）中可能只有一根有地面 → 倒塌变种。
     */
    private static void registerIceGate() {
        SimpleWeightedRandomList<BlockState> pillarBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.PACKED_ICE.defaultBlockState(), 40)
                .add(Blocks.ICE.defaultBlockState(), 35)
                .add(Blocks.BLUE_ICE.defaultBlockState(), 25)
                .build();

        SimpleWeightedRandomList<BlockState> topList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.SNOW_BLOCK.defaultBlockState(), 70)
                .add(Blocks.PACKED_ICE.defaultBlockState(), 30)
                .build();

        DecorationRegistry.registerCustomGenerator("ice_gate", new IceGateGenerator());

        DecorationBuilder.create()
                .type(DecorationType.CUSTOM)
                .body(new WeightedStateProvider(pillarBodyList))
                .top(new WeightedStateProvider(topList))
                .customGenerator("ice_gate")
                .height(20, 40)
                .gateWidth(5, 12)
                .pillarRadius(3)
                .beamThickness(3)
                .decorationChance(0.3f)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SNOW_BLOCK, Blocks.STONE, Blocks.DIRT, Blocks.GRASS_BLOCK, PDBlocks.DYEDREAM_ICE.get(), PDBlocks.DYEDREAM_PACKED_ICE.get(), PDBlocks.ICESTONE.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(false)
                .biome("pasterdream:biome_dyedream_2")
                .rarity(5)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("ice_gate");
    }

    /**
     * 注册方解石之柱装饰物
     * <p>
     * 对应原 CalcitePillarFeature + CalcitePillarConfiguration，
     * 使用 API 内置的 PILLAR 类型，方形截面锥形柱体，
     * 底部 2x2 为主（30% 概率 3x3），高度 15~20，
     * 表面嵌入染梦矿物和晶体，周围散落方解石碎片。
     */
    private static void registerCalcitePillar() {
        SimpleWeightedRandomList<BlockState> crystalList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAMQUARTZ_ORE.get().defaultBlockState(), 30)
                .add(PDBlocks.DYEDREAMDUST_ORE.get().defaultBlockState(), 20)
                .add(PDBlocks.AMBER_CANDY_ORE.get().defaultBlockState(), 15)
                .add(PDBlocks.DYEDREAM_BUD_0.get().defaultBlockState(), 10)
                .add(PDBlocks.DYEDREAM_BUD_1.get().defaultBlockState(), 10)
                .add(PDBlocks.DYEDREAM_BUD_2.get().defaultBlockState(), 10)
                .add(Blocks.CALCITE.defaultBlockState(), 5)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.PILLAR)
                .body(Blocks.CALCITE)
                .crystal(0.3f, new WeightedStateProvider(crystalList))
                .debris(Blocks.CALCITE, 6, 3)
                .height(15, 20)
                .width(2, 1)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.CALCITE, Blocks.STONE, Blocks.DIRT, Blocks.GRASS_BLOCK, PDBlocks.DYEDREAM_BLOCK.get(), PDBlocks.DYEDREAM_DIRT.get(), PDBlocks.DYEDREAM_GRASS.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_1")
                .rarity(3)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("calcite_pillar");
    }

    /**
     * 注册坠云密集子特征 —— 用于 random_selector 的子 feature
     * <p>
     * 对应原 CloudBlobFeature 的密集配置（cluster_size=90, radius=6），
     * 使用 API 内置的 BLOB 类型生成不规则椭球云团，
     * 开启悬空填充（fillHang）使云朵落在地面不悬空，
     * 并启用区域重叠检测（regionCheck）防止叠罗汉。
     */
    private static void registerCloudfallMoundDense() {
        SimpleWeightedRandomList<BlockState> cloudBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.CLOUD.get().defaultBlockState(), 80)
                .add(PDBlocks.THICK_CLOUD.get().defaultBlockState(), 15)
                .add(PDBlocks.CHISELED_DYEDREAMQUARTZ_BLOCK.get().defaultBlockState(), 5)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.BLOB)
                .body(new WeightedStateProvider(cloudBodyList))
                .clusterSize(90)
                .radius(6, 0)
                .yRadius(2)
                .irregularity(0.3f)
                .fillHang(true)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.CAVE_AIR, PDBlocks.CLOUD.get(), PDBlocks.THICK_CLOUD.get(), PDBlocks.DARK_CLOUD.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .biome("#pasterdream:is_dyedream")
                .rarity(1)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("cloudfall_mound_dense");
    }

    /**
     * 注册坠云稀疏子特征 —— 用于 random_selector 的子 feature
     * <p>
     * 对应原 CloudBlobFeature 的稀疏配置（cluster_size=55, radius=5），
     * 使用 API 内置的 BLOB 类型，不规则椭球云团的默认变体，
     * 并启用区域重叠检测（regionCheck）防止叠罗汉。
     */
    private static void registerCloudfallMoundSparse() {
        SimpleWeightedRandomList<BlockState> cloudBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.CLOUD.get().defaultBlockState(), 90)
                .add(PDBlocks.THICK_CLOUD.get().defaultBlockState(), 10)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.BLOB)
                .body(new WeightedStateProvider(cloudBodyList))
                .clusterSize(55)
                .radius(5, 0)
                .yRadius(2)
                .irregularity(0.35f)
                .fillHang(true)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.CAVE_AIR, PDBlocks.CLOUD.get(), PDBlocks.THICK_CLOUD.get(), PDBlocks.DARK_CLOUD.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .biome("#pasterdream:is_dyedream")
                .rarity(1)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("cloudfall_mound_sparse");
    }



    /**
     * 注册冰晶花园装饰物
     * <p>
     * 在寒冷染梦（biome_dyedream_2）地表散布冰晶和冰蕾，
     * 使用 SCATTER 类型在地面随机放置冰块和冰蕾方块，
     * 形成冻住的梦境碎片般的冰霜景观。
     */
    private static void registerIceCrystalGarden() {
        SimpleWeightedRandomList<BlockState> iceCrystalBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 35)
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 25)
                .add(PDBlocks.ICESTONE.get().defaultBlockState(), 20)
                .add(PDBlocks.ICE_BUD_0.get().defaultBlockState(), 10)
                .add(Blocks.PACKED_ICE.defaultBlockState(), 5)
                .add(Blocks.ICE.defaultBlockState(), 5)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.SCATTER)
                .body(new WeightedStateProvider(iceCrystalBodyList))
                .clusterSize(8)
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_2")
                .rarity(2)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("ice_crystal_garden");
    }

    /**
     * 注册珊瑚礁装饰物
     * <p>
     * 使用 API 内置的 AQUATIC 类型，在染梦海洋群系的海底生成群落状珊瑚礁。
     * 主体为 5 种珊瑚块的短柱（1~3 格高），表面嵌入珊瑚扇和海泡菜，
     * 周围散落更多珊瑚扇，形成完整的珊瑚礁生态。
     */
    private static void registerCoralReef() {
        SimpleWeightedRandomList<BlockState> coralBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.TUBE_CORAL_BLOCK.defaultBlockState(), 1)
                .add(Blocks.BRAIN_CORAL_BLOCK.defaultBlockState(), 1)
                .add(Blocks.BUBBLE_CORAL_BLOCK.defaultBlockState(), 1)
                .add(Blocks.FIRE_CORAL_BLOCK.defaultBlockState(), 1)
                .add(Blocks.HORN_CORAL_BLOCK.defaultBlockState(), 1)
                .build();

        SimpleWeightedRandomList<BlockState> coralFanList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.TUBE_CORAL_FAN.defaultBlockState(), 2)
                .add(Blocks.BRAIN_CORAL_FAN.defaultBlockState(), 2)
                .add(Blocks.BUBBLE_CORAL_FAN.defaultBlockState(), 2)
                .add(Blocks.FIRE_CORAL_FAN.defaultBlockState(), 2)
                .add(Blocks.HORN_CORAL_FAN.defaultBlockState(), 2)
                .add(Blocks.SEA_PICKLE.defaultBlockState(), 1)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.AQUATIC)
                .body(new WeightedStateProvider(coralBodyList))
                .crystal(0.2f, new WeightedStateProvider(coralFanList))
                .debris(new WeightedStateProvider(coralFanList), 12, 5)
                .height(1, 3)
                .width(3, 2)
                .waterRequired(true)
                .checkHang(false)
                .occupiedCheck(false)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(1)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("patch_coral_reef");
    }

    /**
     * 注册粉红梦幻珊瑚丛 —— 小型密集变种
     * <p>
     * 使用染梦粉色史莱姆块为主体，搭配粉色蘑菇和珊瑚扇装饰，
     * 小尺寸高密度散布在海底，贴合染梦维度的梦幻粉色风格。
     */
    private static void registerCoralReefPink() {
        SimpleWeightedRandomList<BlockState> pinkBodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(PDBlocks.PINKSLIME_BLOCK.get().defaultBlockState(), 3)
                .add(Blocks.TUBE_CORAL_BLOCK.defaultBlockState(), 1)
                .add(Blocks.BRAIN_CORAL_BLOCK.defaultBlockState(), 1)
                .build();

        SimpleWeightedRandomList<BlockState> pinkDecorList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.BRAIN_CORAL_FAN.defaultBlockState(), 2)
                .add(PDBlocks.PINKAGARIC_0.get().defaultBlockState(), 2)
                .add(PDBlocks.PINKAGARIC_1.get().defaultBlockState(), 2)
                .add(PDBlocks.PINKAGARIC_3.get().defaultBlockState(), 1)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.AQUATIC)
                .body(new WeightedStateProvider(pinkBodyList))
                .crystal(0.3f, new WeightedStateProvider(pinkDecorList))
                .debris(new WeightedStateProvider(pinkDecorList), 8, 4)
                .height(1, 2)
                .width(2, 1)
                .waterRequired(true)
                .checkHang(false)
                .occupiedCheck(false)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(1)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("patch_coral_reef_pink");
    }

    /**
     * 注册冰晶丛装饰物
     * <p>
     * 在染梦冰雪（biome_dyedream_2）地表生成小型冰晶尖刺丛，
     * 使用 SPIKE 类型，高度 3~6 格，频率较高（稀有度1），
     * 混入染梦冰和冰蕾，形成冻土上冒出的水晶丛景观。
     */
    private static void registerIceCrystalSpike() {
        SimpleWeightedRandomList<BlockState> bodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.ICE.defaultBlockState(), 50)
                .add(Blocks.PACKED_ICE.defaultBlockState(), 30)
                .add(Blocks.BLUE_ICE.defaultBlockState(), 10)
                .add(PDBlocks.DYEDREAM_ICE.get().defaultBlockState(), 10)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.SPIKE)
                .body(new WeightedStateProvider(bodyList))
                .crystal(0.1f, BlockStateProvider.simple(PDBlocks.ICE_BUD_0.get()))
                .height(3, 6)
                .radius(2, 0)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SNOW_BLOCK, Blocks.STONE, Blocks.DIRT, Blocks.GRASS_BLOCK, PDBlocks.DYEDREAM_ICE.get(), PDBlocks.DYEDREAM_PACKED_ICE.get(), PDBlocks.ICESTONE.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_2")
                .rarity(1)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("ice_crystal_spike");
    }

    /**
     * 注册冰柱装饰物
     * <p>
     * 在染梦冰雪（biome_dyedream_2）地表生成方形截面的高大冰柱，
     * 使用 PILLAR 类型，高度 8~15 格，以浮冰为主材质更坚固，
     * 表面嵌冰蕾，基部周围散落碎冰。
     */
    private static void registerIcePillar() {
        SimpleWeightedRandomList<BlockState> bodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.PACKED_ICE.defaultBlockState(), 40)
                .add(Blocks.ICE.defaultBlockState(), 30)
                .add(Blocks.BLUE_ICE.defaultBlockState(), 20)
                .add(PDBlocks.DYEDREAM_PACKED_ICE.get().defaultBlockState(), 10)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.PILLAR)
                .body(new WeightedStateProvider(bodyList))
                .crystal(0.15f, BlockStateProvider.simple(PDBlocks.ICE_BUD_0.get()))
                .debris(Blocks.PACKED_ICE, 4, 3)
                .height(8, 15)
                .width(3, 2)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SNOW_BLOCK, Blocks.STONE, Blocks.DIRT, Blocks.GRASS_BLOCK, PDBlocks.DYEDREAM_ICE.get(), PDBlocks.DYEDREAM_PACKED_ICE.get(), PDBlocks.ICESTONE.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_2")
                .rarity(3)
                .step(GenerationStep.Decoration.TOP_LAYER_MODIFICATION)
                .register("ice_pillar");
    }

    /**
     * 注册水下冰刺装饰物 —— 高大倾斜冰尖刺
     * <p>
     * 在寒冷海洋（biome_dyedream_3）海床向上生长巨型倾斜冰刺，
     * 高度 30~60 格，使用 SPIKE 类型（圆形截面），
     * 倾斜程度随机，可穿破水面形成壮观的冰尖刺景观。
     */
    private static void registerUnderwaterIceSpike() {
        SimpleWeightedRandomList<BlockState> bodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.ICE.defaultBlockState(), 50)
                .add(Blocks.PACKED_ICE.defaultBlockState(), 30)
                .add(Blocks.BLUE_ICE.defaultBlockState(), 20)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.SPIKE)
                .body(new WeightedStateProvider(bodyList))
                .crystal(0.1f, BlockStateProvider.simple(PDBlocks.ICE_BUD_0.get()))
                .height(30, 60)
                .radius(5, 1)
                .tilt(0.25f)
                .waterRequired(true)
                .checkHang(false)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .biome("pasterdream:biome_dyedream_3")
                .rarity(3)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("underwater_ice_spike");
    }

    /**
     * 注册海冰丘装饰物
     * <p>
     * 在寒冷海洋（biome_dyedream_3）海底生成破水而出的冰山丘，
     * 高度 8~18 格，宽底矮顶形似小型冰山，
     * 以浮冰和蓝冰为主材质，可突出水面数格。
     */
    private static void registerSeaIceMound() {
        SimpleWeightedRandomList<BlockState> bodyList = SimpleWeightedRandomList.<BlockState>builder()
                .add(Blocks.PACKED_ICE.defaultBlockState(), 50)
                .add(Blocks.BLUE_ICE.defaultBlockState(), 30)
                .add(Blocks.ICE.defaultBlockState(), 20)
                .build();

        DecorationBuilder.create()
                .type(DecorationType.AQUATIC)
                .body(new WeightedStateProvider(bodyList))
                .crystal(0.15f, BlockStateProvider.simple(PDBlocks.ICE_BUD_0.get()))
                .debris(Blocks.PACKED_ICE, 6, 4)
                .height(8, 18)
                .width(4, 2)
                .regionCheck(true, 0.3f)
                .replaceable(BlockPredicate.anyOf(
                    BlockPredicate.matchesBlocks(Blocks.AIR, Blocks.WATER, Blocks.ICE, Blocks.PACKED_ICE, Blocks.BLUE_ICE, Blocks.SAND, Blocks.GRAVEL, PDBlocks.DYEDREAM_SAND.get()),
                    BlockPredicate.matchesTag(BlockTags.REPLACEABLE)
                ))
                .checkHang(true)
                .biome("pasterdream:biome_dyedream_3")
                .rarity(2)
                .step(GenerationStep.Decoration.VEGETAL_DECORATION)
                .register("sea_ice_mound");
    }


    /**
     * 生成所有已注册装饰物的 JSON 数据文件
     * <p>
     * 仅供开发阶段使用，会覆盖已有 JSON 文件。
     * 生成后应将此方法的调用从主类中移除。
     * 不重复调用 register()，仅用已注册的条目生成 JSON。
     */
    public static void generateJson() {
        DecorationRegistry.generateAllJson();
    }
}