import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True, dag=True)
    if not sel:
        print("No objects selected")
    all_shapes = cmds.ls(shapes=True)
    sel = [i for i in sel if i not in all_shapes]
    for i in sel:
        for attr in ['translate', 'rotate', 'scale']:
            for axis in ['X', 'Y', 'Z']:
                full_attr = f"{i}.{attr}{axis}"
                if cmds.getAttr(full_attr, channelBox=False):
                    cmds.setAttr(full_attr, channelBox=True)
                if cmds.getAttr(full_attr, lock=True):
                    cmds.setAttr(full_attr, lock=False)
                if cmds.getAttr(full_attr, keyable=False):
                    cmds.setAttr(full_attr, keyable=True)
                    
# main()