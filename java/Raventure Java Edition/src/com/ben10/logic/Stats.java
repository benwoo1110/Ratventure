package com.ben10.logic;

import java.io.Serializable;
import java.util.Arrays;

public class Stats implements Serializable {
    private int[] damage;
    private int defence;
    private int[] health;
    private boolean orb;

    public Stats(int[] damage, int defence, int[] health) {
        this.damage = damage;
        this.defence = defence;
        this.health = health;
        this.orb = false;
    }

    public Stats(int[] damage, int defence, int[] health, boolean orb) {
        this.damage = damage;
        this.defence = defence;
        this.health = health;
        this.orb = orb;
    }


    public int[] getDamage() {
        return damage;
    }

    public int getRandomDamage(int defence) {
        return Math.max(0, (int) (Math.random() * (damage[1]-damage[0]) + damage[0] - defence));
    }

    public void setDamage(int[] damage) {
        this.damage = damage;
    }

    public int getDefence() {
        return defence;
    }

    public void setDefence(int defence) {
        this.defence = defence;
    }

    public int[] getHealth() {
        return health;
    }

    public int getCurrentHealth() {
        return health[0];
    }

    public int getMaxHealth() {
        return health[1];
    }

    public void setHealth(int[] health) {
        this.health = health;
    }

    public void setCurrentHealth(int health) {
        this.health[0] = health;
    }

    public void updateHealth(int change) {
        this.health[0] = Math.max(0, this.health[0] + change);
    }

    public boolean hasOrb() {
        return orb;
    }

    public void setOrb(boolean orb) {
        this.orb = orb;
    }

    @Override
    public String toString() {
        return "Stats{" +
                "damage=" + Arrays.toString(damage) +
                ", defence=" + defence +
                ", health=" + Arrays.toString(health) +
                ", orb=" + orb +
                '}';
    }
}
