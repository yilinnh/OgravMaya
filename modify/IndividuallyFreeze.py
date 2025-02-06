import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)
    for i in sel:
        children = cmds.listRelatives(i, c=True)
        if children:
            cmds.parent(children, world=True)
            cmds.makeIdentity(i, apply=True)
            cmds.parent(children, i)
        else:
            cmds.makeIdentity(i, apply=True)
        
    cmds.select(sel)