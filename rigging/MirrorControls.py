import maya.cmds as cmds
import importlib
### reload will also run the imported module
AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
src = getattr(AutoMirror, 'src') 
mir = getattr(AutoMirror, 'mir')
ctrl_grp_suffix = getattr(AutoMirror, 'ctrl_grp_suffix') 
mirror_axis = getattr(AutoMirror, 'mirror_axis') 

def mirror_controls():

    print("\n--------------------------------------------------")
    print("# CONTROLS")
    print("--------------------------------------------------")

    ### Find the root ctrl grp
    all_objs = cmds.ls(dag=True, type='transform')
    short_name_all_objs = [i.split('|')[-1] for i in all_objs]
    for i in short_name_all_objs:
        if short_name_all_objs.count(i) > 1:
            cmds.warning(f"More than one object matches name: {i}")
            return

    src_ctrl_grps = [i for i in all_objs if i.startswith(src) and ctrl_grp_suffix in i]
    src_root_ctrl_grps = [i for i in src_ctrl_grps if not cmds.listRelatives(i, p=True)[0].startswith(src)]
    mir_root_ctrl_grps = [i.replace(src, mir, 1) for i in src_root_ctrl_grps]

    ### duplicate the grps to make sure the src_ctrl_descendants have ctrl root name in their relative paths
    # tmp_root_ctrl_grps = cmds.duplicate(src_root_ctrl_grps, returnRootsOnly=True)
    # ### Get all ctrls and reorder them based on the dag hierarchy
    # src_ctrl_descendants = cmds.listRelatives(src_root_ctrl_grps, ad=True, path=True)
    # src_ctrl_descendants = [i for i in src_ctrl_descendants if i.split('|')[-1].startswith(src)]
    # ### this will only mirror the root ctrl name as it's at the first position in the path
    # # mir_ctrl_descendants = [i.replace(src, mir, 1) for i in src_ctrl_descendants]

    # cmds.delete(tmp_root_ctrl_grps)

    for i in src_root_ctrl_grps:
        cmds.duplicate(i, n=i.replace(src, mir, 1))

    # for i in mir_ctrl_descendants:
    #     cmds.rename(i, i.split('|')[-1].replace(src, mir, 1))
    mir_ctrl_list = []
    for i in [cmds.listRelatives(i, ad=True, fullPath=True) for i in mir_root_ctrl_grps]:
        mir_ctrl_list.extend(i)

    ### rename all mirrored controls
    mir_ctrl_list = [cmds.rename(i, i.split('|')[-1].replace(src, mir, 1)) for i in mir_ctrl_list]

    ### Find and delete redundant descendants
    redundant_descendants = []
    for i in mir_ctrl_list:
        if cmds.objExists(i): ### Check if obj exist as in some cases the constraint could be deleted as descendant of ikHandle
            if cmds.objectType(i, isAType='constraint') or cmds.objectType(i, isAType='ikHandle'):
                redundant_descendants.append(i)
                cmds.delete(i)
                # pass

    mir_ctrl_list = list(set(mir_ctrl_list).difference(set(redundant_descendants)))

    # mir_ctrl_list = [cmds.rename(i, i.split('|')[-1].replace(src, mir, 1)) for i in mir_ctrl_descendants]


    
    # all_objs = cmds.ls(dag=True, type='transform')
    # short_name_all_objs = [i.split('|')[-1] for i in all_objs]
    # duplicate_name_ctrls = list(set([i for i in short_name_all_objs if short_name_all_objs.count(i) > 1]))
    # if duplicate_name_ctrls:
    #     cmds.warning(f"Following ctrls have the duplicated name: {duplicate_name_ctrls}")
    #     return

    # ctrl_grps = [i for i in all_objs if i.startswith(src) and ctrl_grp_suffix in i]
    # root_ctrl_grps = [i for i in ctrl_grps if not cmds.listRelatives(i, p=True)[0].startswith(src)]
    # print(all_objs)
    # print(ctrl_grps)
    # print(root_ctrl_grps)

    # ### Get all ctrls and reorder them based on the dag hierarchy
    # all_ctrl_descendants = cmds.listRelatives(root_ctrl_grps, ad=True, fullPath=True)
    # all_ctrl_descendants = [i for i in all_ctrl_descendants if i.split('|')[-1].startswith(src)]

    # mir_root_ctrl_grps = {i.replace(src, mir, 1):i for i in root_ctrl_grps}

    # ### Generate a dict like: {'l_ctrl_grp|l_ctrl': 'r_ctrl'}
    # # mir_all_ctrl_dict = {i:i.split('|')[-1].replace(src, mir, 1) for i in all_ctrl_descendants}
    # ### Change the keys from 'l_ctrl_grp|l_ctrl' to 'r_ctrl_grp|l_ctrl'
    # # mir_all_ctrl_dict = {i.replace(root_ctrl_grps, mir_root_ctrl_grps, 1):mir_all_ctrl_dict[i] for i in mir_all_ctrl_dict}

    # mir_ctrl_dict = {}

    


    # # all_ctrls.append(root_ctrl_grps)
    # # print(all_ctrls)
    # # all_ctrls = [i for i in all_objs if i in all_ctrls]
    # # print(all_ctrls)

    # ### Duplicate all ctrls
    # ### Shouldn't use the built-in rename for duplicating it will increase the digital suffix
    # for i in root_ctrl_grps:
    #     cmds.duplicate(i, n=mir_root_ctrl_grps[i])

    # ### Name 'r_ctrl_grp|l_ctrl' as 'r_ctrl'
    # mir_ctrl_list = [cmds.rename(i, mir_all_ctrl_dict[i]) for i in mir_all_ctrl_dict]
    # mir_ctrl_list = []
    # for i in mir_all_ctrl_dict:
    #     mir_ctrl_list.append(cmds.rename(i, mir_all_ctrl_dict[i]))
    
    # mir_all_ctrl_dict = {i.split('|')[-1].replace(mir_all_ctrl_dict[i], mir_all_ctrl_dict[i].replace(src, mir, 1)):mir_all_ctrl_dict[i] for i in mir_all_ctrl_dict}

    # mir_ctrl_list = []
    # for l in mir_all_ctrl_dict:
    #     split_list = i.split('|')
    #     split_list = [i[:2].replace(src, mir, 1) + i[2:] for i in split_list]
    #     # split_list = [i.replace(src, mir, 1) for i in split_list if i.startswith(src)]
    #     long_path = '|'.join(split_list)
    #     mir_ctrl_list.append(long_path)
        # mir_ctrl_name = split_list[-1].replace(src, mir, 1)
        # split_list = split_list[:-1]
        # split_list.append(mir_ctrl_name)
        # long_path = '|'.join(split_list)
        # mir_ctrl_list.append(long_path)

    # print(mir_ctrl_list)
    # mir_ctrl_dict_values = list(mir_all_ctrl_dict.values())
    # mir_all_ctrl_dict = {}
    # for i in range(len(mir_ctrl_list)):
    #     mir_all_ctrl_dict[mir_ctrl_list[i]] = mir_ctrl_dict_values[i]

    # mir_all_ctrl_dict = {mir_ctrl_list[i]:mir_ctrl_dict_values[i] for i in range(len(mir_ctrl_list))}

    # print(mir_all_ctrl_dict)
    # mir_root_ctrl_grps = cmds.rename(f'{root_ctrl_grps}1', replace_prefix(root_ctrl_grps))
    # print(f'- {mir_root_ctrl_grps}')
    # all_remained_descendants = cmds.listRelatives(mir_root_ctrl_grps, ad=True)
    # for i in all_remained_descendants:
    #     mir_ctrl_name = cmds.rename(i, replace_prefix(i)[:-1])
    #     print(f'- {mir_ctrl_name}')

    # mir_all_ctrl_dict = {}
    # for i in original_node_list:
    #     mir_all_ctrl_dict[i] = cmds.duplicate(i, n='new_utility_node')[0]
    
    # renamed_mir_node_dict = {}
    # for i in mir_all_ctrl_dict:
    #     renamed_mir_node_dict[i] = cmds.rename(mir_all_ctrl_dict[i], replace_prefix(i))



    tmp_grp = cmds.group(n='tmp_grp', empty=True)
    mir_root_ctrl_grp_parent_dict = {i:cmds.listRelatives(i, p=True)[0] for i in mir_root_ctrl_grps}
    cmds.parent(mir_root_ctrl_grps, tmp_grp)
    ### Mirror the root ctrl grp 
    if mirror_axis == 'x':
        cmds.scale(-1, 1, 1, tmp_grp)
    elif mirror_axis == 'y':
        cmds.scale(1, -1, 1, tmp_grp)
    elif mirror_axis == 'z':
        cmds.scale(1, 1, -1, tmp_grp)

    for i in mir_root_ctrl_grps:
        cmds.parent(i, mir_root_ctrl_grp_parent_dict[i])

    cmds.makeIdentity(mir_root_ctrl_grps, apply=True, normal=0, preserveNormals=True)

    cmds.delete(tmp_grp)

    all_dags = cmds.ls(dag=True, l=True)
    for i in mir_root_ctrl_grps:
        print(f"- {i}")
        ad = cmds.listRelatives(i, ad=True, fullPath=True)
        ad = [i for i in all_dags if i in ad]
        for d in ad:
            split_list = d.split('|')
            split_list = split_list[split_list.index(i):]
            indent = (len(split_list) * 2 - 2)* ' '
            print(f"{indent}- {d.split('|')[-1]}")
            


    # ### Mirror the root ctrl grp 
    # if mirror_axis == 'x':
    #     cmds.scale(-1, 1, 1, mir_root_ctrl_grps)
    # elif mirror_axis == 'y':
    #     cmds.scale(1, -1, 1, mir_root_ctrl_grps)
    # elif mirror_axis == 'z':
    #     cmds.scale(1, 1, -1, mir_root_ctrl_grps)

    # ### Freeze the scale value
    # greatest_descendants = cmds.listRelatives(mir_root_ctrl_grps, c=True)
    # descendant_relative_path_dict = {i:cmds.listRelatives(i, p=True)[0] for i in greatest_descendants}
    # tmp_grp = cmds.group(n='tmp_grp', empty=True)
    # cmds.parent(greatest_descendants, 'tmp_grp')

    # cmds.makeIdentity(mir_root_ctrl_grps, apply=True, normal=0, preserveNormals=True)

    # for i in greatest_descendants:
    #     cmds.parent(i, descendant_relative_path_dict[i])

    # cmds.delete(tmp_grp)

    # print(f'- {mir_root_ctrl_grps}')

    # all_objs = cmds.ls(dag=True)
    # ordered_mir_ctrl_list = [i for i in all_objs if i in mir_ctrl_list]

    # for i in ordered_mir_ctrl_list:
    #     split_list = cmds.ls(i, l=True)[0].split('|')
    #     print(f"{((len(split_list[split_list.index(mir_root_ctrl_grps):]) - 1) * 2) * ' '}- {i}")


# mirror_controls()