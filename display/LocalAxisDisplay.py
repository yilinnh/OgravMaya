import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)

    if sel:
        toggle_display_local_axis(sel)

    else:
        all_joints = cmds.ls(type="joint")
        toggle_display_local_axis(all_joints)



def toggle_display_local_axis(objs):
    all_objs = cmds.ls(dag=True)
    all_shapes = cmds.ls(shapes=True)
    all_objs = [i for i in all_objs if i not in all_shapes]
    display_on_list = []

    for i in all_objs:
        if cmds.getAttr(f"{i}.displayLocalAxis") == 1:
            display_on_list.append(i)
        
    if display_on_list:
        for i in display_on_list:
            cmds.setAttr(f"{i}.displayLocalAxis", 0)
        return
    
    for i in objs:
        cmds.setAttr(f"{i}.displayLocalAxis", 1)


# main()