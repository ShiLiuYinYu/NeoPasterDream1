package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.network.chat.Component;
import java.util.List;

/**
 * TrueMoltengold Sword
 */
public class TrueMoltengoldSwordItem extends SwordItem {

    public TrueMoltengoldSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -2.2f)
        ));
    }

    @Override
    public void appendHoverText(ItemStack itemstack, Item.TooltipContext context, List<Component> list, TooltipFlag flag) {
        super.appendHoverText(itemstack, context, list, flag);
                        list.add(Component.literal("\u9576\u5D4C\uFF1A\u00A77\u65E0"));
                        list.add(Component.literal("\u00A77\u25AA \u00A79\u653B\u51FB\u5C06\u4F1A\u4F7F\u76EE\u6807\u88AB\u5F15\u71C34\u79D2"));
                        list.add(Component.literal("\u00A77\u25AA \u00A79\u5982\u76EE\u6807\u5DF2\u88AB\u5F15\u71C3 \u5219\u4F1A\u5728\u76EE\u6807\u5F15\u71C3\u7684\u6301\u7EED\u65F6\u95F4\u4E0A\u589E\u52A02\u79D2 \u53EF\u53E0\u52A0"));
    }

}