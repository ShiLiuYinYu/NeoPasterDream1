package com.pasterdream.pasterdreammod.block;

import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.core.Direction;
import net.minecraft.core.BlockPos;

/**
 * 染梦树叶方块
 * 继承原版 LeavesBlock，支持 distance/persistent 属性、透明度渲染和同种跳过面渲染
 */
public class DyedreamLeavesBlock extends LeavesBlock {
    /**
     * @param properties 方块属性
     */
    public DyedreamLeavesBlock(Properties properties) {
        super(properties);
    }

    /**
     * 使用染梦树叶默认属性
     */
    public DyedreamLeavesBlock() {
        super(BlockBehaviour.Properties.of()
                .ignitedByLava()
                .sound(SoundType.GRASS)
                .strength(0.01f, 0.1f)
                .noOcclusion()
                .isRedstoneConductor((bs, br, bp) -> false)
                .dynamicShape());
    }

    @Override
    public boolean propagatesSkylightDown(BlockState state, BlockGetter reader, BlockPos pos) {
        return true;
    }

    @Override
    public int getLightBlock(BlockState state, BlockGetter worldIn, BlockPos pos) {
        return 0;
    }

    @Override
    public int getFlammability(BlockState state, BlockGetter world, BlockPos pos, Direction face) {
        return 20;
    }
}