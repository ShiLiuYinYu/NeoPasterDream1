package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;

/**
 * Shadow Sword
 */
public class ShadowSwordItem extends SwordItem {

    public ShadowSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -2.4f)
        ));
    }

}