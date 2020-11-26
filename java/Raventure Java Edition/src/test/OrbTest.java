package test;

import com.ben10.logic.Data;
import com.ben10.logic.Hero;
import com.ben10.logic.Orb;
import com.ben10.logic.Stats;
import org.junit.After;
import org.junit.Before;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;

import java.awt.*;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class OrbTest {

    private Orb orb;
    private Data mockGame;

    @Before
    public void setUp() throws Exception {
        mockGame = mock(Data.class);
        orb = new Orb(mockGame, new Point(4, 4));
    }

    @Test
    public void foundOrb() {
        when(mockGame.getHero()).thenReturn(new Hero(
                new Point(0, 0),
                new Stats(new int[]{2, 4}, 1, new int[]{20, 20}, false),
                mockGame
        ));
        // when(mockHero.getPosition()).thenReturn(new Point(4, 4));
    }
}