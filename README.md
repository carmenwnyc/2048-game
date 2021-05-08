# 2048-Game

## 2048-Game Explained
* A demo of the original game in this website: http://gabrielecirulli.github.io/2048

## 2048 As A Two-Player Game
* 2048 is played on a 4x4 grid with numbered tiles which can slide up, down, left, or right. This game is now modeled as a two player game, in which the computer AI generates a 2- or 4-tile placed randomly on the board, and the AI player then selects a direction to move the tiles. Note that the tiles move until they either (1) collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide in a move, they merge into a single tile valued at the sum of the two originals. The resulting tile cannot merge with another tile again in the same move. Computer AI places tiles and the Player moves them.

## Program Explained
* The program is implemented with Adversarial Search Algorithm. It assumes Intelligent agent will take every step that maximizes its chances to win. However, different from the standard adversarial search algorithm, Computer AI is not adversarial. The tile-generating Computer AI of 2048 is not particularly adversarial as it spawns tiles irrespective of whether a spawn is the most adversarial to the user’s progress, with a 90% probability of a 2 and 10% for a 4 (from GameManager.py).Player AI will play as if the computer AI is adversarial since this proves more effective in beating the game.
* Adversarial Search Algorithm and Expectiminimax:
1. https://computing.dcu.ie/~humphrys/Notes/AI/adversarial.search.html#:~:text=Adversarial%20search%20is%20search%20when,unpredictable
2. https://en.wikipedia.org/wiki/Expectiminimax

## Heuristics
* monotonicity heuristics
  1. Reference: http://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
* Smoothness heuristic, which measures the difference between neighboring tiles and tries to minimize this count
  1. Reference: https://github.com/ronzil/2048-AI/blob/master/js/grid.js
* Heuristics that measures the number of mergable cells and empty cells in the whole board
