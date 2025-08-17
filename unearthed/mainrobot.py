from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu(range(1,9))

# Based on the selection, run a program.
match selected:
    case "1":
        import sample_setup_run    
    case _:
        print('!')