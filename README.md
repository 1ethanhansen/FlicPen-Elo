# FlicPen-Elo
A simple elo program like FRC elo or FRC elo app, but optimized for flicpen and in python because kotlin and json don't play nice

## What is FlicPen?
FlicPen is a simple game designed to be easy to play with minimal setup, equipment, and prior knowledge/skill. The goal is to earn points by forcing the opponent to give up a point. Points are given up when a player doesn’t make the pen all the way through the erasers in 3 or fewer flicks, when a player knocks an eraser over, or when the player hits the pen off the table.

## Where can I find more information about FlicPen?
There is a FlicPen subreddit. Not much there because FlicPen is mainly just a thing between my friends and me.
The rules for FlicPen are on the subreddit.

## How it works
Essentially a direct application of the standard Elo formulas, more info on the Elo rating system can be found on [Wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system)

### My breakdown
The Elo rating system is a relative rating system in which players are given a rating based on who they win and lose against, as well as by how much they win or lose.
In terms of FlicPen, a player is given an actual value by the proportion of the total number of points they scored. For instance if a player wins 10-0, they scored 10/10 points so their value is 1. If they scored 10-5, they would get a value of 10/15 = .67.
Before that ever happens, however, the players are given expected values using a crazy formula that can be found at the wikipedia link mentioned above. Then how much the player's score needs to be updated is determined by taking the value and subtracting the expected value.
What this means is that if the player does better than expected their Elo rating will increase, and if it was lower their Elo rating will decrease.
What this gets you is a logistic curve in which it gets harder and harder to increase your Elo rating as your Elo rating gets higher and higher.
