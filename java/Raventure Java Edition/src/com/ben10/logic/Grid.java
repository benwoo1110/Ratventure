package com.ben10.logic;

import java.awt.*;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Grid implements Serializable {
    private List<ArrayList<ArrayList<sprites>>> grid;
    private final Data game;
    private final int row;
    private final int column;

    public Grid(Data game) {
        this.game = game;
        this.row = 8;
        this.column = 8;
        create();
    }

    public int getRow() {
        return row;
    }

    public int getColumn() {
        return column;
    }

    public ArrayList<sprites> getTile(Point pos) {
        return getTile(pos.x, pos.y);
    }

    public ArrayList<sprites> getTile(int r, int c) {
        return grid.get(r).get(c);
    }

    public boolean validTile(int r, int c) {
        return (r >= 0 && r < row && c >= 0 && c < column);
    }

    public boolean hasSprite(int r, int c) {
        return !(grid.get(r).get(c).isEmpty());
    }

    public boolean hasSprite(Point pos, sprites sprite) {
        return hasSprite(pos.x, pos.y, sprite);
    }

    public boolean hasSprite(int r, int c, sprites sprite) {
        return (grid.get(r).get(c).contains(sprite));
    }

    public void add(Point pos, sprites sprite) {
        add(pos.x, pos.y, sprite);
    }

    public void add(int r, int c, sprites sprite) {
        grid.get(r).get(c).add(sprite);
    }

    public void remove(Point pos, sprites sprite) {
        remove(pos.x, pos.y, sprite);
    }

    public void remove(int r, int c, sprites sprite) {
        grid.get(r).get(c).remove(sprite);
    }

    public Grid generate() {
        // Set sprite positions
        grid.get(0).get(0).add(sprites.TOWN);
        grid.get(0).get(0).add(sprites.HERO);
        grid.get(7).get(7).add(sprites.KING);
        randomTowns();

        return this;
    }

    private void create() {
        // Generate grid array
        grid = new ArrayList<>();
        for (int r = 0; r < row; r++) {
            grid.add(new ArrayList<>());
            for (int c = 0; c < column; c++) {
                grid.get(r).add(new ArrayList<>());
            }
        }
    }

    private void randomTowns() {
        int townsGenerated = 0;
        while (townsGenerated < 4) {
            // Get a random town location
            int randomR = (int) (Math.random() * (row + 1));
            int randomC = (int) (Math.random() * (column + 1));
            boolean validPos = validTile(randomR, randomC);

            // Loop through 2 steps radius
            for (int r = -2; r <= 2; r++) {
                int startC = 2 - Math.abs(r);
                for (int c = -startC;c <= startC; c++) {
                    // steps not in grid
                    if (!validTile(randomR+r, randomC+c)) continue;

                    // Check if pos is valid
                    if (hasSprite(randomR+r, randomC+c))
                        validPos = false;
                }
            }

            // Add town to map
            if (validPos) {
                grid.get(randomR).get(randomC).add(sprites.TOWN);
                townsGenerated++;
            }
        }
    }
}
