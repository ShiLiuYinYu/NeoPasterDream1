package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.network.chat.Component;
import java.util.List;

/**
 * Desert Sword
 */
public class DesertSwordItem extends SwordItem {

    public DesertSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -3.1f)
        ));
    }

    @Override
    public void appendHoverText(ItemStack itemstack, Item.TooltipContext context, List<Component> list, TooltipFlag flag) {
        super.appendHoverText(itemstack, context, list, flag);
                        list.add(Component.literal("\u9576\u5D4C\uFF1A\u00A77\u65E0"));
                        list.add(Component.literal("\u00A77\u25AA \u00A79\u624B\u6301\u6B66\u5668\u65F6\u79FB\u901F-15% \u6297\u6027+20%"));
    }

}