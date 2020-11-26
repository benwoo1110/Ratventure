package com.ben10.logic;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class Action implements Serializable {
    private final Data game;
    public final List acceptedMove = new ArrayList<String>(List.of("w", "a", "s", "d"));

    public Action(Data game) {
        this.game = game;
    }

    public boolean move(String direction) {
        // Ensure valid direction
        if (!acceptedMove.contains(direction))
            throw new IllegalArgumentException();

        // Set new pos
        int newR = game.getHero().getPosition().x;
        int newC = game.getHero().getPosition().y;
        switch (direction) {
            case "w":
                newR--;
                break;
            case "a":
                newC--;
                break;
            case "s":
                newR++;
                break;
            case "d":
                newC++;
                break;
            default:
                return false;
        }
        // Ensure new pos is valid
        if (!game.getGrid().validTile(newR, newC)) return false;

        // Remove hero from grid
        game.getGrid().remove(game.getHero().getPosition(), sprites.HERO);

        // Set new
        game.getHero().getPosition().setLocation(newR, newC);

        // Add hero to new pos
        game.getGrid().add(game.getHero().getPosition(), sprites.HERO);

        game.nextDay();
        return true;
    }

    public void rest() {
        // Set health back to max
        game.getHero().getStats().setCurrentHealth(game.getHero().getStats().getMaxHealth());
        game.nextDay();
    }
}
