import sys
import maya.cmds as cmds
import maya.api.OpenMaya as om

def main():
    initialize_module()
    create_ui()
    callback()


def initialize_module():
    global root_set, new_set, set_sel, previous_member_sel, common_title
    root_set = 'selectionSet'
    new_set = ''
    set_sel = []
    previous_member_sel = []
    common_title = '----- COMMON -----'

    if root_set in cmds.ls(sets=True):
        print(f"{root_set} found")
    else:
        cmds.sets(n=root_set, empty=True)


def reload_script():
    module_name = 'SetSelector'
    if module_name in sys.modules:
        import importlib
        importlib.reload(sys.modules[module_name])

# ---------------- UI ----------------

def create_ui():
    global win
    win = 'setSelector'

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    global win_w
    global win_h
    win_w = 300
    win_h = 220
    cmds.window(win, t='Set Selector', mxb=False, mnb=False, wh=(win_w,win_h), s=False, closeCommand=remove_callbacks)
    cmds.showWindow(win)

    global base_form
    global ofst_form
    base_form = cmds.formLayout(p=win)
    ofst_form = cmds.formLayout(p=base_form)
    cmds.formLayout(base_form, e=True, af=[(ofst_form,'top',10), (ofst_form,'bottom',10), (ofst_form,'left',10), (ofst_form,'right',10)])

    pane_layout = cmds.paneLayout(cn='vertical2', st=4, enableKeyboardFocus=False, p=ofst_form) # 115

    global set_list
    global member_list
    set_list = cmds.textScrollList(allowMultiSelection=True, enableKeyboardFocus=False, selectCommand=on_set_select, doubleClickCommand=on_double_click, p=pane_layout)
    member_list = cmds.textScrollList(allowMultiSelection=True, enableKeyboardFocus=False, selectCommand=on_member_select, doubleClickCommand=on_double_click, p=pane_layout)


    btn_bg_form = cmds.formLayout(p=ofst_form)
    l_bg = cmds.rowColumnLayout(h=55, bgc=(0.24,0.24,0.24), p=btn_bg_form)
    r_bg = cmds.rowColumnLayout(h=55, bgc=(0.24,0.24,0.24), p=btn_bg_form)
    two_col_form(btn_bg_form, l_bg, r_bg)

    btn_title_form = cmds.formLayout(p=ofst_form)
    l_title = cmds.text(l='Set')
    r_title = cmds.text(l='Member')
    two_col_form(btn_title_form, l_title, r_title)

    btn_form = cmds.formLayout(p=ofst_form)

    set_form = cmds.formLayout(p=btn_form)
    create_btn = cmds.button(l='Create', command=handle_create_sets)
    delete_btn = cmds.button(l='Delete', command=handle_delete_sets)
    two_col_form(set_form, create_btn, delete_btn)

    # member_row = cmds.rowColumnLayout(nc=2, cw=[(1,btn_w),(2,btn_w)], cs=[(1,5),(2,6)], p=btns)
    member_form = cmds.formLayout(p=btn_form)
    add_btn = cmds.button(l='Add', command=handle_add_members)
    remove_btn = cmds.button(l='Remove', command=handle_remove_members)
    two_col_form(member_form, add_btn, remove_btn)

    cmds.formLayout(btn_form, e=True, 
                    ap=[(set_form,'left',0,2),
                        (set_form,'right',0,47),
                        (member_form,'left',0,53),
                        (member_form,'right',0,98)
                    ])

    cmds.formLayout(ofst_form, e=True, 
                    af=[(pane_layout,'left',0), 
                        (pane_layout,'right',0),
                        (pane_layout,'top',0),
                        (pane_layout,'bottom',60),
                        (btn_bg_form,'left',0),
                        (btn_bg_form,'right',0),
                        (btn_title_form,'left',0),
                        (btn_title_form,'right',0),
                        (btn_form,'left',0),
                        (btn_form,'right',0),
                        (btn_bg_form,'bottom',0),
                        (btn_title_form,'bottom',35),
                        (btn_form,'bottom',5),
                    ])

    # cmds.dockControl(l='Set Selector', area='right', content=win, allowedArea='all', splitLayout='vertical')

    update_set_items()

def two_col_form(form, l_col, r_col):
    cmds.formLayout(form, e=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,49), (r_col,'left',0,51)])

# ---------------- textScrollList events ----------------

def append_items(name, items, **kwargs):
    cmds.textScrollList(name, e=True, append=items, **kwargs)

