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



    tmp_grp = cmds.group(n='tmp_grp', empty=True)
    # mir_root_ctrl_grp_parent_dict = {cmds.listRelatives(i, p=True)[0]:i for i in mir_root_ctrl_grps}
    greatest_descendants = cmds.listRelatives(mir_root_ctrl_grps, c=True)
    mir_root_ctrl_grp_parent_dict = {i:cmds.listRelatives(i, p=True)[0] for i in greatest_descendants}

    ### Mirror the root ctrl grp 
    if mirror_axis == 'x':
        cmds.scale(-1, 1, 1, mir_root_ctrl_grps)
    elif mirror_axis == 'y':
        cmds.scale(1, -1, 1, mir_root_ctrl_grps)
    elif mirror_axis == 'z':
        cmds.scale(1, 1, -1, mir_root_ctrl_grps)

    cmds.parent(greatest_descendants, tmp_grp)

    cmds.makeIdentity(mir_root_ctrl_grps, apply=True, normal=0, preserveNormals=True)

    for i in mir_root_ctrl_grp_parent_dict:
        cmds.parent(i, mir_root_ctrl_grp_parent_dict[i])

    cmds.delete(tmp_grp)

    all_dags = cmds.ls(dag=True, l=True)
    for i in mir_root_ctrl_grps:
        print(f"- {i}")
        ad = cmds.listRelatives(i, ad=True, fullPath=True)
        if ad:
            ad = [i for i in all_dags if i in ad]
            for d in ad:
                split_list = d.split('|')
                split_list = split_list[split_list.index(i):]
                indent = (len(split_list) * 2 - 2) * ' '
                print(f"{indent}- {d.split('|')[-1]}")
            

mirror_controls()