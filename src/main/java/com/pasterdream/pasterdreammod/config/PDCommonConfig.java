package com.pasterdream.pasterdreammod.config;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * 通用配置文件
 * 控制系统计算相关选项
 * <p>
 * 可配置项：
 * - 染梦能量系统启用开关
 * - San 值系统启用开关
 */
public class PDCommonConfig {

    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();

    // ===== 系统启用开关 =====
    public static final ModConfigSpec.BooleanValue ENABLE_MELTDREAM_ENERGY;
    public static final ModConfigSpec.BooleanValue ENABLE_SAN;

    static {
        BUILDER.push("System");

        ENABLE_MELTDREAM_ENERGY = BUILDER
                .comment("启用染梦能量系统，关闭后所有染梦能量相关计算将不再执行，默认：true")
                .define("enableMeltdreamEnergy", true);

        ENABLE_SAN = BUILDER
                .comment("启用 San 值系统，关闭后所有 San 值相关计算将不再执行，默认：true")
                .define("enableSan", true);

        BUILDER.pop();

        SPEC = BUILDER.build();
    }

}