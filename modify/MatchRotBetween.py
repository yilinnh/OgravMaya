import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)
    if len(sel) < 3:
        print("Please select the target object first, then the reference objects")
        return
    
    reference = sel[-2:]
    target = sel[:-2]

    for i in target:
        constraint = cmds.orientConstraint(reference[0], reference[1], i)
        cmds.delete(constraint)