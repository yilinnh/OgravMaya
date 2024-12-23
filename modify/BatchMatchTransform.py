import maya.cmds as cmds
import maya.api.OpenMaya as om
from functools import partial

def main():
    create_ui()
    create_sel_callback()

def create_ui():
    win = 'BatchMatch'
    global win_w
    global win_h
    win_w = 250
    win_h = 214

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t='Batch Match', wh=(win_w,win_h), mxb=False, mnb=False, s=False, cc=cleanup_callback)
    cmds.showWindow(win)

    global ofst_form
    base_form = cmds.formLayout()
    ofst_form = cmds.formLayout(p=base_form)

    cmds.formLayout(base_form, e=True, af=[(ofst_form,'top',10),(ofst_form,'right',10),(ofst_form,'bottom',10),(ofst_form,'left',10)])

    list_title_form = cmds.formLayout(p=ofst_form)
    source_title = cmds.text(l='From')
    target_title = cmds.text(l='To')
    two_col_form(list_title_form, source_title, target_title)

    list_sub_title_form = cmds.formLayout(p=ofst_form)
    sub_title = cmds.text(l='>')
    one_col_form(list_sub_title_form, sub_title)

    list_form = cmds.formLayout(p=ofst_form)
    global source_list
    global target_list
    source_list = cmds.textScrollList(p=list_form, enableKeyboardFocus=False, allowMultiSelection=True, h=win_h-110)
    target_list = cmds.textScrollList(p=list_form, enableKeyboardFocus=False, allowMultiSelection=True, h=win_h-110)
    two_col_form(list_form, source_list, target_list)

    btns_row = cmds.rowColumnLayout(nc=5,cw=[(1,95),(2,25),(3,25),(4,25),(5,50)], cs=[(1,0),(2,4),(3,0),(4,0),(5,4)], p=ofst_form)
    cmds.button(l='All Transforms', c=match_transforms)
    cmds.button(l='T', c=partial(match_transforms, pos=True))
    cmds.button(l='R', c=partial(match_transforms, rot=True))
    cmds.button(l='S', c=partial(match_transforms, scl=True))
    cmds.button(l='Pivots', c=partial(match_transforms, piv=True))

    footer_form = cmds.formLayout(p=ofst_form)
    parent_btn = cmds.button(l='Parent', c=parent_objs)
    one_col_form(footer_form, parent_btn)

    cmds.formLayout(ofst_form, e=True, 
                    af=[(list_title_form,'top',0),
                        (list_title_form,'left',0),
                        (list_title_form,'right',0),
                        (list_sub_title_form,'left',0),
                        (list_sub_title_form,'right',0),
                        (footer_form,'left',0),
                        (footer_form,'right',0),
                        (list_form,'left',0),
                        (list_form,'right',0)
                    ],
                    ac=[(list_form,'top',4,list_title_form), (btns_row,'top',12,list_form), (footer_form,'top',4,btns_row)])

    update_sel_callback()


def one_col_form(form, col):
    cmds.formLayout(form, e=True, af=[(col,'left',0), (col,'right',0)])

def two_col_form(form, l_col, r_col):
    cmds.formLayout(form, e=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[ (l_col,'right',0,49), (r_col,'left',0,51)])

def three_col_form(form, l_col, m_col, r_col):
    cmds.formLayout(form, edit=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,33), (m_col,'left',0,34), (m_col,'right',0,66), (r_col,'left',0,67)])


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


def match_transforms(*args, **kwargs):
    if len(source_sel) != len(target_sel):
        print("Not equal selection of items")
        return

    source_list_items = cmds.textScrollList(source_list, q=True, ai=True)
    target_list_items = cmds.textScrollList(target_list, q=True, ai=True)
    for i in source_list_items:
        cmds.matchTransform(i, target_list_items[source_list_items.index(i)], **kwargs)

    # for i in source_sel:
    #     cmds.matchTransform(i, target_sel[source_sel.index(i)], **kwargs)

def parent_objs(*args):
    if len(source_sel) != len(target_sel):
        print("Not equal selection of items")
        return

    source_list_items = cmds.textScrollList(source_list, q=True, ai=True)
    target_list_items = cmds.textScrollList(target_list, q=True, ai=True)
    for i in source_list_items:
        cmds.parent(i, target_list_items[source_list_items.index(i)])
    # for i in source_sel:
    #     cmds.parent(i, target_sel[source_sel.index(i)])


def create_sel_callback():
    global callback_id
    callback_id = om.MEventMessage.addEventCallback('SelectionChanged', update_sel_callback)


def update_sel_callback(*args):
    cmds.textScrollList(source_list, e=True, ra=True)
    cmds.textScrollList(target_list, e=True, ra=True)
    sel = cmds.ls(sl=True)
    if sel:
        half_sel_len = int(len(sel)/2)
        # print(sel[0])
        global source_sel, target_sel
        source_sel = sel[:half_sel_len]
        target_sel = sel[half_sel_len:]
        cmds.textScrollList(source_list, e=True, a=source_sel)
        cmds.textScrollList(target_list, e=True, a=target_sel)
        # if len(source_sel) != len(target_sel):
        #     cmds.textScrollList(source_list, e=True, a=source_sel)
        # else:
        #     cmds.textScrollList(source_list, e=True, a=source_sel)
        #     cmds.textScrollList(target_list, e=True, a=target_sel)
    

def cleanup_callback():
    global callback_id
    if callback_id:
        om.MMessage.removeCallback(callback_id)
        callback_id = None


# main()