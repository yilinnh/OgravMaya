import maya.cmds as cmds
import importlib
### reload will also run the imported module
AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_suffix = all_attrs['ctrl_suffix']
loc_suffix = '_loc'
ctrlJnt_suffix = 'ctrlJnt'
mirror_axis = all_attrs['mirror_axis']

all_mir_ctrls = []

def main():

    print("\n--------------------------------------------------")
    print("# CONTROLS")
    print("--------------------------------------------------")

    ### Find the root ctrl grp
    all_objs = cmds.ls(dag=True, type='transform')
    src_ctrl_grps = [i for i in all_objs if i.startswith(src) and ctrl_suffix in i.lower()]
    src_loc_grps = [i for i in all_objs if i.startswith(src) and loc_suffix in i.lower()]

    if src_loc_grps:
        src_ctrl_grps.extend(src_loc_grps)

    if not src_ctrl_grps:
        print("No source controls found")
        return

    src_root_ctrl_grps = [i for i in src_ctrl_grps if not cmds.listRelatives(i, p=True)[0].startswith(src)]
    src_root_ctrl_grps = [i for i in src_root_ctrl_grps if ctrlJnt_suffix not in i]

    print(f"All src root ctrl grps: {src_root_ctrl_grps}\n")
    ### check if there's any unfrozen value
    # unfrozen_src_root_ctrl_grps = [i for i in src_root_ctrl_grps if not check_if_frozen(i)]
    # if unfrozen_src_root_ctrl_grps:
    #     print(f"At least one root control group has unfrozen transformation values: {unfrozen_src_root_ctrl_grps}")
    #     cmds.select(unfrozen_src_root_ctrl_grps)
        # return

    ### update and mirror root control grps
    mir_root_ctrls = [i.replace(src, mir, 1) for i in src_root_ctrl_grps]
    update_existing_mirrored_controls(mir_root_ctrls)

    for i in src_root_ctrl_grps:
        # cmds.duplicate(i)
        cmds.duplicate(i, n=i.replace(src, mir, 1))

    ### get all mirrored ctrl paths
    mir_root_ctrls_ad = []
    for i in mir_root_ctrls:
        mir_root_ctrls_ad += cmds.listRelatives(i, ad=True, fullPath=True)
    
    # for i in reversed(mir_root_ctrls_ad):
    #     print(i)
    #     short_name = i.split('|')[-1]
    #     if short_name.startswith(src):
    #         cmds.rename(i, short_name.replace(src, mir, 1))

    global all_mir_ctrls
    all_mir_ctrls = [i for i in mir_root_ctrls_ad if not cmds.objectType(i, isAType='shape')]
    # all_mir_ctrls = [i for i in mir_root_ctrls_ad]

    # print(all_mir_ctrls)
    ### rename all mirrored controls
    if all_mir_ctrls:
        all_mir_ctrls = [cmds.rename(i, i.split('|')[-1].replace(src, mir, 1)) for i in all_mir_ctrls if i not in mir_root_ctrls]
        ### Find and delete redundant descendants
        redundant_descendants = []
        for i in all_mir_ctrls:
            if cmds.objExists(i): ### Check if obj exist as in some cases the constraint could be deleted as descendant of ikHandle
                if cmds.objectType(i, isAType='constraint') or cmds.objectType(i, isAType='ikHandle'):
                    redundant_descendants.append(i)
                    cmds.delete(i)
                    # pass

        all_mir_ctrls = list(set(all_mir_ctrls).difference(set(redundant_descendants)))

    ### Mirror the root ctrl grp 
    # if mirror_axis == 'x':
    #     cmds.scale(-1, 1, 1, mir_root_ctrls)
    # elif mirror_axis == 'y':
    #     cmds.scale(1, -1, 1, mir_root_ctrls)
    # elif mirror_axis == 'z':
    #     cmds.scale(1, 1, -1, mir_root_ctrls)

    # cmds.makeIdentity(mir_root_ctrls, a=True, s=True, t=False, r=False)

    tmp_group = cmds.group(empty=True)
    mir_root_ctrl_parent_dict = {i:cmds.listRelatives(i, p=True) for i in mir_root_ctrls}
    cmds.parent(mir_root_ctrls, tmp_group)

    if mirror_axis == 'x':
        cmds.scale(-1, 1, 1, tmp_group)
    elif mirror_axis == 'y':
        cmds.scale(1, -1, 1, tmp_group)
    elif mirror_axis == 'z':
        cmds.scale(1, 1, -1, tmp_group)
    
    # cmds.makeIdentity(tmp_group, a=True, s=True, t=False, r=False)

    for i in mir_root_ctrl_parent_dict:
        cmds.parent(i, mir_root_ctrl_parent_dict[i])
    
    cmds.delete(tmp_group)

    # [make_identity_individually(i) for i in mir_root_ctrls]
    # [bake_to_offset_parent_matrix(i) for i in mir_root_ctrls]



    all_dags = cmds.ls(dag=True, l=True)
    for i in mir_root_ctrls:
        print(f"- {i}")
        ad = cmds.listRelatives(i, ad=True, fullPath=True)
        if ad:
            ad = [i for i in all_dags if i in ad]
            for d in ad:
                split_list = d.split('|')
                split_list = split_list[split_list.index(i):]
                indent = (len(split_list) * 2 - 2) * ' '
                print(f"{indent}- {d.split('|')[-1]}")

    cmds.select(cl=True)
            

def update_existing_mirrored_controls(items):
    for i in items: 
        if cmds.objExists(i):
            cmds.delete(i)
            print(f"Updated existing mirrored root controls: {i}")


def check_if_frozen(control_grp):
    translation = cmds.getAttr(f"{control_grp}.translate")[0]
    rotation = cmds.getAttr(f"{control_grp}.rotate")[0]
    # scale = cmds.getAttr(f"{control_grp}.scale")[0]
    
    all_transformation = translation + rotation 
    frozen_transformation = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    
    return all_transformation == frozen_transformation


# def make_identity_individually(item):
#     children = cmds.listRelatives(item, c=True)

#     if children and not cmds.objectType(children, isAType='shape'):
#         cmds.parent(children, world=True)
#         cmds.makeIdentity(item, apply=True)
#         cmds.parent(children, item)
#     else:
#         cmds.makeIdentity(item, apply=True)


# def bake_to_offset_parent_matrix(obj):
#     if not cmds.objExists(obj):
#         raise ValueError(f"Object '{obj}' does not exist.")

#     # Get the object's current world matrix
#     world_matrix = cmds.xform(obj, q=True, matrix=True, ws=True)
#     # Apply the current world matrix to the offsetParentMatrix
#     cmds.setAttr(f"{obj}.offsetParentMatrix", world_matrix, type="matrix")

#     # Reset local transformations
#     cmds.setAttr(f"{obj}.translate", 0, 0, 0)
#     cmds.setAttr(f"{obj}.rotate", 0, 0, 0)
#     cmds.setAttr(f"{obj}.scale", 1, 1, 1)


def get_variables():
    return {
        'all_mir_ctrls': all_mir_ctrls
    }

# main()