import maya.cmds as cmds


def main():
    sel = cmds.ls(sl=True)
    for i in sel:
        bake_to_offset_parent_matrix(i)


def bake_to_offset_parent_matrix(obj):
    if not cmds.objExists(obj):
        raise ValueError(f"Object '{obj}' does not exist.")

    # Get the object's current world matrix
    world_matrix = cmds.xform(obj, q=True, matrix=True, ws=True)
    print(world_matrix)
    # Apply the current world matrix to the offsetParentMatrix
    cmds.setAttr(f"{obj}.offsetParentMatrix", world_matrix, type="matrix")

    # Reset local transformations
    cmds.setAttr(f"{obj}.translate", 0, 0, 0)
    cmds.setAttr(f"{obj}.rotate", 0, 0, 0)
    cmds.setAttr(f"{obj}.scale", 1, 1, 1)

# Example usage:
# Assuming you've updated the transformations of "pCube1" and want it to stay in place
