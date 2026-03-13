# Space Shooter Game

A grid-based space shooter game written in Python using Tkinter for the GUI and NumPy for the game state grid.

## Status

> ⚠️ **Work in Progress** — Core mechanics are functional but the game is still being developed.

## Features

- **Player movement** — Arrow keys or WASD to move in all four directions on a 16×16 grid
- **Shooting** — Press Space to fire bullets upward
- **Enemies** — Spawn randomly at the top and descend; two types: `weak` (1 HP) and `strong` (2 HP)
- **Collision detection** — Bullets reduce enemy HP; enemies that reach the player deal damage
- **Power-ups** — 10% drop chance from destroyed enemies (currently collected but not yet active)
- **Player health** — 3 HP; game ends at 0

## Grid Cell Codes

| Value | Entity |
|---|---|
| 0 | Empty |
| 1 | Player (white) |
| 2 | Enemy (red) |
| 3 | Bullet (yellow) |
| 4 | Power-up (blue) |

## Requirements

```bash
pip install numpy
```

Tkinter is included with standard Python installations.

## Run

```bash
python main.py
```

## Controls

| Key | Action |
|---|---|
| Arrow Keys / WASD | Move player |
| Space | Shoot |

## Planned Features

- Different enemy behaviours
- Active power-up effects
- Scoring system and level progression
- Sound effects and background music
- Improved visual design
