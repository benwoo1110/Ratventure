package com.ben10.logic;

public class AttackResult {
    private boolean immune = false;
    private String enemyName = "";
    private int heroDamage = -1;
    private int enemyDamage = -1;
    private String endResult = "";

    public AttackResult(String enemyName) {
        this.enemyName = enemyName;
    }

    public boolean hasImmune() {
        return immune;
    }

    public void setImmune(boolean immune) {
        this.immune = immune;
    }

    public int getHeroDamage() {
        return heroDamage;
    }

    public void setHeroDamage(int heroDamage) {
        this.heroDamage = heroDamage;
    }

    public int getEnemyDamage() {
        return enemyDamage;
    }

    public void setEnemyDamage(int enemyDamage) {
        this.enemyDamage = enemyDamage;
    }

    public String getEndResult() {
        return endResult;
    }

    public void setEndResult(String endResult) {
        this.endResult = endResult;
    }

    public String getEnemyName() {
        return enemyName;
    }

    @Override
    public String toString() {
        return "AttackResult{" +
                "immune=" + immune +
                ", heroDamage=" + heroDamage +
                ", enemyDamage=" + enemyDamage +
                ", endResult='" + endResult + '\'' +
                '}';
    }
}
