import maya.cmds as cmds


def main():
    sel = cmds.ls(sl=True)

    if sel:
        display_on_list = [i for i in sel if cmds.getAttr(f"{i}.displayLocalAxis") == 1]

        if display_on_list:
            for i in display_on_list:
                cmds.setAttr(f"{i}.displayLocalAxis", 0)
            return
        else:
            for i in sel:
                cmds.setAttr(f"{i}.displayLocalAxis", 1)

    else:
        all_objs = cmds.ls(dag=True, type='transform')
        display_on_list = [i for i in all_objs if cmds.getAttr(f"{i}.displayLocalAxis") == 1]

        if display_on_list:
            for i in display_on_list:
                cmds.setAttr(f"{i}.displayLocalAxis", 0)
            return
        else:
            all_jnts = cmds.ls(type='joint')
            for i in all_jnts:
                cmds.setAttr(f"{i}.displayLocalAxis", 1)

# main()