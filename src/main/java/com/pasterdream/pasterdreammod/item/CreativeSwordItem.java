package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.network.chat.Component;
import java.util.List;

/**
 * Creative Sword
 */
public class CreativeSwordItem extends SwordItem {

    public CreativeSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -2.4f)
        ));
    }

    @Override
    public void appendHoverText(ItemStack itemstack, Item.TooltipContext context, List<Component> list, TooltipFlag flag) {
        super.appendHoverText(itemstack, context, list, flag);
                        list.add(Component.literal("\u00A77\u521B\u9020\u6A21\u5F0F\u8C03\u8BD5\u5DE5\u5177"));
                        list.add(Component.literal("\u00A77\u5F3A\u5236\u51FB\u6740\u5E76\u6E05\u9664\u5B9E\u4F53"));
    }

}