def select_items(name, items, **kwargs):
    cmds.textScrollList(name, e=True, selectItem=items, **kwargs)

def remove_all_items(name):
    cmds.textScrollList(name, e=True, removeAll=True)


def update_all_sets():
    global all_sets
    all_sets = cmds.ls(sets=True)


def update_set_sel():
    global set_sel
    set_sel = cmds.textScrollList(set_list, q=True, selectItem=True)


def update_member_sel():
    global member_sel
    if set_sel:
        member_sel = cmds.textScrollList(member_list, q=True, selectItem=True)


# Update the set list when sets are created or deleted
def update_set_items(*args):
    update_all_sets()
    remove_all_items(set_list)

    if root_set in all_sets:
        sub_sets = cmds.sets(root_set, q=True)
        if sub_sets:
            ex_sub_sets = set(sub_sets) & set(all_sets)
        # print('selectionSet Found')
            if ex_sub_sets:
                # remove_all_items(set_list)
                append_items(set_list, sorted(ex_sub_sets))
                # append the display type sets

# Update the member list when objs are created or deleted
def update_member_items(*args):
    update_set_sel()
    remove_all_items(member_list)

    if set_sel:
        members = cmds.sets(set_sel, q=True)

        if members:
            # Order the members as how it is shown in the outliner
            global all_dag_objs, ordered_members
            all_dag_objs = cmds.ls(dag=True)
            ordered_members = [i for i in all_dag_objs if i in members]

            # Order members which are not dag objs, e.g., curve points
            ordered_members += [i for i in members if i not in ordered_members]

            append_items(member_list, ordered_members)

            if len(set_sel) > 1:
                common_items = cmds.sets(set_sel, intersection=set_sel[0])
                # append_items(member_list, ordered_members) 

                if common_items:
                    # common_items = sorted(set(common_items))
                    append_items(member_list, common_title)
                    cmds.textScrollList(member_list, e=True, enableItem=(common_title,False))

                    ordered_common_items = [i for i in all_dag_objs if i in common_items]
                    cmds.textScrollList(member_list, e=True, removeItem=ordered_common_items)
                    append_items(member_list, ordered_common_items)



# mainly for maintaining or recovering the selection
def select_previous_set_items():
    if new_set in all_sets:
        cmds.textScrollList(set_list, e=True, deselectAll=True)
        select_items(set_list, new_set)
    elif set_sel:
        ex_set_sel = set(set_sel) & set(all_sets)
        cmds.textScrollList(set_list, e=True, deselectAll=True)
        select_items(set_list, ex_set_sel)
    else: 
        return
    

# Apply the set selection to the scene, and show the members in the right pane
def on_set_select(*args):
    global set_selected_bool, member_selected_bool
    set_selected_bool = True
    member_selected_bool = False

    update_set_sel()
    update_member_items()

    members = cmds.textScrollList(member_list, q=True, ai=True)
    if members:
        if common_title in members:
            members.remove(common_title)
        # when the sets have members, activate the selection
        cmds.select(members, replace=True)
        # cmds.select(set_sel, replace=True) # this actually selects all members of the set, to select the set, use noExpand flag

    global previous_member_sel
    previous_member_sel = []

# Apply the member selection to the scene
def on_member_select(*args):
    global set_selected_bool, member_selected_bool
    set_selected_bool = False
    member_selected_bool = True

    update_member_sel()

    global member_sel, previous_member_sel

    if member_sel:
        # Extend the list by the order of selection instead of the order of them in member list which is the same as the dag objects order
        if previous_member_sel:
            member_sel = [i for i in previous_member_sel if i in member_sel] + [i for i in member_sel if i not in previous_member_sel]

        cmds.select(member_sel, replace=True)
        previous_member_sel = member_sel

        print('select ' + ', '.join(member_sel))


# Rename the item
def on_double_click():
    if member_selected_bool:
        current_name = cmds.ls(member_sel, sn=True)[0]
    elif set_selected_bool:
        current_name = cmds.ls(set_sel, sn=True)[0]

    result = cmds.promptDialog(
        title='Rename',
        text=f"{current_name}",
        message='Enter Name:',
        button={'OK','Cancel'},
        cancelButton='Cancel',
        dismissString='Cancel',
        defaultButton='OK'
    )

    if result == 'OK':
        text = cmds.promptDialog(q=True, text=True)

        update_set_sel()        
        update_member_sel()

        if text:
            if member_selected_bool:
                new_name = cmds.rename(member_sel, text)
                update_member_items()
                select_items(member_list, new_name)
                update_member_sel()

            elif set_selected_bool:
                new_name = cmds.rename(set_sel, text)
                update_set_items()
                select_items(set_list, new_name)
                update_set_sel()

            else:
                print('No objects found')


