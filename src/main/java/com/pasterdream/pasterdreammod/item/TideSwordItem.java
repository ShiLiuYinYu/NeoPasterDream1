package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.network.chat.Component;
import java.util.List;

/**
 * Tide Sword
 */
public class TideSwordItem extends SwordItem {

    public TideSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -2.8f)
        ));
    }

    @Override
    public void appendHoverText(ItemStack itemstack, Item.TooltipContext context, List<Component> list, TooltipFlag flag) {
        super.appendHoverText(itemstack, context, list, flag);
                        list.add(Component.literal("\u9576\u5D4C\uFF1A\u00A77\u65E0"));
                        list.add(Component.literal("\u00A77\u25AA \u00A79\u624B\u6301\u6B66\u5668\u65F6\u83B7\u5F97\u6C34\u4E0B\u547C\u5438\u6548\u679C"));
    }

}