import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)
    origin_grp = cmds.listRelatives(sel[0], p=True)

    if origin_grp:
        all_children = cmds.listRelatives(origin_grp, allDescendents=True)
        for i in sel:
            if i not in all_children:
                print(f"{i} is not in the same group as others")
                return
    # nodes are world direct descendents
    else:
        new_grp = cmds.group(n=f"{sel[0]} to {sel[-1]} Ofst_Grp", em=True)


    temp_grp = cmds.group(sel, n="temp")

    siblings = cmds.listRelatives(temp_grp, c=True)


    for i in range(len(siblings)-1):
        current_sibling = siblings[i]
        next_sibling = siblings[i+1]
        current_sibling_children = cmds.listRelatives(current_sibling, c=True)

        if not current_sibling_children:
            cmds.parent(next_sibling, current_sibling)
            
        elif cmds.objectType(current_sibling_children) == "nurbsCurve":
            cmds.parent(next_sibling, current_sibling)

        elif cmds.objectType(current_sibling_children) != "nurbsCurve":
            cmds.parent(next_sibling, current_sibling_children[0])
        
    if origin_grp:
        cmds.parent(sel[0], origin_grp) # parent the top node to maintain the hierarchy
    else:
        cmds.parent(sel[0], new_grp) 

    cmds.delete(temp_grp)

# main()
