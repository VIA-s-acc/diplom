# Readme


### Usage
Path [.exe](cppCode\DIPLIM_console\x64\Debug\DIPLIM_console.exe)

```py
Usage: DIPLIM_console.exe <config_file_path> [-f <config_file_path>] [-Oi <n>] [-h]
```
```bash
Options:
  -h, --help          Show this help message and exit.
  -f, --file <path>   Load the model from a specified configuration file.
  -Oi, --optimization-iterations <n>  Run optimization for n iterations (default is 1).
  -sf, --save-flag <1/0>   Enable or disable save flag (1 = true, 0 = false).
  -lf, --log-flag <1/0>    Enable or disable log flag (1 = true, 0 = false).

Examples:
  DIPLIM_console.exe config.ini              Load the model from config.json and run optimization.
  DIPLIM_console.exe -f config.ini -Oi 10    Load the model from config.json and run optimization for 10 iterations.
  DIPLIM_console.exe -sf 1 -lf 1               Enable save flag and log flag.
  DIPLIM_console.exe -h                       Show help message.
```