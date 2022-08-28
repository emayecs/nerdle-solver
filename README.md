# nerdle-solver
Solver for the Classic mode of the math game [Nerdle](https://nerdlegame.com/)

Instructions:

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
