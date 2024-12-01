import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)

    if not sel:
        print("No objects selected")
        return

    for i in sel:
        cmds.setAttr(f"{i}.rotate", 0, 0, 0)