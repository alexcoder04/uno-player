
# uno-player

A program that plays the popular Uno card game.

## Current state

**Game**: insert information via command line, it checks for possible cards
and puts a random one.

**Image recognition**: train on our small dataset, recognize cards (works ok).

## Plan

Read card with Raspberry Pi camera (machine learning), play smart (not actually
using machine learning but simple rules, the game is not so complex).

## Roadmap

 - save and load the model on disk
 - number recognition -> load image in greyscale
 - some smart gameplay rules
 - input cards into the game with the AI
   - wait for the AI to be "sure enough" about the picture, only then use it
   - first only detecting, one person has to help the computer to physically play
   - build some kind of robot that puts the cards itself
 - text to speech

