import maya.cmds as cmds

def main():
    global sel, all_jnts, arm_jnts
    sel = cmds.ls(sl=True)
    all_jnts = cmds.ls(dag=True, type='joint')
    arm_jnts = cmds.listRelatives(sel, ad=True)
    arm_jnts.insert(0, sel[0])
    arm_jnts = [i for i in all_jnts if i in arm_jnts]

    rename_finger_jnts()
    rename_arm_jnts()

def rename_arm_jnts():
    arm_main_jnts = arm_jnts[:4]
    arm_main_jnt_names = ('shoulder', 'elbow', 'radius', 'wrist')
    for j,n in zip(arm_main_jnts, arm_main_jnt_names):
        cmds.rename(j, f'L_{n}')


def rename_finger_jnts():
    init_finger_jnts = cmds.listRelatives(arm_jnts[3]) # index 3 is the wrist
    init_finger_jnts_pos = {}

    for i in init_finger_jnts:
        init_finger_jnts_pos[i] = cmds.getAttr(f'{i}.translateZ')

    sorted_init_finger_jnts = dict(sorted(init_finger_jnts_pos.items(), key=lambda x: x[1], reverse=True)) # sort the list of tuples (which is dict.items()) by the value (jnt position value, which is jnt[1] in the dict)

    finger_jnt_names = ('thumb', 'index', 'middle', 'ring', 'pinky')
    finger_jnt_name_lists = [format_finger_jnt_names(i) for i in finger_jnt_names]
    
    print(sorted_init_finger_jnts)
    for i in list(sorted_init_finger_jnts):
        finger_jnts = get_whole_finger_jnts(i) # get whole unnamed joints
        jnt_name_list_index = list(sorted_init_finger_jnts).index(i)

        for j in finger_jnts:
            cmds.rename(j, finger_jnt_name_lists[jnt_name_list_index][finger_jnts.index(j)])


def get_whole_finger_jnts(init_jnt):
    finger_jnts = cmds.listRelatives(init_jnt, ad=True)
    finger_jnts = [i for i in all_jnts if i in finger_jnts]
    finger_jnts.reverse() # to suit for both meta or non-meta finger rigging, if it's a non-meta finger which means it has one less joint, then the last item in the name list will be ignored as it's out of match field
    finger_jnts.append(init_jnt)
    return finger_jnts


def format_finger_jnt_names(name):
    if name == 'Thumb':
        name_list = (f'l_{name}_end', f'l_{name}_2', f'l_{name}_1', f'l_{name}_meta')
    else:
        name_list = (f'l_{name}_end', f'l_{name}_3', f'l_{name}_2', f'l_{name}_1', f'l_{name}_meta')
    return name_list

# main()