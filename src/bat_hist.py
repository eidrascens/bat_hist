from datetime import datetime as dt, timedelta
from os import get_terminal_size, remove
from os.path import dirname, realpath
from pathlib import Path
from statistics import mean, median
from subprocess import CalledProcessError, DEVNULL, call

from psutil import sensors_battery

import numpy as np


def remove_outliers(data: list[float]) -> tuple[np.array, np.array]:
    THRESHOLD: float = 2
    d = np.abs(data - np.median(data))
    m = np.median(d)
    s = d / m if m else np.zeros(len(d))
    return (data[s < THRESHOLD], data[s > THRESHOLD])


def format_minutes(time_min: float) -> str:
    return (
            "{:02d} hr {:02d} min ({time_min:.2f} min)"
        ).format(
            *divmod(int(time_min), 60), time_min=time_min
        ) if time_min > 60.0 else f"{time_min} min"


def analyze_bat(file: Path) -> None:
    with open(file, "r", encoding="utf-8") as bat_file:
        bat_hist: list[str] = bat_file.readlines()

    bat_info_arr: list[tuple[float, str]] = []

    for line in bat_hist[::-1]:
        bat_stat: str = line[34:].strip()
        bat_p: float = round(float(line[27:34].strip()), 2)
        log_time: str = line[6:17].strip()

        #print(bat_p)
        if bat_stat in ["discharging", "pending-charge"]:
            bat_info_arr.append(
                (bat_p, log_time)
            )

        if int(bat_p) == 80:
            break

    FMT = "%H:%M:%S"
    bat_info_arr.reverse()

    time_delta_arr: list[float] = []
    for i in range(0, len(bat_info_arr) - 1):
        time_i: dt = dt.strptime(bat_info_arr[i][1], FMT)
        time_f: dt = dt.strptime(bat_info_arr[i+1][1], FMT)
        time_f = time_f + timedelta(hours=24) if time_f < time_i else time_f

        time_delta: timedelta = time_f - time_i
        time_delta_m: float = round(
                time_delta.total_seconds() / 60, 2
            )

        time_delta_arr.append(time_delta_m)
        time_delta_str: str = format_minutes(time_delta_m)

        print(
            (
                "Batt_i = %i, "
                "Time_i = %s, "
                "Time_f = %s, "
                "Time_d = %s"
            ) % (
                bat_info_arr[i][0],
                time_i.time(),
                time_f.time(),
                time_delta_str
            )
        )

    clean_time_delta_arr, time_delta_out = remove_outliers(
            np.array(time_delta_arr)
        )
    mean_time_delta: float = mean(clean_time_delta_arr)
    median_time_delta: float = median(clean_time_delta_arr)
    total_time_used_clean: str = format_minutes(
            sum(clean_time_delta_arr)
        )
    total_time_used_raw: str = format_minutes(
            sum(time_delta_arr)
        )

    print("=" * get_terminal_size()[0])
    print(
        (
            "Outliers removed: {}\n"
            "Median Minute / 1% = {:.2f} min\n"
            "Mean Minute / 1% = {:.2f} min\n"
            "Mean % Consumed / Minute = {:.2f}%\n"
            "Median % Consumed / Minute = {:.2f}%\n"
            "Total Time Used (Clean) = {}\n"
            "Total Time Used (Gross) = {}"
        ).format(
            time_delta_out.tolist(),
            mean_time_delta,
            median_time_delta,
            1 / mean_time_delta,
            1 / median_time_delta,
            total_time_used_clean,
            total_time_used_raw
        )
    )

def main() -> None:
    CWD: Path = Path(dirname(realpath(__file__)))
    temp_file: Path = CWD / "bat.temp"
    BAT_DIR: str = "/var/lib/upower/history-charge-ASUS_Battery-63.dat"

    curr_bat_p: int = int(round(sensors_battery().percent, 0))
    diff: int = 80 - curr_bat_p

    get_lines: int = diff + int(round(curr_bat_p / diff, 0))

    CMD: str = " ".join(
            [
                "tail",
                "-n",
                f"{get_lines}",
                BAT_DIR,
                "|",
                "while read f; do",
                r'd=$(date +"%b %e %H:%M:%S"',
                r'-d @`echo $f | cut -d\  -f1`);',
                f'echo "$d  $f" >> {temp_file};',
                "done"
            ]
        )

    try:
        call(
            CMD,
            shell=True,
            stdin=DEVNULL,
            stdout=DEVNULL,
            stderr=DEVNULL
        )
    except (SystemError, CalledProcessError) as _:
        print(f"Encountered an error excuting {CMD}")
    else:
        analyze_bat(temp_file)
        remove(temp_file)


main()
