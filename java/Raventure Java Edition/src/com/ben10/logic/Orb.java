package com.ben10.logic;

import java.awt.*;
import java.io.Serializable;

public class Orb implements Serializable {
    Point position;

    private final Data game;

    public Orb(Data game) {
        this.game = game;
        position = new Point();
        randomPos();
    }

    public Orb(Data game, Point position) {
        this.game = game;
        this.position = position;
    }

    public String sense() {
        // Check if orb is already found
        if (game.getHero().getStats().hasOrb())
            return "Already found";

        // A day to sense orb
        game.nextDay();

        // See if hero on orb tile
        if (game.getHero().getPosition().equals(position)) {
            // Set new stats
            game.getHero().getStats().setDamage(new int[]{7, 9});
            game.getHero().getStats().setDefence(6);
            return "Found";
        }

        // Calculate direction of the Orb
        String direction = "";
        if (game.getHero().getPosition().x > position.x)
            direction += "north";
        else if (game.getHero().getPosition().x < position.x)
            direction += "south";
        if (game.getHero().getPosition().y > position.y)
            direction += "west";
        else if (game.getHero().getPosition().y < position.y)
            direction += "east";

        return direction;
    }

    private void randomPos() {
        while (true) {
            int randomR = (int) (Math.random() * (game.getGrid().getRow() + 1));
            int randomC = (int) (Math.random() * (game.getGrid().getRow() + 1));

            if (game.getGrid().validTile(randomR, randomC) && !game.getGrid().hasSprite(randomR, randomC))
                position.setLocation(randomR, randomC);
                break;
        }
    }
}
