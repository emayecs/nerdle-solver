# nerdle-solver
Solver for the Classic mode of the math game [Nerdle](https://nerdlegame.com/)

## Instructions

The program has three functions: solve, play, and simulate. 

- **Solve** solves a Nerdle given a guess and it's colorcoded result
- **Play** allows the user to play a game of Nerdle
- **Simulate** simulates solving a Nerdle

### Solve

Enter a guess into Nerdle—e.g. "12+35=47."
Record the colors as an 8-length string, with the following characters corresponding to each character: 

- p - purple
- g - green
- b - black

Run solve by entering the guess and result as arguments. The program will print the optimal guess and take in the results of entering each guess until the Nerdle is solved.

Example:

```
python3 main.py solve 12+35=47 pbpbbpbb
Best Guess: 86=96-10
Probability: 0.06261740763932373%
Enter the result.
gbppbppp
Best Guess: 89*0+1=1
Probability: 0.5649717514124294%
Enter the result.
gpbpppgb
Best Guess: 8-0/19=8
Probability: 4.545454545454546%
Enter the result.
ggpbgpgb
Best Guess: 8-9+10=9
Probability: 100.0%
```

### Play

Play a nerdle game by running the "play" method and entering your guesses. Note that the terminal will color-code each input to reflect the guess's accuracy.

Example:

```
python3 main.py play                   

████████
████████
████████
████████
████████
████████

12+35=47

12+35=47
████████
████████
████████
████████
████████

68*0+9=9

12+35=47
68*0+9=9
████████
████████
████████
████████

35*0+3=3

12+35=47
68*0+9=9
35*0+3=3
████████
████████
████████

33*0+5=5

12+35=47
68*0+9=9
35*0+3=3
33*0+5=5
████████
████████

30*0+5=5
```

### Simulate

Simulates solving a number of Nerdle games. Run simulate and enter the number of desired simulations. Note that the terminal will color-code each equation to reflect the guess's accuracy.

Example:

```
python3 main.py simulate 3
Equation: 52-3=7*7
35+46=81
7=9*3-20
52-7*7=3
52-3=7*7

Equation: 81=33+48
35+46=81
78=90-12
81=38+43
81=33+48

Equation: 10-9/1=1
35+46=81
70=91-21
10-9*1=1
10-9/1=1
```
