package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.network.chat.Component;
import java.util.List;

/**
 * Grass Sword
 */
public class GrassSwordItem extends SwordItem {

    public GrassSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -2.5f)
        ));
    }

    @Override
    public void appendHoverText(ItemStack itemstack, Item.TooltipContext context, List<Component> list, TooltipFlag flag) {
        super.appendHoverText(itemstack, context, list, flag);
                        list.add(Component.literal("\u9576\u5D4C\uFF1A\u00A77\u65E0"));
                        list.add(Component.literal("\u00A77\u25AA \u00A79\u653B\u51FB\u65BD\u52A0\u4E2D\u6BD2\u6548\u679C"));
    }

}