import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)
    if not sel:
        print("No objects seleted")
        return
    
    for i in sel:
        cmds.joint(i, e=True, zeroScaleOrient=True)

    cmds.inViewMessage(
        msg=f"Reoriented translation axis",
        pos='topCenter',
        fade=True
    )

# main()