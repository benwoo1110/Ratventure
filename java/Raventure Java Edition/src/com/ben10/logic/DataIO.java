package com.ben10.logic;

import java.io.*;

public class DataIO {
    private static final String FILEPATH = "./saveFile.dat";
    private Object serObj;

    public DataIO(Object serObj) {
        this.serObj = serObj;
    }

    public void writeToFile() {
        try (var fileOut = new FileOutputStream(FILEPATH)) {
            var objectOut = new ObjectOutputStream(fileOut);
            objectOut.writeObject(serObj);
            System.out.println("Successfully saved game to " + FILEPATH);

        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public Object loadFromFile() {
        ObjectInputStream objectIn;
        try (var fileIn = new FileInputStream(FILEPATH)) {
            objectIn = new ObjectInputStream(fileIn);
            return objectIn.readObject();
        }
        catch (FileNotFoundException e) {
            System.out.println("No save file found! Play now and save a game!");
            return null;
        }
        catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        return null;
    }
}
