package com.pasterdream.pasterdreammod.config;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * 客户端配置文件
 * 控制 HUD 渲染相关选项
 * <p>
 * 可配置项：
 * - HUD 渲染开关（染梦能量条 / San 值条）
 * - 潜行模式显示
 * - 屏幕位置偏移
 */
public class PDClientConfig {

    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();

    // ===== HUD 渲染开关 =====
    public static final ModConfigSpec.BooleanValue SHOW_MELTDREAM_ENERGY_HUD;
    public static final ModConfigSpec.BooleanValue SHOW_SAN_HUD;
    public static final ModConfigSpec.BooleanValue STEALTH_DISPLAY_HUD;

    // ===== HUD 位置偏移 =====
    public static final ModConfigSpec.ConfigValue<Integer> MELTDREAM_ENERGY_X_OFFSET;
    public static final ModConfigSpec.ConfigValue<Integer> MELTDREAM_ENERGY_Y_OFFSET;
    public static final ModConfigSpec.ConfigValue<Integer> SAN_X_OFFSET;
    public static final ModConfigSpec.ConfigValue<Integer> SAN_Y_OFFSET;

    static {
        BUILDER.push("HUD");

        SHOW_MELTDREAM_ENERGY_HUD = BUILDER
                .comment("显示染梦能量 HUD 条，默认：true")
                .define("showMeltdreamEnergyHud", true);

        SHOW_SAN_HUD = BUILDER
                .comment("显示 San 值 HUD 条，默认：true")
                .define("showSanHud", true);

        STEALTH_DISPLAY_HUD = BUILDER
                .comment("仅在潜行时显示 HUD 图标，默认：false")
                .define("stealthDisplayHud", false);

        MELTDREAM_ENERGY_X_OFFSET = BUILDER
                .comment("染梦能量条 X 偏移，默认：0")
                .define("meltdreamEnergyXOffset", 0);

        MELTDREAM_ENERGY_Y_OFFSET = BUILDER
                .comment("染梦能量条 Y 偏移，默认：0")
                .define("meltdreamEnergyYOffset", 0);

        SAN_X_OFFSET = BUILDER
                .comment("San 值条 X 偏移，默认：0")
                .define("sanXOffset", 0);

        SAN_Y_OFFSET = BUILDER
                .comment("San 值条 Y 偏移，默认：0")
                .define("sanYOffset", 0);

        BUILDER.pop();

        SPEC = BUILDER.build();
    }

}