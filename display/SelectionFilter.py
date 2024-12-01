import maya.cmds as cmds

class CheckBox:
    def __init__(self, short_name, label=""):
        if not label:
            label = short_name
        self.type = short_name
        cmds.checkBox(short_name, l=label.capitalize(), value=False, onCommand=self.on_command, offCommand=self.off_command)

    def on_command(self, *args):
        checked_types.append(self.type)

    def off_command(self, *args):
        checked_types.remove(self.type)

def main():
    global window
    global checked_types
    window = "SelectionFilter"
    checked_types = []

    if cmds.window(window, ex=True):
        cmds.deleteUI(window)

    cmds.window(window, t="Selection Filter", mnb=0, mxb=0, s=0, wh=(203,170))
    cmds.showWindow(window)

    # cmds.rowColumnLayout(adj=True)
    base_form = cmds.formLayout()
    main_form = cmds.formLayout(nd=100)
    cmds.formLayout(base_form, e=True, af=[(main_form,'top',10), (main_form,'right',10), (main_form,'bottom',10), (main_form,'left',10)])

    # header_row = cmds.rowColumnLayout(p=main_form)
    header_text = cmds.text(l="Choose filter types:", p=main_form)
    content_grid = cmds.gridLayout(nc=2, cw=90, ch=20, p=main_form)
    CheckBox("transform")
    CheckBox("shape")
    CheckBox("mesh")
    CheckBox("nurbsCurve", "NURBS Curve")
    CheckBox("clusterHandle", "cluster")
    CheckBox("joint")
    CheckBox("constraint")

    footer_row = cmds.rowColumnLayout(nc=2, cs=[(1,0),(2,10)], cw=[(1,85),(2,85)], p=main_form)
    cmds.button(l="Apply", command=on_apply, p=footer_row)
    cmds.button(l="Close", command=close_window, p=footer_row)

    cmds.formLayout(main_form, edit=True, 
                    af=[(content_grid,'left',4), (footer_row,'bottom',0)],
                    ac=[(content_grid,'top',8,header_text)])


def on_apply(*args):
    # Get the current selection, including all objects in folded groups
    sel = cmds.ls(sl=True)

    if not sel: 
        print("No objects selected")
        return

    global checked_types

    filtered_sel = []
    nested_node = ["nurbsCurve", "clusterHandle"]
    checked_nested_nodes = set(nested_node) & set(checked_types)
    
    if checked_nested_nodes:
        # list selectoin from both viewport and outliner
        transform_sel = cmds.ls(sel, type="transform")

        if transform_sel:
            for i in transform_sel:
                if cmds.listRelatives(i, c=True, type=checked_nested_nodes):
                    filtered_sel.append(i)

        general_checked_types = [i for i in set(checked_types) if i not in set(checked_nested_nodes)]

        if general_checked_types:
            filtered_sel += cmds.ls(sel, type=general_checked_types)
        
    else:
        filtered_sel = cmds.ls(sel, type=checked_types)
        
    # Update selection with filtered results
    cmds.select(set(filtered_sel), replace=True)

def close_window(*args):
    cmds.deleteUI("SelectionFilter")
    checked_types.clear()

# main()