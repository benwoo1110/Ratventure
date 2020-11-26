package com.ben10.text;

import com.ben10.logic.Data;

import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class TextBased {
    private Data game;
    TextDisplay display;
    TextInput userInput;

    public TextBased() {
        game = new Data();
        display = new TextDisplay(game);
        userInput = new TextInput(game);
    }

    public void run() {
        // Main loop for console
        while (true) {
            // Main menu options
            int menuOption = userInput.getOption("menu");

            switch (menuOption) {
                case 1:
                    // new game
                    game.start();
                    game.setNickname(userInput.getPlayerName());
                    runGame();
                    break;
                case 2:
                    // load game
                    var gameSavedData = game.load();
                    if(gameSavedData != null) {
                        game = gameSavedData;
                        runGame();
                    }
                    break;
                case 3:
                    // Leaderboard
                    break;
                case 4:
                    // end game
                    return;
                default:
                    break;
            }
        }
    }

    private void runGame() {
        int gameChoice;
        int attackChoice;

        while (true) {
            // Check for enemy attack
            if (game.getAttack().checkEncounter()) {
                // Attack options
                System.out.printf("Encounter - %s!\n", game.getAttack().getEnemyName());
                display.printStats(game.getAttack().getEnemyStats());
                attackChoice = userInput.getOption("attack");

                // Attack
                // Check if game ended
                // Run
                switch (attackChoice) {// Skip the other selections
                    case 1:
                        var attackResult = game.getAttack().battle();
                        display.printAttack(attackResult);
                        switch (attackResult.getEndResult()) {
                            case "winGame":
                                // Add to leaderboard
                                return;
                            case "loseGame":
                                return;
                        }
                        continue;
                    case 2:
                        game.getAttack().run();
                        break;
                }
            }

            // Town
            if (game.getHero().inTown()) {
                // Get user input of choice
                System.out.printf("Day %d: You are in town.\n", game.getDay());
                gameChoice = userInput.getOption("town");

                // In town actions
                switch (gameChoice) {
                    case 4:
                        // rest
                        game.getAction().rest();
                        break;
                    case 5:
                        // save game
                        game.save();
                        break;
                    case 6:
                        // exit
                        return;
                }
            }

            // Outdoors
            else {
                // Get user input of choice
                System.out.printf("Day %d: You are in the open.\n", game.getDay());
                gameChoice = userInput.getOption("open");

                // In open actions
                switch (gameChoice) {
                    case 4:
                        // sense orb
                        display.printOrbSense(game.getOrb().sense());
                        break;
                    case 5:
                        // exit
                        return;
                }
            }

            // Common options
            // View hero
            // View map
            // Move
            switch (gameChoice) {
                case 1:
                    display.printStats("Hero: " + game.getNickname(), game.getHero().getStats());
                    break;
                case 2:
                    display.printGrid();
                    break;
                case 3:
                    display.printGrid();
                    game.getAction().move(userInput.getDirection());
                    display.printGrid();
                    break;
            }
        }
    }
}
