package com.ben10.text;

import com.ben10.logic.AttackResult;
import com.ben10.logic.Data;
import com.ben10.logic.Stats;

import java.util.ArrayList;

public class TextDisplay {
    private Data game;

    public TextDisplay(Data game) {
        this.game = game;
    }

    public void printStats(String name, Stats stats) {
        System.out.println(name);
        printStats(stats);
    }

    public void printStats(Stats stats) {
        System.out.printf("Damage: %d - %d\n", stats.getDamage()[0], stats.getDamage()[1]);
        System.out.printf("Defence: %d\n", stats.getDefence());
        System.out.printf("Health: %d/%d\n", stats.getHealth()[0], stats.getHealth()[1]);
    }

    public void printGrid() {
        String separator = "+---+---+---+---+---+---+---+---+";
        for (int r = 0 ; r < game.getGrid().getRow(); r++) {
            System.out.println(separator);
            for (int c = 0 ; c < game.getGrid().getRow(); c++) {
                System.out.print("|" + textAlignCenter(getTileText(r, c), 3));
            }
            System.out.println("|");
        }
        System.out.println(separator);
    }

    public void printOrbSense(String result) {
        switch (result) {
            case "Already found":
                System.out.println("You have already taken the orb!");
                break;
            case "Found":
                System.out.println("You found the Orb of Power!");
                System.out.println("Your attack increases by 5!");
                System.out.println("Your defence increases by 5!");
                break;
            default:
                System.out.printf("You sense that the Orb of Power is to the %s.\n", result);
                break;
        }
    }

    public void printAttack(AttackResult result) {
        if (result.hasImmune())
            System.out.println("You do not have the Orb of Power - the Rat King is immune!");

        System.out.printf("You deal %d damage to the %s\n", result.getHeroDamage(), result.getEnemyName());

        if (result.getEndResult().startsWith("win")) {
            System.out.printf("The %s is dead! You are victorious!\n", result.getEnemyName());

            if (result.getEndResult().equals("winGame")) {
                System.out.println("Congratulations, you have defeated the Rat King!");
                System.out.println("The world is saved! You win!");
            }
            return;
        }

        System.out.printf("Ouch! The %s hit you for %d damage!\n", result.getEnemyName(), result.getEnemyDamage());
        System.out.printf("You have %d HP left.\n", game.getHero().getStats().getCurrentHealth());

        if (result.getEndResult().equals("loseGame")) {
            System.out.println("OH nOOoO! You are dead! Game over...");
        }
    }

    private String getTileText(int r, int c) {
        var tileList = new ArrayList<String>();
        for (var sprite : game.getGrid().getTile(r, c)) {
            switch (sprite) {
                case HERO:
                    tileList.add("H");
                    break;
                case TOWN:
                    tileList.add("T");
                    break;
                case KING:
                    tileList.add("K");
                    break;
            }
        }
        return String.join("/", tileList);
    }

    private String textAlignCenter(String text, int width) {
        if (width <= text.length())
            return text.substring(0, width);
        int before = (width - text.length())/2;
        if (before == 0)
            return String.format("%-" + width + "s", text);
        int rest = width - before;
        return String.format("%" + before + "s%-" + rest + "s", "", text);
    }

    public static String capitalize(String str) {
        if(str == null || str.isEmpty()) {
            return str;
        }
        return str.substring(0, 1).toUpperCase() + str.substring(1);
    }

}
