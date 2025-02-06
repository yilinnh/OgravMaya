import maya.cmds as cmds

def main():
    rotate_order = 'zxy'

    sel = cmds.ls(sl=True)
    rotate_order_dict = {'xyz':0, 'yzx':1, 'zxy':2, 'xzy':3, 'yxz':4, 'zyx':5}

    for i in sel:
        cmds.setAttr(f'{i}.rotateOrder', rotate_order_dict[rotate_order])
    
    cmds.inViewMessage(
        msg=f'Change rotate order to "{rotate_order}"',
        pos='topCenter',
        fade=True
    )