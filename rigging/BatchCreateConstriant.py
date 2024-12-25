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
    selected_constraint = 'Parent'

def create_ui():
    global win
    win = 'BatchConstrain'
    global win_w
    win_w = 270
    win_h = 352
    if cmds.window(win, ex=True):
        cmds.deleteUI(win)
    cmds.window(win, t='Batch Constrain', wh=(win_w,win_h), s=False, mnb=False, mxb=False)

    cmds.showWindow(win)

    base_form = cmds.formLayout(p=win)
    global ofst_form
    ofst_form = cmds.formLayout(p=base_form)
    option_area = cmds.formLayout(p=ofst_form)

    header = cmds.text(l='Constraint Type:', p=ofst_form)

    grid = cmds.gridLayout(nc=4, cw=60, p=option_area)
    cmds.radioCollection()
    parent_radio_btn = RadioBtn('Parent')
    RadioBtn('Point')
    RadioBtn('Orient')
    RadioBtn('Scale')

    # select the parent radio btn by default
    cmds.radioButton(parent_radio_btn.btn, e=True, sl=True)

    global ofst_check
    ofst_check = cmds.checkBox(l='Maintain Offset', v=1, changeCommand=on_ofst_check, p=option_area)

    list_title_form = cmds.formLayout(p=ofst_form)
    two_col_form(list_title_form, cmds.text(l='Drivers'), cmds.text(l='Drivens'))

    list_sub_title_form = cmds.formLayout(p=ofst_form) 
    one_col_form(list_sub_title_form, cmds.text(l='>'))

    # list_cols_form = two_cols_layout(h=140)
    list_cols_form = cmds.formLayout(p=ofst_form)
    global driver_list, driven_list
    driver_list = cmds.textScrollList(p=list_cols_form, enableKeyboardFocus=False, allowMultiSelection=True, sc=select_drivers, h=140)
    driven_list = cmds.textScrollList(p=list_cols_form, enableKeyboardFocus=False, allowMultiSelection=True, sc=select_drivens, h=140)
    two_col_form(list_cols_form, driver_list, driven_list)

    load_btns_form = cmds.formLayout(p=ofst_form)
    load_drivers_btn = cmds.button(l='Load Drivers', command=handle_load_drivers)
    load_drivens_btn = cmds.button(l='Load Drivens', command=handle_load_drivens)
    cmds.formLayout(load_btns_form, e=True,
                    ap=[(load_drivers_btn,'left',0,8),
                        (load_drivers_btn,'right',0,42),
                        (load_drivens_btn,'left',0,58),
                        (load_drivens_btn,'right',0,92),
                    ])

    hr_list_form = cmds.formLayout(p=ofst_form)
    one_col_form(hr_list_form, cmds.separator(style='in'))
    hr_footer_form = cmds.formLayout(p=ofst_form)
    one_col_form(hr_footer_form, cmds.separator(style='in'))

    footer_form = cmds.formLayout(p=ofst_form)
    three_col_form(footer_form, 
                   cmds.button(l='Apply', command=handle_apply), 
                   cmds.button(l='Delete', command=handle_delete), 
                   cmds.button(l='Close', command=handle_close))

    cmds.formLayout(base_form, e=True, af=[(ofst_form,'top',10), (ofst_form,'right',10), (ofst_form,'bottom',10), (ofst_form,'left',10)])

    cmds.formLayout(ofst_form, e=True, 
                    af=[(header,'left',4), 
                        (option_area,'left',4), 
                        (list_title_form,'left',0),
                        (list_title_form,'right',0),
                        (list_sub_title_form,'left',0),
                        (list_sub_title_form,'right',0),
                        (list_cols_form,'left',0),
                        (list_cols_form,'right',0),
                        (load_btns_form,'left',0),
                        (load_btns_form,'right',0),
                        (hr_list_form,'left',0),
                        (hr_list_form,'right',0),
                        (hr_footer_form,'left',0),
                        (hr_footer_form,'right',0),
                        (footer_form,'left',0),
                        (footer_form,'right',0),
                    ], 
                    ac=[(option_area,'top',4,header), 
                        (hr_list_form,'top',12,option_area), 
                        (list_title_form,'top',4,hr_list_form), 
                        (list_sub_title_form,'top',4,hr_list_form),
                        (list_cols_form,'top',4,list_title_form), 
                        (load_btns_form,'top',8,list_cols_form), 
                        (hr_footer_form,'top',8,load_btns_form), 
                        (footer_form,'top',8,hr_footer_form)])

    cmds.formLayout(option_area, e=True, ac=[(ofst_check,'top',0,grid)])


def one_col_form(form, col):
    cmds.formLayout(form, e=True, af=[(col,'left',0), (col,'right',0)])

def two_col_form(form, l_col, r_col):
    cmds.formLayout(form, e=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,49), (r_col,'left',0,51)])

def three_col_form(form, l_col, m_col, r_col):
    cmds.formLayout(form, edit=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,33), (m_col,'left',0,34), (m_col,'right',0,66), (r_col,'left',0,67)])

def append_sel(list_cols_form):
    sel = cmds.ls(sl=True)
    cmds.textScrollList(list_cols_form, e=True, removeAll=True)
    # cmds.textScrollList(list_cols_form, e=True, a=ordered_sel)
    cmds.textScrollList(list_cols_form, e=True, a=sel)

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
        print("The quantity of drivers does not match drivens'")
        return

    if not selected_constraint:
        print("No constraint selected")
        return

    elif selected_constraint == 'Parent':
        for i in driver_list_items:
            cmds.parentConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)
    elif selected_constraint == 'Point':
        for i in driver_list_items:
            cmds.pointConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)
    elif selected_constraint == 'Orient':
        for i in driver_list_items:
            cmds.orientConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)
    elif selected_constraint == 'Scale':
        for i in driver_list_items:
            cmds.scaleConstraint(i, driven_list_items[driver_list_items.index(i)], maintainOffset=ofst_value)


def handle_delete(*args):
    constraints = []

    if not selected_constraint:
        print('No constraint selected')
        return

    elif selected_constraint == 'Parent':
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type='parentConstraint'))
    elif selected_constraint == 'Point':
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type='pointConstraint'))
    elif selected_constraint == 'Orient':
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type='orientConstraint'))
    elif selected_constraint == 'Scale':
        for i in driven_list_items:
            constraints += (cmds.listRelatives(i, c=True, type='scaleConstraint'))
    
    cmds.delete(constraints)
    constraints.clear()

def handle_close(*args):
    cmds.deleteUI('BatchConstrain')
    global selected_constraint, driver_list_items, driven_list_items
    selected_constraint = ''
    driver_list_items = []
    driven_list_items = []

# main()