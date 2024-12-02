import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)

    if sel:
        toggle_display_local_axis(sel)

    else:
        all_joints = cmds.ls(type="joint")
        toggle_display_local_axis(all_joints)



def toggle_display_local_axis(objs):

    for i in objs:
        local_axis_display = cmds.getAttr(f"{i}.displayLocalAxis")

        if local_axis_display == 0:
            continue

        elif local_axis_display == 1:
            for j in objs:
                cmds.setAttr(f"{j}.displayLocalAxis", 0)
            return
    
    for i in objs:
        cmds.setAttr(f"{i}.displayLocalAxis", 1)

    return


# main()