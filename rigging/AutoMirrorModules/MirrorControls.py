import maya.cmds as cmds
import importlib
### reload will also run the imported module
AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_grp_suffix = all_attrs['ctrl_grp_suffix']
mirror_axis = all_attrs['mirror_axis']

def main():

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
    ### check if there's any unfrozen value
    for i in src_root_ctrl_grps:
        if not check_if_frozen(i):
            print(f"At least one root control group has unfrozen transformation values: {i}")
            cmds.select(i)
            return

    ### update and mirror root control grps
    mir_root_ctrl_grps = [i.replace(src, mir, 1) for i in src_root_ctrl_grps]
    update_existing_mirrored_controls(mir_root_ctrl_grps)

    for i in src_root_ctrl_grps:
        cmds.duplicate(i, n=i.replace(src, mir, 1))

    ### get all mirrored ctrl paths
    global all_mir_ctrls
    all_mir_ctrls = []

    for i in [cmds.listRelatives(i, ad=True, fullPath=True) for i in mir_root_ctrl_grps]:
        all_mir_ctrls.extend(i)

    ### rename all mirrored controls
    all_mir_ctrls = [cmds.rename(i, i.split('|')[-1].replace(src, mir, 1)) for i in all_mir_ctrls]

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
    if mirror_axis == 'x':
        cmds.scale(-1, 1, 1, mir_root_ctrl_grps)
    elif mirror_axis == 'y':
        cmds.scale(1, -1, 1, mir_root_ctrl_grps)
    elif mirror_axis == 'z':
        cmds.scale(1, 1, -1, mir_root_ctrl_grps)

    [make_identity_individually(i) for i in mir_root_ctrl_grps]


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
            
    print(mirror_axis)

def update_existing_mirrored_controls(items):
    for i in items: 
        if cmds.objExists(i):
            cmds.delete(i)
            print(f"Updated existing mirrored root controls: {i}")


def check_if_frozen(control_grp):
    translation = cmds.getAttr(f"{control_grp}.translate")[0]
    rotation = cmds.getAttr(f"{control_grp}.rotate")[0]
    scale = cmds.getAttr(f"{control_grp}.scale")[0]
    
    all_transformation = translation + rotation + scale
    frozen_transformation = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0)
    
    return all_transformation == frozen_transformation


def make_identity_individually(item):
    children = cmds.listRelatives(item, c=True)

    if children:
        cmds.parent(children, world=True)
        cmds.makeIdentity(item, apply=True)
        cmds.parent(children, item)
    else:
        cmds.makeIdentity(item, apply=True)


def get_variables():
    return {
        'all_mir_ctrls': all_mir_ctrls
    }

# main()
