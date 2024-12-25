import maya.cmds as cmds
sel = cmds.ls(sl=True)

if len(sel) <= 2:
    for i in sel:
        # at:attributeType, en:enumName, dv:defaultValue, h:hidden
        attr_category = 'MOVEMENT'
        attr_dict = {1:'Toe_Twist', 2:'Heel_Twist', 3:'Bank', 4:'Toe_Tap', 5:'Roll'}

        cmds.addAttr(ln=attr_category, at='enum', en='----------', k=True)
        # l:lock, cb:channelBox, k=keyable
        cmds.setAttr(f'{i}.{attr_category}', l=True, cb=True, k=False)

        for i in dict:
            cmds.addAttr(ln=attr_dict[i], at='double', min=-10, max=10, dv=0, k=True) 