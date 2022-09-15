# nerdle-solver
Utility program for the math game [Nerdle](https://nerdlegame.com/)

## Instructions

The program has three functions: solve, play, and simulate. 

- **Solve** solves a Nerdle given a guess and it's colorcoded result
- **Play** starts a game of Nerdle
- **Simulate** simulates solving a Nerdle

### Shared Arguments

As of September 2022, Nerdle doesn't include equations with lone zeros, leading zeros, or negative numbers. As a result, the user can filter out equations to be used for any function by including any of these arguments:
- ```--no_negatives``` - Equations with with negative numbers will not be included (e.g. -4*3=-12)
- ```--no_leading_zeroes``` - Equations with leading zeroes will not be included (e.g. 004*3=12)
- ```--dne_zero``` - Equations that equal 0 will not be included (e.g. 0*9999=0)

If none of these arguments are given, the program will deem all equations as fair game.

### Solve

#### Arguments

- ```guess``` - the guess for the equation e.g. "12+35=47."
- ```result``` - an 8-length string with the following characters corresponding to each color: 
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

Play a nerdle game by running the "play" method and entering your guesses. The terminal will color-code each input to reflect the guess's accuracy.

#### Arguments
- ```chances``` - the number of chances that the user gets to guess the equation

### Simulate

Simulates solving a number of Nerdle games. Run simulate and enter the number of desired simulations. The terminal will color-code each equation to reflect the guess's accuracy.

#### Arguments
- ```iterations``` - number of simulations to run
- ```first_guess``` - the first guess to be used for the simulations
- ```chances``` - the number of chances that the simulator gets to guess the equation
