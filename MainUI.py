import re
import maya.cmds as cmds
import maya.api.OpenMaya as om
import importlib
from functools import partial

def main():
    create_ui()
    create_panels()
    create_selection_counter()
    arrange_layout()

class Layout:
    def __init__(self, type):
        self.type = type
    def create_column_layout(self, parent):
        self.column_path = cmds.columnLayout(rs=3, w=win_w-9,  adjustableColumn=True, p=parent)


class Script:
    def __init__(self, subfolder, script_name):
        main_folder = "OgravMaya"
        self.script_name = script_name
        self.module = importlib.import_module(f"{main_folder}.{subfolder}.{script_name}")

    def create_btn(self):
        cmds.button(label=nice_script_name(self.script_name), command=partial(self.run_script, self.script_name))

    def create_btn_with_submenu(self):
        cmds.button(label=f"  {nice_script_name(self.script_name)} >", command=partial(self.run_script, self.script_name))

    def run_script(self, *args):
        importlib.reload(self.module)
        self.module.main()


def nice_script_name(script_name):
    return re.sub(r"(?<!^)(?=[A-Z])", " ", script_name)


def create_ui():
    global win, win_w, win_h
    win = "OgravMayaTools"
    nice_win_name = f"{nice_script_name(win)}"
    win_w = 220
    # win_w = 300
    win_h = 300
    if cmds.window(win, exists=True):
        cmds.deleteUI(win)
    cmds.window(win, t=nice_script_name(win), wh=(win_w, win_h), sizeable=0, mnb=0, mxb=0, closeCommand=cleanup_callback, nestedDockingEnabled=True)
    cmds.showWindow(win)
    print(f"{nice_win_name} loaded")

    global base_form # contain the main_col and footer_col
    base_form = cmds.formLayout(p=win)

    global main_col_layout # contain the tabs
    main_col_layout = cmds.columnLayout(adj=True, p=base_form)

    global tabs # contain the offset form
    tabs = cmds.tabLayout(borderStyle="top", p=main_col_layout)

    global footer_col_layout # contain the footer (seletion counter)
    footer_col_layout = cmds.columnLayout(adj=True, p=base_form, w=win_w, bgc=(0.23,0.23,0.23))

    # cmds.dockControl(l='Grav Maya Tools', area='left', content=win, allowedArea='all', splitLayout='vertical')
  


def create_panels():
    def create_display_panel(type="display"):
        global f_ofst_form, f_scroll, f_col  
        f_ofst_form = cmds.formLayout(p=tabs)
        f_scroll = create_scroll_layout(f_ofst_form)
        f_col = Layout(type)
        f_col.create_column_layout(f_scroll)
        edit_ofst_form_layout(f_ofst_form, f_scroll)

        cmds.setParent(f_col.column_path)
        cmds.text(l="Select")
        Script(type, "SetSelector").create_btn_with_submenu()
        Script(type, "SelectionFilter").create_btn_with_submenu()
        Script(type, "SoftSelection").create_btn()

        cmds.text(l="Attribute")
        Script(type, "LocalAxisDisplay").create_btn()
        Script(type, "DisplayType").create_btn_with_submenu()
        Script(type, "OverrideColor").create_btn_with_submenu()
        Script(type, "CurveLineWidth").create_btn_with_submenu()


    def create_modify_panel(type="modify"):
        global s_ofst_form, s_scroll, s_col
        s_ofst_form = cmds.formLayout(p=tabs)
        s_scroll = create_scroll_layout(s_ofst_form)
        s_col = Layout(type)
        s_col.create_column_layout(s_scroll)
        edit_ofst_form_layout(s_ofst_form, s_scroll)

        cmds.setParent(s_col.column_path)
        cmds.text(l="Transform")
        Script(type, "ZeroRotation").create_btn()
        Script(type, "StepRotate").create_btn_with_submenu()
        Script(type, "BatchMatchTransform").create_btn_with_submenu()
        Script(type, "MatchToVertex").create_btn()

        cmds.text(l="Search")
        Script(type, "RegexMatch").create_btn_with_submenu()

        cmds.text(l="Hierarchy")
        Script(type, "AscendHierarchyLevel").create_btn()
        Script(type, "CombineShapes").create_btn()

        cmds.text(l="Misc")
        Script(type, "AutoTumblePivot").create_btn()
        Script(type, "CommandPort").create_btn()


    def create_rigging_panel(type="rigging"):
        global t_ofst_form, t_scroll, t_col
        t_ofst_form = cmds.formLayout(p=tabs)
        t_scroll = create_scroll_layout(t_ofst_form)
        t_col = Layout(type)
        t_col.create_column_layout(t_scroll)
        edit_ofst_form_layout(t_ofst_form, t_scroll)

        cmds.setParent(t_col.column_path)
        cmds.text(l="Skeleton")
        Script(type, "OrientEndJoints").create_btn()
        Script(type, "MatchTransToRotAxis").create_btn()
        Script(type, "RenameJoints").create_btn()

        cmds.text(l="Create")
        Script(type, "BatchCreateControl").create_btn()
        Script(type, "BatchCreateOffsetGroup").create_btn()
        Script(type, "BatchCreateConstriant").create_btn_with_submenu()
        Script(type, "BatchControlConstraintOffset").create_btn()

    create_display_panel()
    create_modify_panel()
    create_rigging_panel()

def create_scroll_layout(parent):
    return cmds.scrollLayout(w=win_w-2, h=win_h-36, p=parent, verticalScrollBarAlwaysVisible=True)

def edit_ofst_form_layout(form, scroll):
    cmds.formLayout(form, e=True, af=[(scroll,"top",0), (scroll,"left",0), (scroll,"right",-20)])

def create_selection_counter():
    cmds.text("selectionCountLabel", label="Selected Objects: 0", p=footer_col_layout)
    global callback_id
    callback_id = om.MEventMessage.addEventCallback("SelectionChanged", update_selection_count)

def update_selection_count(*args):
    selected_objects = cmds.ls(sl=True)
    sel_count = len(selected_objects)
    # Update the label with the number of selected objects
    cmds.text("selectionCountLabel", edit=True, label=f"Selected Objects: {sel_count}")

def cleanup_callback():
    global callback_id
    if callback_id:
        om.MMessage.removeCallback(callback_id)
        callback_id = None

def arrange_layout():
    cmds.tabLayout(tabs, edit=True, tabLabel=[(f_ofst_form, f_col.type.capitalize()), (s_ofst_form, s_col.type.capitalize()), (t_ofst_form, t_col.type.capitalize())])
    cmds.formLayout(base_form, edit=True, attachForm=[(main_col_layout,"top",0), (main_col_layout,"left",0), (main_col_layout,"right",0), (footer_col_layout,"bottom",0)], p=win)


main()
# if __name__ == "__main__":
#     main()
