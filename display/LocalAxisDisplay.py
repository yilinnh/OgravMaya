import maya.cmds as cmds

def main():
    selection = cmds.ls(sl=True)

    if not selection:
        print("No objects selected")
        return

    for i in selection:
        local_axis_display = cmds.getAttr(f"{i}.displayLocalAxis")

        if local_axis_display == 0:
            cmds.setAttr(f"{i}.displayLocalAxis", 1)
        elif local_axis_display == 1:
            cmds.setAttr(f"{i}.displayLocalAxis", 0)