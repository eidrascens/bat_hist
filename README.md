# Battery History

A simple Python script to analyze the battery consumption
based on number of minutes per 1% decreased logged in
`/var/lib/upower/*.dat`.

# Installation

Determine the location of your battery information file (usually inside
`/var/lib/upower/` and ending in `.dat`) (_e.g._ `history-charge-ASUS_Battery-63.dat`)
and replace the variable `BAT_DIR` at line #116 in `bat_hist.py` with
the absolute path of the battery file.

Place `src/bat_hist.py` inside any of your `$PATH` (_e.g._ `$HOME/.local/bin`
(RECOMMENDED)) and create a virtual environment at the same DIR of `bat_hist.py`
with

```bash
python -m venv venv
```

Hereafter, activate the virtual environment with `source venv/bin/activate.*`
(replace with appropriate extension, _e.g._ `.fish` for FISH). Install the
dependencies with

```
pip install numpy==2.5.4 psutil==7.2.2
```

Finally, create an alias for `<DIR>/venv/bin/python <DIR>/bat_hist.py`.

# Output

Example output:

```
Batt_i = 80, Time_i = 03:17:05, Time_f = 03:17:56, Time_d = 0.85 min
Batt_i = 79, Time_i = 03:17:56, Time_f = 03:30:56, Time_d = 13.0 min
Batt_i = 78, Time_i = 03:30:56, Time_f = 09:35:55, Time_d = 06 hr 04 min (364.98 min)
Batt_i = 76, Time_i = 09:35:55, Time_f = 13:20:02, Time_d = 03 hr 44 min (224.12 min)
Batt_i = 74, Time_i = 13:20:02, Time_f = 13:27:09, Time_d = 7.12 min
Batt_i = 73, Time_i = 13:27:09, Time_f = 14:08:03, Time_d = 40.9 min
Batt_i = 72, Time_i = 14:08:03, Time_f = 14:13:33, Time_d = 5.5 min
Batt_i = 71, Time_i = 14:13:33, Time_f = 14:19:03, Time_d = 5.5 min
Batt_i = 70, Time_i = 14:19:03, Time_f = 14:28:34, Time_d = 9.52 min
Batt_i = 69, Time_i = 14:28:34, Time_f = 14:35:04, Time_d = 6.5 min
Batt_i = 68, Time_i = 14:35:04, Time_f = 14:40:04, Time_d = 5.0 min
Batt_i = 67, Time_i = 14:40:04, Time_f = 14:48:05, Time_d = 8.02 min
Batt_i = 66, Time_i = 14:48:05, Time_f = 14:54:35, Time_d = 6.5 min
Batt_i = 65, Time_i = 14:54:35, Time_f = 15:03:36, Time_d = 9.02 min
Batt_i = 64, Time_i = 15:03:36, Time_f = 15:10:06, Time_d = 6.5 min
=========================================================================================
Outliers removed: [0.85, 13.0, 364.98, 224.12, 40.9]
Median Minute / 1% = 6.92 min
Mean Minute / 1% = 6.50 min
Mean % Consumed / Minute = 0.14%
Median % Consumed / Minute = 0.15%
Total Time Used (Clean) = 01 hr 09 min (69.18 min)
Total Time Used (Gross) = 11 hr 53 min (713.03 min)
```
