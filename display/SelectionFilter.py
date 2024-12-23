import maya.cmds as cmds

class CheckBox:
    def __init__(self, short_name, label):
        # if not label:
        #     label = short_name
        self.type = short_name
        cmds.checkBox(short_name, l=label, value=False, onCommand=self.on_command, offCommand=self.off_command)

    def on_command(self, *args):
        checked_types.append(self.type)

    def off_command(self, *args):
        checked_types.remove(self.type)

def main():
    global window
    global checked_types
    window = 'SelectionFilter'
    checked_types = []

    if cmds.window(window, ex=True):
        cmds.deleteUI(window)

    cmds.window(window, t='Selection Filter', wh=(210,170), mnb=False, mxb=False, s=False)
    cmds.showWindow(window)

    # cmds.rowColumnLayout(adj=True)
    base_form = cmds.formLayout()
    ofst_form = cmds.formLayout(nd=100)
    cmds.formLayout(base_form, e=True, af=[(ofst_form,'top',10), (ofst_form,'right',10), (ofst_form,'bottom',10), (ofst_form,'left',10)])

    # header_row = cmds.rowColumnLayout(p=ofst_form)
    header_text = cmds.text(l='Choose filter types:', p=ofst_form)
    content_grid = cmds.gridLayout(nc=2, cw=90, ch=20, p=ofst_form)
    CheckBox('transform', 'Transform')
    CheckBox('shape', "Shape")
    CheckBox('mesh', 'Mesh')
    CheckBox('nurbsCurve', 'Curve')
    CheckBox('joint', 'Joint')
    CheckBox('constraint', 'Constraint')
    CheckBox('clusterHandle', 'Cluster')

    # footer_form = cmds.rowColumnLayout(nc=2, cs=[(1,0),(2,10)], cw=[(1,85),(2,85)], p=ofst_form)
    footer_form = cmds.formLayout(p=ofst_form)
    apply_btn = cmds.button(l='Apply', command=on_apply, p=footer_form)
    close_btn = cmds.button(l='Close', command=close_window, p=footer_form)
    two_col_form(footer_form, apply_btn, close_btn)


    cmds.formLayout(ofst_form, edit=True, 
                    af=[(header_text,'left',4), (content_grid,'left',8), (footer_form,'bottom',0), (footer_form,'left',0), (footer_form,'right',0)],
                    ac=[(content_grid,'top',8,header_text)])


def two_col_form(form, l_col, r_col):
    cmds.formLayout(form, e=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[ (l_col,'right',0,49), (r_col,'left',0,51)])


def on_apply(*args):
    # Get the current selection, including all objects in folded groups
    objs = cmds.ls(sl=True)

    if not objs: 
        objs = cmds.ls(dag=True)

    global checked_types

    filtered_sel = []
    nested_node_types = ['nurbsCurve', 'clusterHandle']
    checked_nested_node_types = set(nested_node_types) & set(checked_types)
    
    if checked_nested_node_types:
        for t in checked_nested_node_types:
            # List selectoin from both viewport and outliner
            transform_sel = cmds.ls(objs, type='transform')

            if transform_sel:
                # for i in transform_sel:
                #     if cmds.listRelatives(i, c=True, type=checked_nested_node_types):
                #         filtered_sel.append(i)

                # Find the transform node instead of the shape node
                filtered_sel = [i for i in transform_sel if cmds.listRelatives(i, c=True, type=t)]

        # general_checked_types = [i for i in checked_types if i not in checked_nested_node_types]
        for i in checked_nested_node_types:
            general_checked_types = checked_types.remove(i)

        if general_checked_types:
            filtered_sel += cmds.ls(objs, type=general_checked_types)
        
    else:
        filtered_sel = cmds.ls(objs, type=checked_types)
        
    # Update selection with filtered results
    cmds.select(set(filtered_sel), replace=True)

def close_window(*args):
    cmds.deleteUI('SelectionFilter')
    checked_types.clear()

# main()