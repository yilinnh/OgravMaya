import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)

    for i in sel:
        cmds.addAttr(ln='newAttr', proxy='root_ctrl.testAttr')

