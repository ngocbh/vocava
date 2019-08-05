package com.google.cloud.android.speech;


import java.util.Random;

public class SpeakerVertification {

    private final float THRESHOLD = 0.5f;
    private float totalProb;
    private int numWindow;

    public SpeakerVertification(){
        reset();
    }

    public void recognition(short[] inputBuffer){
        // send inputBuffer to server and recieve a float
        Random rand = new Random();
        float prob = rand.nextFloat();
        // end
        totalProb += prob;
        numWindow += 1;
    }

    public void reset(){
        totalProb = 0;
        numWindow = 0;
    }

    public boolean isVertified(){
        return totalProb / numWindow >= THRESHOLD;
    }
}
