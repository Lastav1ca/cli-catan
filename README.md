# cli-catan

CLI version of the board game Catan, written in Python.

## Features

- 2–4 player hotseat play in the terminal
- Randomized hex board with resources, number tokens, and robber
- Full setup phase: snake-order settlement + road placement, starting resources from the second settlement
- Turn loop: dice roll, resource production, robber on 7 (discard + steal)
- Build settlements, cities, roads
- Development cards: Knight, Road Building, Year of Plenty, Monopoly, Victory Point
- 4:1 bank trades
- Win condition: first to 10 victory points

## Requirements

- Python 3.7+ (uses `sys.stdout.reconfigure`)
- A terminal with Unicode + ANSI color support

## Run

```bash
cd src
python3 main.py
```

## Not implemented (yet)

- Longest road / largest army bonus VPs
- Player-to-player trading
- Ports / better-than-4:1 trades
- Hidden VP dev cards (currently counted immediately)
