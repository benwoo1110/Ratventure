package com.ben10.logic;

import java.awt.*;
import java.io.Serializable;

public class Hero implements Serializable {
    private final Point position;
    private Stats stats;

    private final Data game;

    public Hero(Point position, Stats stats, Data game) {
        this.position = position;
        this.stats = stats;
        this.game = game;
    }

    public boolean inTown() {
        return game.getGrid().hasSprite(position, sprites.TOWN);
    }

    public Stats getStats() {
        return stats;
    }

    public Point getPosition() {
        return position;
    }

    public void setStats(Stats stats) {
        this.stats = stats;
    }

    @Override
    public String toString() {
        return "Hero{" +
                "position=" + position +
                ", stats=" + stats +
                '}';
    }
}
