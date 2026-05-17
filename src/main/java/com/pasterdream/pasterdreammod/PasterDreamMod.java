package com.pasterdream.pasterdreammod;

import com.pasterdream.pasterdreammod.capability.MeltDreamEnergyCapability;
import com.pasterdream.pasterdreammod.capability.SanCapability;
import com.pasterdream.pasterdreammod.command.PDCommands;
import com.pasterdream.pasterdreammod.config.PDClientConfig;
import com.pasterdream.pasterdreammod.config.PDCommonConfig;
import com.pasterdream.pasterdreammod.registry.PDBlockEntities;
import com.pasterdream.pasterdreammod.registry.PDBlocks;
import com.pasterdream.pasterdreammod.registry.PDCreativeTabs;
import com.pasterdream.pasterdreammod.registry.PDEffects;
import com.pasterdream.pasterdreammod.registry.PDEntities;
import com.pasterdream.pasterdreammod.registry.PDEntityEvents;
import com.pasterdream.pasterdreammod.registry.PDItems;
import com.pasterdream.pasterdreammod.registry.PDMenus;
import com.pasterdream.pasterdreammod.registry.PDParticles;
import com.pasterdream.pasterdreammod.registry.PDStructures;
import com.pasterdream.pasterdreammod.worldgen.PDBiomeModifiers;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * PasterDream 模组主类
 * 负责模组的初始化和事件总线管理
 */
@Mod(PasterDreamMod.MOD_ID)
public class PasterDreamMod {

    /**
     * 模组 ID 常量
     */
    public static final String MOD_ID = "pasterdream";

    /**
     * 模组日志记录器
     */
    public static final Logger LOGGER = LoggerFactory.getLogger(PasterDreamMod.class);

    /**
     * 构造函数
     *
     * @param modEventBus NeoForge 事件总线
     * @param modContainer NeoForge 模组容器
     */
    public PasterDreamMod(IEventBus modEventBus, ModContainer modContainer) {
        // 注册方块
        PDBlocks.BLOCKS.register(modEventBus);

        // 注册物品
        PDItems.ITEMS.register(modEventBus);

        // 注册方块实体
        PDBlockEntities.BLOCK_ENTITIES.register(modEventBus);

        // 注册实体类型
        PDEntities.ENTITY_TYPES.register(modEventBus);

        // 注册创造模式物品栏
        PDCreativeTabs.TABS.register(modEventBus);

        // 注册状态效果（BUFF/DEBUFF）
        PDEffects.MOB_EFFECTS.register(modEventBus);

        // 染梦维度的注册由 data/pasterdream/dimension/dyedream_world.json 数据驱动

        // 注册结构类型
        PDStructures.STRUCTURE_TYPES.register(modEventBus);

        // 注册菜单类型
        PDMenus.MENUS.register(modEventBus);

        // 注册粒子类型
        PDParticles.PARTICLE_TYPES.register(modEventBus);

        // 注册 BiomeModifier 序列化器（用于染梦维度特征注入）
        PDBiomeModifiers.BIOME_MODIFIER_SERIALIZERS.register(modEventBus);

        // 初始化染梦能量系统（注册 AttachmentType + 事件监听器）
        MeltDreamEnergyCapability.init(modEventBus);

        // 初始化 San 理智值系统（注册 AttachmentType + 事件监听器）
        SanCapability.init(modEventBus);

        // 注册配置文件
        modContainer.registerConfig(ModConfig.Type.CLIENT, PDClientConfig.SPEC);
        modContainer.registerConfig(ModConfig.Type.COMMON, PDCommonConfig.SPEC);

        // 监听通用设置事件
        modEventBus.addListener(this::commonSetup);

        // 在游戏总线上注册指令
        NeoForge.EVENT_BUS.addListener(PDCommands::register);
    }

    /**
     * 通用设置阶段初始化
     *
     * @param event FML 通用设置事件
     */
    private void commonSetup(final FMLCommonSetupEvent event) {
        LOGGER.info("===== PasterDreamMod 地形生成系统初始化 =====");
        LOGGER.info("BiomeModifier 序列化器已注册: pasterdream:dyedream_features");

        // 输出预期的 BiomeModifier JSON 配置文件列表（用于测试时确认文件是否被正确加载）
        LOGGER.info("预期的 BiomeModifier JSON 文件列表:");
        LOGGER.info("  - neoforge/biome_modifier/dyedream_ores.json -> 注入矿石 (UNDERGROUND_ORES)");
        LOGGER.info("    ├ pasterdream:ore_amber_candy");
        LOGGER.info("    ├ pasterdream:ore_dyedreamdust");
        LOGGER.info("    └ pasterdream:ore_dyedreamquartz");
        LOGGER.info("  - neoforge/biome_modifier/dyedream_vegetation.json -> 注入树木与植被 (VEGETAL_DECORATION)");
        LOGGER.info("    ├ pasterdream:dyedream_trees");
        LOGGER.info("    ├ pasterdream:patch_dyedream_buds");
        LOGGER.info("    ├ pasterdream:patch_pinkagaric");
        LOGGER.info("    ├ pasterdream:patch_dyedream_lily_pad");
        LOGGER.info("    ├ pasterdream:patch_dyedream_lotus");
        LOGGER.info("    └ pasterdream:patch_dyedream_seagrass");
        LOGGER.info("目标生物群系标签: #pasterdream:is_dyedream");
        LOGGER.info("===== 地形生成系统初始化完成 =====");
    }
}
