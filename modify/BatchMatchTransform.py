import maya.cmds as cmds
import maya.api.OpenMaya as om
from functools import partial

def main():
    create_ui()
    create_sel_callback()

def create_ui():
    win = "BatchMatch"
    global win_w
    global win_h
    win_w = 250
    win_h = 182

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t="Batch Match", wh=(win_w,win_h), mxb=False, mnb=False, s=False, cc=cleanup_callback)
    cmds.showWindow(win)

    global main_form
    base_form = cmds.formLayout()
    main_form = cmds.formLayout(p=base_form)

    cmds.formLayout(base_form, e=True, af=[(main_form,"top",10),(main_form,"right",10),(main_form,"bottom",10),(main_form,"left",11)])

    list_titles = two_cols_layout()
    cmds.text(l="From")
    cmds.text(l="To")
    list_sub_title = one_col_layout()
    cmds.text(l=">")

    list_cols = two_cols_layout(h=100)
    global from_list
    global to_list
    from_list = cmds.textScrollList(p=list_cols, enableKeyboardFocus=False, allowMultiSelection=True)
    to_list = cmds.textScrollList(p=list_cols, enableKeyboardFocus=False, allowMultiSelection=True)

    btns_row = cmds.rowColumnLayout(nc=5,cw=[(1,93),(2,25),(3,25),(4,25),(5,50)], cs=[(1,0),(2,4),(3,0),(4,0),(5,4)], p=main_form)
    cmds.button(l="All Transforms", c=match_pattern)
    cmds.button(l="T", c=partial(match_pattern, pos=True))
    cmds.button(l="R", c=partial(match_pattern, rot=True))
    cmds.button(l="S", c=partial(match_pattern, scl=True))
    cmds.button(l="Pivots", c=partial(match_pattern, piv=True))

    cmds.formLayout(main_form, e=True, 
                    af=[list_titles,"top",0],
                    ac=[(list_cols,"top",4,list_titles), (btns_row,"top",12,list_cols)])

    update_sel_callback()


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
    return create_row_column_layout(2, win_w/2-14, 4, main_form, **kwargs)

def one_col_layout(**kwargs):
    return create_row_column_layout(1, win_w-23, 0, main_form, **kwargs)


def match_pattern(*args, **kwargs):
    from_list_items = cmds.textScrollList(from_list, q=True, ai=True)
    to_list_items = cmds.textScrollList(to_list, q=True, ai=True)
    for i in from_list_items:
        cmds.matchTransform(i, to_list_items[from_list_items.index(i)], **kwargs)


def create_sel_callback():
    global callback_id
    callback_id = om.MEventMessage.addEventCallback("SelectionChanged", update_sel_callback)


def update_sel_callback(*args):
    cmds.textScrollList(from_list, e=True, ra=True)
    cmds.textScrollList(to_list, e=True, ra=True)
    sel = cmds.ls(sl=True)
    if sel:
        half_sel_len = int(len(sel)/2)
        # print(sel[0])
        f_list = sel[:half_sel_len]
        s_list = sel[half_sel_len:]
        if len(f_list) != len(s_list):
            cmds.textScrollList(from_list, e=True, a=sel)
        else:
            cmds.textScrollList(from_list, e=True, a=f_list)
            cmds.textScrollList(to_list, e=True, a=s_list)
    

def cleanup_callback():
    global callback_id
    if callback_id:
        om.MMessage.removeCallback(callback_id)
        callback_id = None


# main()