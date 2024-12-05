import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)

    if not sel:
        print("No objects selected")
        return

    grp_list = []
    current_parent = cmds.listRelatives(sel[0], p=True)

    for i in sel:
        grp_name = cmds.group(empty=True, n=f"{i}_Ofst")
        sel_matrix = cmds.xform(i, q=True, matrix=True)

        # set the tranformation no matter the obj has offset poivot 
        cmds.xform(grp_name, matrix=sel_matrix)

        cmds.matchTransform(grp_name, i, pivots=True)

        cmds.parent(i, grp_name)
        grp_list.append(grp_name)
        # if there's ascending hierarchy level later, the attr shouldn't be locked yet
        # for attr in ["translate", "rotate", "scale", "visibility"]:
        #     cmds.setAttr(f"{grp_name}.{attr}", lock=1)


    if current_parent:
        cmds.parent(grp_list, current_parent)

    elif not current_parent and len(sel) == 1:
        return

    elif not current_parent and len(sel) > 1:
        current_parent = cmds.group(empty=True, n=f"{sel[0]}_to_{sel[-1]}_Ofst_Grp")
        cmds.parent(grp_list, current_parent)

# main()