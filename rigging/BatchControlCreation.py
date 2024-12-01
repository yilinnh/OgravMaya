import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)

    if not sel: 
        print("No objects selected")
        return

    ctrl_list = []

    for jnt in sel:
        ctrl = cmds.circle( nr=(1,0,0), c=(0,0,0), n=f"{jnt}_Ctrl")[0]
        cmds.matchTransform(ctrl, jnt)
        ctrl_list.append(ctrl)

    cmds.select(ctrl_list)
    # first_jnt = sel[0]
    # cmds.sets(ctrl_list, n=f"{first_jnt}_to_{jnt}_Set")
