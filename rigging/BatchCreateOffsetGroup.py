import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)

    if not sel:
        print("No objects selected")
        return

    grp_list = []
    # current_parent = cmds.listRelatives(sel[0], p=True)

    for i in sel:
        sel_parent = cmds.listRelatives(i, p=True)
        if sel_parent:
            cmds.parent(i, world=True)

        sel_matrix = cmds.xform(i, q=True, matrix=True)

        grp = cmds.group(empty=True, n=f"{i}_ofst")
        # set the tranformation no matter the obj has offset poivot 
        cmds.xform(grp, matrix=sel_matrix)
        cmds.matchTransform(grp, i, pivots=True)

        cmds.parent(i, grp)

        if sel_parent:
            cmds.parent(grp, sel_parent)
        else:
            grp_list.append(grp)

        # if there's ascending hierarchy later, the attr shouldn't be locked yet
        # for attr in ["translate", "rotate", "scale", "visibility"]:
        #     cmds.setAttr(f"{grp}.{attr}", lock=1)


    # if current_parent:
    #     cmds.parent(grp_list, current_parent)

    if len(sel) == 1:
        return

    elif grp_list and len(sel) > 1:
        current_parent = cmds.group(empty=True, n=f"{sel[0]}_to_{sel[-1]}_ofst_grp")
        cmds.parent(grp_list, current_parent)

# main()