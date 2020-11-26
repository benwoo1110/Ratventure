package com.ben10.logic;

import java.awt.*;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Attack implements Serializable {
    private String enemyName;
    private Stats enemyStats;
    private boolean inBattle = false;

    private final List<Point> knowLocations;
    private final Data game;

    public Attack(Data game) {
        this.game = game;
        knowLocations = new ArrayList<>();
    }

    public boolean checkEncounter() {
        // Check if currently in a battle
        if (inBattle)
            return true;

        // No enemy when hero in town
        if (game.getHero().inTown()) return false;

        // Check if in known location
        for (var knowLocation : knowLocations) {
            if (knowLocation.equals(game.getHero().getPosition()))
                return false;
        }

        // Set the enemy
        if (game.getHero().getPosition().equals(new Point(7, 7))) {
            // King
            enemyName = "Rat King";
            enemyStats = new Stats(new int[]{6, 10}, 5, new int[]{24, 24}, true);
        }
        else {
            // Rat
            enemyName = "Rat";
            enemyStats = new Stats(new int[]{1, 3}, 1, new int[]{8, 8}, false);
        }

        inBattle = true;
        return true;
    }

    public AttackResult battle() {
        int heroDamage;
        var result = new AttackResult(enemyName);

        // Hero attacks
        if (enemyStats.hasOrb() && !game.getHero().getStats().hasOrb()){
            result.setImmune(true);
            heroDamage = 0;
        }
        else heroDamage = game.getHero().getStats().getRandomDamage(enemyStats.getDefence());
        enemyStats.updateHealth(-heroDamage);
        result.setHeroDamage(heroDamage);

        // See if enemy is dead
        if (enemyStats.getCurrentHealth() <= 0) {
            // Special for rat king
            if (enemyName.equals("Rat King")) result.setEndResult("winGame");
            else result.setEndResult("win");

            // Add to attacked before location
            knowLocations.add(new Point(game.getHero().getPosition()));

            inBattle = false;
            return result;
        }

        // Enemy attacks
        int enemyDamage = enemyStats.getRandomDamage(game.getHero().getStats().getDefence());
        game.getHero().getStats().updateHealth(-enemyDamage);
        result.setEnemyDamage(enemyDamage);

        // See if hero is dead
        if (game.getHero().getStats().getCurrentHealth() <= 0)
            result.setEndResult("loseGame");

        return result;
    }

    public void run() {
        inBattle = false;
    }

    public String getEnemyName() {
        return enemyName;
    }

    public Stats getEnemyStats() {
        return enemyStats;
    }
}
