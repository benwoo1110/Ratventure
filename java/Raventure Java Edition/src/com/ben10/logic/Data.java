package com.ben10.logic;

import java.awt.*;
import java.io.Serializable;

public class Data implements Serializable {
    private Hero hero;
    private Grid grid;
    private Orb orb;
    private int day;
    private String nickname;
    private final Action action;
    private final Attack attack;

    public Data() {
        action = new Action(this);
        attack = new Attack(this);
    }

    public void start() {
        day = 1;
        grid = new Grid(this).generate();
        orb = new Orb(this);
        hero = new Hero(
                new Point(0, 0),
                new Stats(new int[]{2, 4}, 1, new int[]{20, 20}, false),
                this
        );
    }

    public void save() {
        var serObject = new DataIO(this);
        serObject.writeToFile();
    }

    public Data load() {
        var serObject = new DataIO(this);
        return (Data) serObject.loadFromFile();
    }

    public Hero getHero() {
        return hero;
    }

    public Grid getGrid() {
        return grid;
    }

    public Orb getOrb() {
        return orb;
    }

    public Action getAction() {
        return action;
    }

    public Attack getAttack() {
        return attack;
    }

    public int getDay() {
        return day;
    }

    public void nextDay() {
        day++;
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }

}
