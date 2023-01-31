"""
This module provides a function called `prange` that displays a progress bar while looping through a range or an iterable.
The progress bar also displays the percentage of completion and the current iteration count.
"""

import time
import colorama as cl
from typing import Optional, Callable
cl.init()

def prange(stop: int = None, start: int = 0, step: int = 1, iterable: Optional[list]=None, task: Optional[str]=None, fn: Optional[Callable]=None) -> None:
    """
    Progress Bar Range

    This function displays a progress bar in the console, it can be used with a range of numbers or an iterable, if an iterable is provided, the length of the iterable will be used as the `stop` value.

    Args:
    stop (int, optional): Where to stop at. Required if `iterable` is not provided.
    start (int, optional): Where to start at. Defaults to 0.
    step (int, optional): How much to step per iteration. Defaults to 1.
    iterable (Iterable, optional): The iterable to loop through. Defaults to None.
    task (str, optional): The task message. Defaults to None
    fn (Callable, optional): A function to execute at every iteration. Defaults to None.

    Returns:
    None
    """
    if not task and iterable and not stop:
        task = "Loop through iterable"
    elif not iterable and stop and not task:
        task = "Summon progressbar"

    if iterable:
        stop = len(iterable)

    print(f"Task: {task}")

    for i in range(start, stop, step):
        range_ = stop - start
        corrected_start_value = i - start
        percentage = int((corrected_start_value * 100) / range_)
        bar = "⎯" * percentage
        print(cl.Style.RESET_ALL, end="\r")
        if percentage < 20:
            color = ""
        elif 20 <= percentage < 50:
            color = cl.Fore.YELLOW
        elif 50 <= percentage < 70:
            color = cl.Fore.MAGENTA
        elif 70 <= percentage < 90:
            color = cl.Fore.BLUE
        else:
            color = cl.Fore.GREEN
        print(f"{color}{bar}{cl.Style.RESET_ALL} [{i+1}/{stop} {percentage}%]", end="\r")
        time.sleep(0.1)
        if fn:
            fn(iterable[i] if iterable else i)
    print("\n")
