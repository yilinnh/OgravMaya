import maya.cmds as cmds

class RadioBtn:
    def __init__(self, key):
        self.key = key
        self.name_dict = {0:"Normal", 1:"Template", 2:"Reference"}
        cmds.radioButton(l=self.name_dict[key], onCommand=self.on_radio_btn)
    
    def on_radio_btn(self, *args):
        global display_type
        display_type = self.key


def main():
    global window
    window = "DisplayType"
    if cmds.window(window, ex=True):
        cmds.deleteUI(window)

    win_w = 264
    win_h = 104
    cmds.window(window, t="Display Type", wh=(win_w,win_h), s=0, mnb=0, mxb=0)
    cmds.showWindow(window)

    base_form = cmds.formLayout(p=window)
    main_form = cmds.formLayout(p=base_form)
    cmds.formLayout(base_form, e=True, af=[(main_form,"top",10), (main_form,"right",10), (main_form,"bottom",10), (main_form,"left",10)])

    f_row = create_row_column_layout(3, win_w/3-4, 0, main_form)
    cmds.radioCollection()
    RadioBtn(0)
    RadioBtn(1)
    RadioBtn(2)
    cmds.rowColumnLayout(f_row, edit=True, cw=[(1,72)])

    global vis_check, vis_value
    s_row = create_row_column_layout(1, win_w-23, 0, main_form)
    vis_check = cmds.checkBox(l="Visibility", v=1, cc=on_checkbox)
    vis_value = cmds.checkBox(vis_check, q=True, v=True)


    bottom_row = create_row_column_layout(2, win_w/2-15, 8, main_form)
    cmds.button(l="Apply", command=handle_apply)
    cmds.button(l="Close", command=handle_close)

    cmds.formLayout(main_form, e=True, 
                    af=[(f_row,"left",4), (s_row,"left",4), (bottom_row,"bottom",0)], 
                    ac=[(s_row,"top",4,f_row)])

    # create_set()
    initialize_sets()



# def create_set():
#     global root_set, display_sets, tem_set, ref_set, vis_set
#     root_set = "displayTypeSet"
#     display_sets = ["T", "R", "H"]
#     tem_set, ref_set, vis_set = display_sets
#     initialize_sets()


def initialize_sets():
    global root_set, display_sets, tem_set, ref_set, vis_set
    root_set = "displayTypeSet"
    selector_set = "selectionSet"
    display_sets = ["T", "R", "H"]
    tem_set, ref_set, vis_set = display_sets
    all_sets = cmds.listSets(allSets=True)

    if selector_set in all_sets:
        for i in display_sets:
            if i not in all_sets:
                cmds.sets(n=i, empty=True)
                cmds.sets(i, e=True, forceElement=selector_set)
    elif root_set in all_sets:
        for i in display_sets:
            if i not in all_sets:
                cmds.sets(n=i, empty=True)
                cmds.sets(i, e=True, forceElement=root_set)
    elif root_set not in all_sets:
        cmds.sets(n=root_set, empty=True)
        for i in display_sets:
            if i not in all_sets:
                cmds.sets(n=i, empty=True)
                cmds.sets(i, e=True, forceElement=root_set)


def create_row_column_layout(num_of_col, col_width, col_spacing, parent):
    cw = []
    cs = []

    for i in range(num_of_col):
        cw.append((i+1, col_width))
        if i == 0:
            cs.append((i+1, 0)) 
        else:
            cs.append((i+1, col_spacing)) 

    return cmds.rowColumnLayout(nc=num_of_col, cw=cw, cs=cs, p=parent)


def on_checkbox(*args):
    global vis_value
    vis_value = cmds.checkBox(vis_check, q=True, v=True)


def handle_apply(*args):
    sel = cmds.ls(sl=True)

    if not sel:
        print("No objects selected")
        return

    # initialize_sets()

    for i in sel:
        cmds.setAttr(f"{i}.overrideEnabled", 1)
        cmds.setAttr(f"{i}.overrideDisplayType", display_type)
        cmds.setAttr(f"{i}.visibility", vis_value)

        if display_type == 0:
            cmds.sets(remove=tem_set)
            cmds.sets(remove=ref_set)
        elif display_type == 1:
            cmds.sets(add=tem_set)
            cmds.sets(remove=ref_set)
        elif display_type == 2:
            cmds.sets(add=ref_set)
            cmds.sets(remove=tem_set)
        
        if vis_value == 0:
            cmds.sets(add=vis_set)
        elif vis_value == 1:
            cmds.sets(remove=vis_set)


def handle_close(*args):
    cmds.deleteUI("DisplayType")

def test():
    print("this is the display type")

# main()