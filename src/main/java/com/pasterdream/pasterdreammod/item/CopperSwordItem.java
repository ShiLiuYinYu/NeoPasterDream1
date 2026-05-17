package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;

/**
 * Copper Sword
 */
public class CopperSwordItem extends SwordItem {

    public CopperSwordItem() {
        super(PDSwordTiers.WOOD_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.WOOD_LEVEL, 3, -2.4f)
        ));
    }

}