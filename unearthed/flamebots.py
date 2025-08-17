from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu(range(1,9))

# Based on the selection, run a program.
match selected:
    case "1":
        import Run1_collect
    case "2":
        import Run2_nursery_shark
    case "8":
        import Run8
    case _:
        print('!')