import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)
    for i in sel:
        cmds.joint(i, e=True, zeroScaleOrient=True)
    
