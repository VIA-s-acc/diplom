# Readme


### Usage

```py
Usage: DIPLIM_console.exe <config_file_path> [-f <config_file_path>] [-Oi <n>] [-h] [-m <1/2>] [-sf <1/0>] [-lf <1/0>]
```
```bash
Options:
  -h, --help          Show this help message and exit.
  -f, --file <path>   Load the model from a specified configuration file.
  -Oi, --optimization-iterations <n>  Run optimization for n iterations (default is 1).
  -sf, --save-flag <1/0>   Enable or disable save flag (1 = true, 0 = false).
  -lf, --log-flag <1/0>    Enable or disable log flag (1 = true, 0 = false).
  -m,  --method   <1/2/3>    Optimization method (1 = CGD, 2 = GD, 3 = NDFP).
  -r,  --regularization   <f>   Use Regularization with lambda = f
  -d   --diagnostic  <1/0> Find optimal parametrs for selected method (1 = true, 0 = false, currently supports 3: NDFP).
Examples:
  DIPLIM_console.exe config.ini              Load the model from config.json and run optimization.
  DIPLIM_console.exe -f config.ini -Oi 10    Load the model from config.json and run optimization for 10 iterations.
  DIPLIM_console.exe -sf 1 -lf 1               Enable save flag and log flag.
  DIPLIM_console.exe -h                       Show help message.
  DIPLIM_console.exe -f config.ini -d 1 -m 3
```