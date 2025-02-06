import maya.cmds as cmds

def main():
    create_ui()

def create_ui():
    global win, win_w, win_h
    win = 'attributeConnector'
    win_w = 300
    win_h = 370

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t='Attribute Connector', wh=(win_w,win_h), mxb=False, mnb=False, s=False)
    cmds.showWindow(win)

    global ofst_form
    base_form = cmds.formLayout()
    ofst_form = cmds.formLayout(p=base_form)

    cmds.formLayout(base_form, e=True, af=[(ofst_form,'top',10),(ofst_form,'right',10),(ofst_form,'bottom',10),(ofst_form,'left',10)])


    ### show srouce and target objs
    global pane, src_list, tgt_list, load_src_btn, load_tgt_btn, src_input, tgt_input
    obj_list_title = cmds.text(l='Objects:', p=ofst_form)
    attr_list_title = cmds.text(l='Attribute:', p=ofst_form)

    pane = cmds.paneLayout(cn='vertical2', p=ofst_form, st=4, enableKeyboardFocus=False)

    src_col = cmds.rowColumnLayout(p=pane, adj=True, rs=[(1,4)], ro=[(4,'top',40)], w=win_w/4)
    cmds.text(l='Source', p=src_col)
    src_list = cmds.textScrollList(enableKeyboardFocus=False, allowMultiSelection=True, sc=handle_src_sel, p=src_col, w=win_w/8)
    load_src_btn = cmds.button('loadSrcBtn', l='Load Source', c=handle_src_load)
    src_input = cmds.textField(aie=True, pht='srcAttr', enterCommand=handle_src_input,  textChangedCommand=handle_src_input)


    tgt_col = cmds.rowColumnLayout(p=pane, adj=True, rs=[(1,4)], ro=[(4,'top',40)], w=win_w/4)
    cmds.text(l='Target', p=tgt_col)
    tgt_list = cmds.textScrollList(enableKeyboardFocus=False, allowMultiSelection=True, sc=handle_tgt_sel,p=tgt_col, w=win_w/8)
    load_tgt_btn = cmds.button('loadTgtBtn', l='Load Target', c=handle_tgt_load)
    tgt_input = cmds.textField(aie=True, pht='tgtAttr', enterCommand=handle_tgt_input)


    ### footer buttons
    footer_hr = cmds.separator(st='in', p=ofst_form)
    footer_form = cmds.formLayout(p=ofst_form)
    apply_btn = cmds.button(l='Apply', c=handle_apply)
    close_btn = cmds.button(l='Close', c=handle_close)
    two_cols_form(footer_form, apply_btn, close_btn)

    ### rearrange forms
    cmds.formLayout(ofst_form, e=True, 
                    af=[
                        (obj_list_title,'top',0),
                        (pane,'left',0),
                        (pane,'right',0),
                        (footer_hr,'left',0),
                        (footer_hr,'right',0),
                        (footer_form,'left',0),
                        (footer_form,'right',0),
                        (footer_form,'bottom',0)
                    ],
                    ac=[
                        (pane,'top',5,obj_list_title),
                        (attr_list_title,'top',230, obj_list_title),
                        (footer_hr,'bottom',10,footer_form),
                    ])


def one_col_form(form, col):
    cmds.formLayout(form, e=True, af=[(col,'left',0), (col,'right',0)])


def two_cols_form(form, l_col, r_col):
    cmds.formLayout(form, e=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,49), (r_col,'left',0,51)])


def handle_src_sel(*args):
    selected_items = cmds.textScrollList(src_list, q=True, selectItem=True)
    select_list_item(src_list, selected_items)


def handle_tgt_sel(*args):
    selected_items = cmds.textScrollList(tgt_list, q=True, selectItem=True)
    select_list_item(tgt_list, selected_items)


def select_list_item(list, selected_items):
    # all_objs = cmds.ls(dag=True)
    # exist_sel = list(set(selected_items) & set(all_objs))
    # if not exist_sel:
    #     cmds.textScrollList(list, e=True, deselectAll=True)
    #     return
    # cmds.select(exist_sel)
    cmds.select(selected_items)


def handle_src_load(*args):
    global all_src
    sel = cmds.ls(sl=True)
    cmds.textScrollList(src_list, e=True, ra=True)
    cmds.textScrollList(src_list, e=True, append=sel)
    all_src = cmds.textScrollList(src_list, q=True, ai=True)

def handle_tgt_load(*args):
    global all_tgt
    sel = cmds.ls(sl=True)
    cmds.textScrollList(tgt_list, e=True, ra=True)
    cmds.textScrollList(tgt_list, e=True, append=sel)
    all_tgt = cmds.textScrollList(tgt_list, q=True, ai=True)


def handle_src_input(*args):
    src_attr = cmds.textField(src_input, q=True, text=True)
    if src_attr in ['translate', 'rotate', 'scale']:
        cmds.textField(tgt_input, e=True, text=src_attr)


def handle_tgt_input(*args):
    pass
    # global tgt_attr
    # tgt_attr = cmds.textField(tgt_input, q=True, text=True)

def handle_apply(*args):
    global src_attr, tgt_attr
    src_attr = cmds.textField(src_input, q=True, text=True)
    tgt_attr = cmds.textField(tgt_input, q=True, text=True)

    if len(all_src) == len(all_tgt):
        for s,t in zip(all_src, all_tgt):
            cmds.connectAttr(f'{s}.{src_attr}', f'{t}.{tgt_attr}')
    elif len(all_src) == 1:
        for t in all_tgt:
            cmds.connectAttr(f'{all_src[0]}.{src_attr}', f'{t}.{tgt_attr}')

    # for s in all_src:
    #     for t in all_tgt:
    #         cmds.connectAttr(f'{s}.{src_attr}', f'{t}.{tgt_attr}')
    
def handle_close(*args):
    cmds.deleteUI(win)

# main()