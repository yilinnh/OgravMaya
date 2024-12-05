import maya.cmds as cmds

class RadioBtn:
    def __init__(self, label):
        self.btn = cmds.radioButton(l=label, changeCommand=self.on_click)
        self.value = 0

    def on_click(self, *args):
        select_state = cmds.radioButton(self.btn, q=True, select=True)
        if select_state:
            self.value = 1
        else:
            self.value = 0


def main():
    create_ui()
    # create_controls()

def create_ui():
    global win, win_w, win_h
    win = 'newWindow'
    win_w = 200
    win_h = 100
    
    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t='New Window', wh=(win_w,win_h), mxb=False, mnb=False, s=False)
    cmds.showWindow(win)

    global main_form
    base_form = cmds.formLayout()
    main_form = cmds.formLayout(p=base_form)

    cmds.formLayout(base_form, e=True, af=[(main_form,'top',10),(main_form,'right',10),(main_form,'bottom',10),(main_form,'left',10)])

    header = cmds.text(l='Primary Axis:')
    primary_axis_row = create_row_column_layout(3, 30, 4, main_form)
    cmds.radioCollection()
    global x_axis_radio, y_axis_radio, z_axis_radio
    x_axis_radio = RadioBtn('X')
    y_axis_radio = RadioBtn('Y')
    z_axis_radio = RadioBtn('Z')

    footer_btns_row = two_cols_layout()
    cmds.button(l='Apply', c=handle_apply)
    cmds.button(l='Cancel')

    cmds.formLayout(main_form, e=True, af=[(footer_btns_row,'bottom',0)],
                    ac=[(primary_axis_row,'top',4,header)])
    

def create_row_column_layout(num_of_col, col_width, col_spacing, parent, **kwargs):
    cw = []
    cs = []
    for i in range(num_of_col):
        cw.append((i+1, col_width))
        if i == 0:
            cs.append((i+1, 0))
        else:
            cs.append((i+1, col_spacing))
    return cmds.rowColumnLayout(nc=num_of_col, cw=cw, cs=cs, p=parent, adj=True, **kwargs)

def two_cols_layout(**kwargs):
    return create_row_column_layout(2, win_w/2-13, 4, main_form, **kwargs)


def handle_apply(*args):
    sel = cmds.ls(sl=True)
    if not sel: 
        print("No objects selected")
        return

    global primary_axis
    primary_axis = (x_axis_radio.value, y_axis_radio.value, z_axis_radio.value)

    ctrl_list = []

    for jnt in sel:
        ctrl = cmds.circle( normal=primary_axis, c=(0,0,0), n=f"{jnt}_Ctrl")[0]
        cmds.matchTransform(ctrl, jnt)
        ctrl_list.append(ctrl)

    cmds.select(ctrl_list)




# main()