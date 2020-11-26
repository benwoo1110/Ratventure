package test;

import com.ben10.logic.Stats;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class StatsTest {
    private Stats stats;

    @Before
    public void setUp() throws Exception {
        stats = new Stats(
                new int[] {2, 4},
                1,
                new int[] {18, 20},
                false);
    }

    @After
    public void tearDown() throws Exception {
        stats = null;
    }

    @Test
    public void getDamage() {
        int[] expected = {2, 4};
        int[] actual = stats.getDamage();
        assertArrayEquals(expected, actual);
    }

    @Test
    public void getRandomDamage() {
        final int MAX = 3;
        final int MIN = 1;
        final int DEFENCE = 1;
        for (int i = 0; i < 100; i++) {
            int damageDone = stats.getRandomDamage(DEFENCE);
            assertTrue(damageDone >= MIN);
            assertTrue(damageDone <= MAX);
        }
    }

    @Test
    public void setDamage() {
        int[] expected = {5, 7};
        stats.setDamage(new int[] {5, 7});
        assertArrayEquals(stats.getDamage(), expected);
    }

    @Test
    public void getDefence() {
        int expected = 1;
        int actual = stats.getDefence();
        assertEquals(expected, actual);
    }

    @Test
    public void setDefence() {
        int expected = 4;
        stats.setDefence(4);
        assertEquals(stats.getDefence(), expected);
    }

    @Test
    public void getHealth() {
        int[] expected = {18, 20};
        int[] actual = stats.getHealth();
        assertArrayEquals(expected, actual);
    }

    @Test
    public void getCurrentHealth() {
        int expected = 18;
        int actual = stats.getCurrentHealth();
        assertEquals(expected, actual);
    }

    @Test
    public void getMaxHealth() {
        int expected = 20;
        int actual = stats.getMaxHealth();
        assertEquals(expected, actual);
    }

    @Test
    public void setHealth() {
        int[] expected = {15, 18};
        stats.setHealth(new int[] {15, 18});
        assertArrayEquals(stats.getHealth(), expected);
    }

    @Test
    public void setCurrentHealth() {
        int expected = 12;
        stats.setCurrentHealth(12);
        assertEquals(stats.getCurrentHealth(), expected);
    }

    @Test
    public void updateHealth() {
        // positive
        int expected = 19;
        stats.updateHealth(1);
        assertEquals(stats.getCurrentHealth(), expected);

        // negative
        expected = 12;
        stats.updateHealth(-7);
        assertEquals(stats.getCurrentHealth(), expected);
    }

    @Test
    public void hasOrb() {
        assertFalse(stats.hasOrb());
    }

    @Test
    public void setOrb() {
        stats.setOrb(true);
        assertTrue(stats.hasOrb());
    }
}