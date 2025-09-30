from pybricks.hubs import PrimeHub
from pybricks.tools import hub_menu, run_task, wait

hub = PrimeHub()

def better_menu(*options):
    options = list(options)

    last_selection = int(hub.system.storage(99, read=1)[0])
    if last_selection not in options:
        last_selection = options[-1]
    
    next_idx = (options.index(last_selection) + 1) % len(options)
    options = options[next_idx:] + options[:next_idx]

    selection = hub_menu(*tuple((chr(48 + o) for o in options)))
    selection_num = ord(selection) - 48
    hub.system.storage(99, write=bytes([selection_num]))

    return selection_num


def main():
    selected = better_menu(0, 1, 2, 3, 4, 5, 6)
    if selected == 0:
 #       import Run_1_2_15_2025_collect
    elif selected == 1:
        hub.display.text('ONE')
        #import Swiper3001_far
    elif selected == 2:
        hub.display.text('TWO')
        #import Krakens_Chest
    elif selected == 3:
        hub.display.text('THREE')
        #import FLLSubmerged_M1_M2_M3
    elif selected == 4:
        hub.display.text('FOUR')
        #import Left_To_Right
    elif selected == 5:
        hub.display.text('FIVE')
        #import sonarwhale
    elif selected == 6:
        hub.display.text('SIX')
        #import mission8

   
 
main()
    
        