from pybricks.tools import hub_menu, StopWatch

from pybricks.hubs import PrimeHub
from pybricks.tools import hub_menu, run_task, wait

hub = PrimeHub()

def better_menu(*options):
    options = list(options)

    last_selection = int(hub.system.storage(99, read=1)[0])
    if last_selection not in options:
        last_selection = options[0]
    
    next_idx = (options.index(last_selection) + 1) % len(options)
    options = options[next_idx:] + options[:next_idx]

    selection = hub_menu(*tuple((chr(48 + o) for o in options)))
    selection_num = ord(selection) - 48
    hub.system.storage(99, write=bytes([selection_num]))

    return selection_num

# Based on the selection, run a program.
def main():
    selected = better_menu(1, 2, 3, 4, 5, 6, 7, 8)
    print(f"Selected {selected}")
    run_watch = StopWatch()
    if selected == 1:
        import unearthed_v2_forge
    elif selected == 2:
        import unearthed_v2_scale
    elif selected == 3:
        import unearthed_v2_silo
    elif selected == 4:
        import unearthed_v2_statue
    elif selected == 5:
        import unearthed_v2_ship
    elif selected == 6:
        import unearthed_v2_mapreveal
    elif selected == 7:
        import unearthed_v2_mineshaft
    elif selected == 8:
        import unearthed_v2_final
    print(f"{selected} stopped, time {run_watch.time()}(ms)")
    hub.speaker.beep(500, 500)

main()