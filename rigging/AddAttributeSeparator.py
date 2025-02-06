import maya.cmds as cmds

def main():
    attr_name = input().upper()
    sel = cmds.ls(sl=True)
    if sel and attr_name:
        for i in sel:
            cmds.addAttr(i, ln=attr_name, at='enum', en='----------:')
            cmds.setAttr(f'{i}.{attr_name}', e=True, channelBox=True)
            cmds.setAttr(f'{i}.{attr_name}', e=True, keyable=False)
            cmds.setAttr(f'{i}.{attr_name}', e=True, lock=True)
    else: 
        return

