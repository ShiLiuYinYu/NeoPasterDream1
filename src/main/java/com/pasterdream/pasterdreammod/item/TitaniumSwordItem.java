package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;

/**
 * Titanium Sword
 */
public class TitaniumSwordItem extends SwordItem {

    public TitaniumSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -2.4f)
        ));
    }

}