# ---------------- button events ----------------

def handle_create_sets(*args):
    update_all_sets()

    set_items = cmds.textScrollList(set_list, q=True, allItems=True)

    global new_set

    if root_set not in all_sets:
        new_set = cmds.sets(n='set1', empty=True)
        cmds.sets(n=root_set, empty=True)
        cmds.sets('set1', e=True, forceElement=root_set)

    elif set_items is None:
        new_set = cmds.sets(n='set1', empty=True)
        cmds.sets('set1', e=True, forceElement=root_set)

    else:
        set_item_count = len(set_items)
        new_set_name = f"set{set_item_count+1}"
        new_set = cmds.sets(n=new_set_name, empty=True)
        cmds.sets(new_set, e=True, forceElement=root_set)

    update_set_items()
    update_member_items()


def handle_delete_sets(*args):
    if set_sel:
        cmds.delete(set_sel)

    update_set_items() 
    update_member_items()


def handle_add_members(*args):
    sel = cmds.ls(sl=True)

    if sel and set_sel:
        for i in set_sel:
            cmds.sets(sel, add=i)

        update_member_items()
        select_items(member_list, sel)
        update_member_sel()


def handle_remove_members(*args):
    sel = cmds.ls(sl=True)

    if sel and set_sel:
        for i in set_sel:
            cmds.sets(sel, remove=i)

        update_member_items()

# ---------------- callback ----------------

def callback():
    global callback_ids 
    callback_ids = []
    callback_ids.append(om.MSceneMessage.addCallback(om.MSceneMessage.kAfterNew, on_scene_event))
    callback_ids.append(om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, on_scene_event))

    callback_ids.append(om.MDGMessage.addNodeAddedCallback(added_callback, 'dependNode'))
    callback_ids.append(om.MDGMessage.addNodeRemovedCallback(removed_callback, 'dependNode'))
    callback_ids.append(om.MEventMessage.addEventCallback('Undo', undo_callback))
    callback_ids.append(om.MEventMessage.addEventCallback('Redo', redo_callback))

    global abort_added_callback, abort_removed_callback
    abort_added_callback = False
    abort_removed_callback = False


def on_scene_event(msg, *args):
    if msg in (om.MSceneMessage.kAfterNew, om.MSceneMessage.kAfterOpen):
        reload_script()


def added_callback(node, clientData):
    global abort_added_callback

    if abort_added_callback:
        return

    abort_added_callback = True

    def deferred_callback():
        global abort_added_callback
        print('callback of added')
        update_set_items() 
        # update_set_sel()
        select_previous_set_items()
        update_member_items()
        abort_added_callback = False

    cmds.evalDeferred(deferred_callback, lowestPriority=True)


def removed_callback(node, clientData):
    global abort_removed_callback

    if abort_removed_callback:
        return
    
    abort_removed_callback = True

    def deferred_callback():
        global abort_removed_callback
        print('callback of removed')
        update_set_items()
        # update_set_sel()
        select_previous_set_items()
        update_member_items()
        abort_removed_callback = False

    cmds.evalDeferred(deferred_callback, lowestPriority=True)


def undo_callback(clientData):
    global abort_added_callback, abort_removed_callback

    if abort_added_callback or abort_removed_callback:
        return
    abort_added_callback, abort_removed_callback = True, True

    def undo_callback_deferred():
        print('callback of undo')
        update_set_items()
        # update_set_sel()
        select_previous_set_items()
        update_member_items()

        global abort_added_callback, abort_removed_callback
        abort_added_callback, abort_removed_callback = False, False

    cmds.evalDeferred(undo_callback_deferred, lowestPriority=True)


def redo_callback(clientData):

    global abort_added_callback, abort_removed_callback

    if abort_added_callback or abort_removed_callback:
        return
    abort_added_callback, abort_removed_callback = True, True

    def redo_callback_deferred():
        print('callback of redo')
        update_set_items()
        # update_set_sel()
        select_previous_set_items()
        update_member_items()

        global abort_added_callback, abort_removed_callback
        abort_added_callback, abort_removed_callback = False, False

    cmds.evalDeferred(redo_callback_deferred, lowestPriority=True)


def remove_callbacks(*args):
    om.MMessage.removeCallbacks(callback_ids)
    callback_ids.clear()


# main()