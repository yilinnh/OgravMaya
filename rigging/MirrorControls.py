import maya.cmds as cmds

def mirror_controls():

    def replace_prefix(item):
        return item.replace('l_', 'r_', 1)

    print("\n--------------------------------------------------")
    print("# CONTROLS")
    print("--------------------------------------------------")

    mirror_axis = 'x'
    root_ctrl_grp_suffix = 'ctrl'

    ### Find the root ctrl grp
    all_objs = cmds.ls(dag=True, type='transform')
    ctrl_grps = [i for i in all_objs if i.startswith('l_') and root_ctrl_grp_suffix in i]
    root_ctrl_grp = [i for i in ctrl_grps if not cmds.listRelatives(i, p=True)[0].startswith('l_')][0]

    ### Get all ctrls and reorder them based on the dag hierarchy
    all_ctrl_descendants = cmds.listRelatives(root_ctrl_grp, ad=True, fullPath=True)

    # mirrored_ctrl_dict = {}
    # for i in all_ctrl_descendants:
    #     mirrored_ctrl_dict[i] = replace_prefix(i.split('|')[-1])

    mirrored_root_ctrl_name = replace_prefix(root_ctrl_grp)
    ### Assign value for the keys like: {'l_ctrl_grp|l_ctrls': 'r_ctrls'}
    mirrored_ctrl_dict = {i:replace_prefix(i.split('|')[-1]) for i in all_ctrl_descendants}
    ### Change from 'l_ctrl_grp|l_ctrls' to 'r_ctrl_grp|l_ctrls'
    mirrored_ctrl_dict = {i.replace(root_ctrl_grp, mirrored_root_ctrl_name, 1):mirrored_ctrl_dict[i] for i in mirrored_ctrl_dict}


    # all_ctrls.append(root_ctrl_grp)
    # print(all_ctrls)
    # all_ctrls = [i for i in all_objs if i in all_ctrls]
    # print(all_ctrls)

    ### Duplicate all ctrls
    ### Shouldn't use the built-in rename for duplicating it will increase the digital suffix
    mirrored_ctrls = cmds.duplicate(root_ctrl_grp, n=mirrored_root_ctrl_name)
    # mirrored_ctrls = [f'{mirrored_root_ctrl_name}|{i}' for i in mirrored_ctrls[1:]]
    for i in mirrored_ctrl_dict:
        cmds.rename(i, mirrored_ctrl_dict[i])

    ### Find and delete redundant descendants
    for i in mirrored_ctrls:
        if cmds.objExists(i): ### Check if obj exist as in some cases the constraint could be deleted as descendant of ikHandle
            if cmds.objectType(i, isAType='constraint') or cmds.objectType(i, isAType='ikHandle'):
                cmds.delete(i)

    # mirrored_root_ctrl_name = cmds.rename(f'{root_ctrl_grp}1', replace_prefix(root_ctrl_grp))
    # print(f'- {mirrored_root_ctrl_name}')
    # all_remained_descendants = cmds.listRelatives(mirrored_root_ctrl_name, ad=True)
    # for i in all_remained_descendants:
    #     mirrored_ctrl_name = cmds.rename(i, replace_prefix(i)[:-1])
    #     print(f'- {mirrored_ctrl_name}')

    # mirrored_ctrl_dict = {}
    # for i in original_node_list:
    #     mirrored_ctrl_dict[i] = cmds.duplicate(i, n='new_utility_node')[0]
    
    # renamed_mirrored_node_dict = {}
    # for i in mirrored_ctrl_dict:
    #     renamed_mirrored_node_dict[i] = cmds.rename(mirrored_ctrl_dict[i], replace_prefix(i))


    ### Mirror the root ctrl grp 
    if mirror_axis == 'x':
        cmds.scale(-1, 1, 1, mirrored_root_ctrl_name)
    elif mirror_axis == 'y':
        cmds.scale(1, -1, 1, mirrored_root_ctrl_name)
    elif mirror_axis == 'z':
        cmds.scale(1, 1, -1, mirrored_root_ctrl_name)

    ### Freeze the scale value
    greatest_descendants = cmds.listRelatives(mirrored_root_ctrl_name, c=True)
    tmp_grp = cmds.group(n='tmp_grp', empty=True)
    cmds.parent(greatest_descendants, 'tmp_grp')

    cmds.makeIdentity(mirrored_root_ctrl_name, apply=True, normal=0, preserveNormals=True)

    cmds.parent(greatest_descendants, mirrored_root_ctrl_name)
    cmds.delete(tmp_grp)

    print(f'- {mirrored_root_ctrl_name}')

    all_objs = cmds.ls(dag=True)
    ordered_mirrored_ctrl_list = [i for i in all_objs if i in mirrored_ctrl_dict.values()]

    for i in ordered_mirrored_ctrl_list:
        split_list = cmds.ls(i, l=True)[0].split('|')
        print(f"{((len(split_list[split_list.index(mirrored_root_ctrl_name):]) - 1) * 2) * ' '}- {i}")


# mirror_controls()