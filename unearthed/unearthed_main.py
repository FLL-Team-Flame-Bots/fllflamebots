from pybricks.tools import hub_menu, run_task
from unearthed_run1 import run1
from unearthed_run2 import run2

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu(range(1,7))

# Based on the selection, run a program.
match selected:
    case "1":
        run_task(run1)
    case "2":
        run_task(run2)
    case _:
        print('!')