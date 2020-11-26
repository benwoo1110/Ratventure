package com.ben10.text;

import com.ben10.logic.Data;

import java.util.*;

public class TextInput {
    private Data game;

    public TextInput(Data game) {
        this.game = game;
    }

    private final Scanner userInput = new Scanner(System.in);

    private final Map<String, String[]> options = new HashMap<>() {{
        put("menu", new String[]{ "New game", "Load saved", "Leaderboard", "Quit game" });
        put("town", new String[]{ "View stats", "View map", "Move", "Rest", "Save game", "Exit game" });
        put("open", new String[]{ "View stats", "View map", "Move", "Sense Orb", "Exit game" });
        put("attack", new String[]{ "Attack", "Run" });
    }};

    public String getPlayerName() {
        String name;
        while (true) {
            // Get the input
            System.out.print("Enter a cool name: ");
            name = userInput.nextLine().trim();

            // Ensure no empty
            if (!name.isEmpty())
                return name;
        }
    }

    public int getOption(String optionName) {
        int choice;
        var optionsList = options.get(optionName);

        while (true) {
            // Display options
            int counter = 1;
            for (var option : optionsList) {
                System.out.printf("%d) %s\n", counter, option);
                counter++;
            }

            // Get the input
            System.out.print("Enter choice: ");
            try {
                choice = Integer.parseInt(userInput.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Please enter a number!");
                continue;
            } finally {
                // Clear console after input
                clear();
            }

            // Check if option is valid
            if (choice > 0 && choice <= optionsList.length)
                return choice;
            else
                System.out.printf("Please enter a choice from 1 to %d!\n", optionsList.length);
        }

    }

    public String getDirection() {
        String choice;

        while (true) {
            // Display options
            System.out.println("W = up; A = left; S = down; D = right");

            // Get the input
            System.out.print("Enter choice: ");
            choice = userInput.nextLine().toLowerCase();

            // Check if option is valid
            if (game.getAction().acceptedMove.contains(choice))
                return choice;
            else
                System.out.println("Invalid direction!");
        }
    }

    private void clear() {
        // Clear the console after each user input
        // for (int i = 0; i < 50; i++) System.out.println();
        System.out.println();
    }
}
