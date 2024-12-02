# select the joints to start
import maya.cmds as cmds

def main():
    selection = cmds.ls(sl=True)

    if not selection:
        print("No objects selected")
        return

    first_jnt = selection[0]
    top_grp = cmds.group(em=True, n="Ctrls")
    current_parent = top_grp
    ctrl_list = []

    constraint_type = input()

    def CreateConstraint():
        if constraint_type is "o":
            cmds.orientConstraint(ctrl, jnt)
        elif constraint_type is "p":
            cmds.parentConstraint(ctrl, jnt)
        elif constraint_type is "n":
            return

    for jnt in selection:
        # create ctrls
        ctrl = cmds.circle( nr=(1,0,0), c=(0,0,0), n=f"{jnt}_Ctrl")[0] # this returned 2 names
        cmds.matchTransform(ctrl, jnt)
        # create constraints
        CreateConstraint()
        # create grps
        grp = cmds.group(em=True, n=f"{ctrl}_Ofst", p=current_parent)
        cmds.matchTransform(grp, ctrl)
        cmds.parent(ctrl, grp)

        for attr in ["translate", "rotate", "scale", "visibility"]:
            cmds.setAttr(f"{grp}.{attr}", lock=True)

        ctrl_list.append(ctrl)
        current_parent = ctrl

    cmds.rename(top_grp, f"{first_jnt}_to_{jnt}_{top_grp}")
    cmds.sets(ctrl_list, n=f"{first_jnt}_to_{jnt}_Set")
