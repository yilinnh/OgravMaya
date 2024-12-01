import maya.cmds as cmds

class RadioBtn:
    def __init__(self, label):
        self.btn = cmds.radioButton(l=label, onCommand=self.on_click)

    def on_click(self, *args):
        global selected_constraint
        selected_constraint = cmds.radioButton(self.btn, q=True, l=True)


def main():
    create_ui()
    on_ofst_check()
    global selected_constraint
    selected_constraint = ""

def create_ui():
    global win
    win = "BatchConstrain"
    global win_w
    win_w = 264
    win_h = 358
    if cmds.window(win, ex=True):
        cmds.deleteUI(win)
    cmds.window(win, t="Batch Constrain", wh=(win_w,win_h), s=False, mnb=False, mxb=False)

    cmds.showWindow(win)

    base_form = cmds.formLayout(p=win)
    global main_form
    main_form = cmds.formLayout(p=base_form)
    option_area = cmds.formLayout(p=main_form)

    header = cmds.text(l="Constraint type:", p=main_form)

    grid = cmds.gridLayout(nc=4, cw=60, p=option_area)
    cmds.radioCollection()
    RadioBtn("Parent")
    RadioBtn("Point")
    RadioBtn("Orient")
    RadioBtn("Scale")
    global ofst_check
    ofst_check = cmds.checkBox(l="Maintain Offset", v=1, changeCommand=on_ofst_check, p=option_area)

    list_title = two_cols_layout()
    cmds.text(l="Drivers")
    cmds.text(l="Drivens")
    list_sub_title = one_col_layout()
    cmds.text(l=">")

    list_cols = two_cols_layout(h=140)
    global driver_list
    global driven_list
    driver_list = cmds.textScrollList(p=list_cols, enableKeyboardFocus=False, allowMultiSelection=True, sc=select_drivers)
    driven_list = cmds.textScrollList(p=list_cols, enableKeyboardFocus=False, allowMultiSelection=True, sc=select_drivens)

    load_btns = create_row_column_layout(2,100,24,main_form)
    cmds.button(l="Load Drivers", command=handle_load_drivers)
    cmds.button(l="Load Drivens", command=handle_load_drivens)

    hr_list = one_col_layout()
    cmds.separator(style="in")
    hr_footer = one_col_layout()
    cmds.separator(style="in")

    footer = create_row_column_layout(3,76,5,main_form)
    cmds.button(l="Apply", command=handle_apply)
    cmds.button(l="Delete", command=handle_delete)
    cmds.button(l="Close", command=handle_close)

    cmds.formLayout(base_form, e=True, af=[(main_form,"top",10), (main_form,"right",10), (main_form,"bottom",10), (main_form,"left",11)])

    cmds.formLayout(main_form, e=True, 
                    af=[(header,"left",4), (option_area,"left",4), (load_btns,"left",8), (load_btns,"right",8)], 
                    ac=[(option_area,"top",4,header), (hr_list,"top",12,option_area), (list_title,"top",4,hr_list), (list_sub_title,"top",4,hr_list),(list_cols,"top",4,list_title), (load_btns,"top",8,list_cols), (hr_footer,"top",8,load_btns), (footer,"top",8,hr_footer)])

    cmds.formLayout(option_area, e=True, ac=[(ofst_check,"top",0,grid)])

def two_cols_layout(**kwargs):
    return create_row_column_layout(2, win_w/2-14, 4, main_form, **kwargs)

def one_col_layout(**kwargs):
    return create_row_column_layout(1, win_w-23, 0, main_form, **kwargs)

def create_row_column_layout(num_of_col, col_width, col_spacing, parent, **kwargs):
    cw = []
    cs = []
    for i in range(num_of_col):
        cw.append((i+1, col_width))
        if i == 0:
            cs.append((i+1, 0)) 
        else:
            cs.append((i+1, col_spacing)) 
    return cmds.rowColumnLayout(nc=num_of_col, cw=cw, cs=cs, p=parent, **kwargs)

def append_sel(list_cols):
    sel = cmds.ls(sl=True)
    all_dags = cmds.ls(dag=True)
    ordered_sel = [i for i in all_dags if i in sel]
    cmds.textScrollList(list_cols, e=True, removeAll=True)
    cmds.textScrollList(list_cols, e=True, a=ordered_sel)

def handle_load_drivers(*args):
    append_sel(driver_list)
    global driver_list_items
    driver_list_items = cmds.textScrollList(driver_list, q=True, allItems=True)

def handle_load_drivens(*args):
    append_sel(driven_list)
    global driven_list_items
    driven_list_items = cmds.textScrollList(driven_list, q=True, allItems=True)


def on_ofst_check(*args):
    global ofst_value
    ofst_value = cmds.checkBox(ofst_check, q=True, v=True)

def select_drivers(*args):
    items = cmds.textScrollList(driver_list, q=True, si=True)
    cmds.select(items)

def select_drivens(*args):
    items = cmds.textScrollList(driven_list, q=True, si=True)
    cmds.select(items)

def handle_apply(*args):
    if len(driver_list_items) != len(driven_list_items):
        print("The quantity of the first group does not match the second group")
        return

    if not selected_constraint:
        print("No constraint selected")
        return

    elif selected_constraint == "Parent":
        for i in driver_list_items:
            cmds.parentConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)
    elif selected_constraint == "Point":
        for i in driver_list_items:
            cmds.pointConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)
    elif selected_constraint == "Orient":
        for i in driver_list_items:
            cmds.orientConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)
    elif selected_constraint == "Scale":
        for i in driver_list_items:
            cmds.scaleConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)


def handle_delete(*args):
    constraints = []

    if not selected_constraint:
        print("No constraint selected")
        return

    elif selected_constraint == "Parent":
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type="parentConstraint"))
    elif selected_constraint == "Point":
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type="pointConstraint"))
    elif selected_constraint == "Orient":
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type="orientConstraint"))
    elif selected_constraint == "Scale":
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type="scaleConstraint"))
    
    cmds.delete(constraints)
    constraints.clear()

def handle_close(*args):
    cmds.deleteUI("BatchConstrain")

#main()