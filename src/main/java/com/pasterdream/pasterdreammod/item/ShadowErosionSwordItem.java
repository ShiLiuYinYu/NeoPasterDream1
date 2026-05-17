package com.pasterdream.pasterdreammod.item;

import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Item;

/**
 * ShadowErosion Sword
 */
public class ShadowErosionSwordItem extends SwordItem {

    public ShadowErosionSwordItem() {
        super(PDSwordTiers.STONE_LEVEL, new Item.Properties().attributes(
            SwordItem.createAttributes(PDSwordTiers.STONE_LEVEL, 3, -1.0f)
        ));
    }

}