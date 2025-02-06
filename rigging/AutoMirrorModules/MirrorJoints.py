import maya.cmds as cmds
import importlib

AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_suffix = all_attrs['ctrl_suffix']
mirror_axis = all_attrs['mirror_axis']
ofst_suffix = 'ofst'

def main():

    print("\n--------------------------------------------------")
    print("# JOINT")
    print("--------------------------------------------------")

    ### Get all left root joint to mirror
    all_joints = cmds.ls(dag=True, type='joint')
    all_src_joints = [i for i in all_joints if i.startswith(src)]
    if not all_src_joints:
        print("No source joints found")
        return

    # all_src_root_joints = [i for i in all_src_joints if not cmds.listRelatives(i, p=True)[0].startswith(src) or not cmds.listRelatives(i, p=True, type='joint')]
    # all_src_root_joints = [i for i in all_src_joints if not cmds.listRelatives(i, p=True)[0].startswith(src)]
    # all_src_root_joints = [i for i in all_src_joints if cmds.listRelatives(i, p=True)[0].startswith(src) and not cmds.listRelatives(i)]
    all_src_root_joints = []
    for i in all_src_joints:
        parent = cmds.listRelatives(i, p=True)[0]
        if cmds.objectType(parent, isType='joint') and not parent.startswith(src):
            all_src_root_joints.append(i)
        elif cmds.objectType(parent, isType='transform') and parent.startswith(src):
            # if not parent.endswith(ofst_suffix):
            all_src_root_joints.append(i)

    ### exclude the duplicates
    # all_src_root_joints = [i for i in set(all_src_root_joints) if i in all_src_root_joints]
    print(f'All src root joints: {all_src_root_joints}\n')

    # all_mir_joints_new_name = [i.replace(src, mir, 1) for i in all_src_joints]
    all_mir_root_joints = [i.replace(src, mir, 1) for i in all_src_root_joints]
    update_existing_mirrored_joints(all_mir_root_joints)

    all_mir_joints = []

    if mirror_axis == 'x':
        for i in all_src_root_joints:
            # mir_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorYZ=True)
            mir_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorYZ=True)
            all_mir_joints.extend(mir_joint_list)

    elif mirror_axis == 'y':
        for i in all_src_root_joints:
            mir_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorXZ=True)
            all_mir_joints.extend(mir_joint_list)

    elif mirror_axis == 'z':
        for i in all_src_root_joints:
            mir_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorXY=True)
            all_mir_joints.extend(mir_joint_list)


    ### reorder all mir joints and rename them
    all_joints = cmds.ls(dag=True, type='joint')
    # all_src_joints = [i for i in all_joints if i in all_src_joints]
    # all_mir_joints = [i for i in all_joints if i not in all_src_joints and i.startswith(src)]
    all_mir_joints = [i for i in all_mir_joints if cmds.objectType(i, isType='joint')]
    # all_mir_joints = [i for i in all_joints if i in all_mir_joints]

    all_mir_joints_new_name = [i.replace(src, mir, 1) for i in all_src_joints]

    # for a,b,c in zip(all_src_joints, all_mir_joints, all_mir_joints_new_name):
        # print(f'{a} -> {b} - {c}')

    # print("\nRenamed mirrored joints:")
    for i,n in zip(all_mir_joints, all_mir_joints_new_name):
        print(f'{i} -> {n}')
        cmds.rename(i, n)

    all_mir_joints = all_mir_joints_new_name

    ## Delete all redundant and invalid nodes under right side joints
    all_mir_root_joints = [i for i in all_mir_joints if not cmds.listRelatives(i, p=True)[0].startswith(mir)]

    all_joints = cmds.ls(dag=True, type='joint', l=True)

    print("Mirrored joints hierarchy:")
    for i in all_mir_root_joints:
        ad = cmds.listRelatives(i, ad=True)
        if ad:
            [cmds.delete(d) for d in ad if cmds.objectType(d, isAType='constraint') or cmds.objectType(d, isAType='ikHandle') or cmds.objectType(d, isAType = 'ikEffector')]
            [cmds.rename(d, d.replace(src, mir, 1)[:-1]) for d in ad if d.endswith(f'{ofst_suffix}1')]


        all_joint_descendants = cmds.listRelatives(i, ad=True, fullPath=True)

        print(f'- {i}')
        root_joint_name = i.split('|')[-1]

        if all_joint_descendants:
            all_joint_descendants = [i for i in all_joints if i in all_joint_descendants]

            for d in all_joint_descendants:
                split_list = d.split('|')
                split_list = split_list[split_list.index(root_joint_name):]
                print(f"{(len(split_list) * 2 - 2) * ' '}- {split_list[-1]}")
            

    ### reorient the joints that should orient to the world
    # world_oriented_src_joints = [i for i in all_src_joints if is_joint_oriented_to_world(i)]
    # world_oriented_mir_joints = [i.replace(src, mir, 1) for i in world_oriented_src_joints]

    # [cmds.joint(i, e=True, oj='none') for i in world_oriented_mir_joints]
    # for i in world_oriented_mir_joints:
    #     parent = cmds.listRelatives(i, p=True)
    #     if parent:
    #         cmds.parent(i, world=True)
    #         cmds.joint(i, e=True, oj='none')
    #         cmds.parent(i, parent)
    #     else:
    #         cmds.joint(i, e=True, oj='none')



    def parent_to_mir_group(root):
        src_parent_dict = {}
        for i in root:
            # p = cmds.listRelatives(i, p=True, type='transform')[0]
            p = cmds.listRelatives(i, p=True)[0]
            if p.startswith(src) and cmds.objectType(p, isType='transform'):
                src_parent_dict[i] = p
                ### duplicate from src to mir groups
                mir_p_grp = p.replace(src, mir, 1)
                if not cmds.objExists(mir_p_grp):
                    mir_p_grp = cmds.duplicate(p, n=mir_p_grp, parentOnly=True)[0]
                    mir_p_grp_parent = cmds.listRelatives(mir_p_grp, p=True)[0]

                    tmp_grp = cmds.group(empty=True)
                    cmds.parent(mir_p_grp, tmp_grp)
                    
                    if mirror_axis == 'x':
                        cmds.scale(-1, 1, 1, tmp_grp)
                    elif mirror_axis == 'y':
                        cmds.scale(1, -1, 1, tmp_grp)
                    elif mirror_axis == 'z':
                        cmds.scale(1, 1, -1, tmp_grp)
                    
                    cmds.makeIdentity(tmp_grp, apply=True, s=True)

                    cmds.parent(mir_p_grp, mir_p_grp_parent)
                    cmds.delete(tmp_grp)

                    # if cmds.getAttr(f'{p}.offsetParentMatrix') == init_ofst_parent_matrix:
                    #     continue
                    # else:
                    #     bake_to_offset_parent_matrix(mir_p_grp)

                else:
                    continue
            else:
                continue


        if  src_parent_dict:
            mir_parent_dict = {c.replace(src, mir, 1):p.replace(src, mir, 1) for c,p in src_parent_dict.items()}
            [cmds.parent(c, p) for c,p in mir_parent_dict.items() if cmds.listRelatives(c, p=True)[0] != p]

        return src_parent_dict

    src_joint_parent_dict = parent_to_mir_group(all_src_root_joints)
    nested_src_joint_parent_dict = parent_to_mir_group(src_joint_parent_dict.values())



    # print(f"\nWorld oriented joints:")
    # [print(f"- {i}") for i in world_oriented_mir_joints]

    ### prevent scale the joints in letter process 
    cmds.select(cl=True)


def make_identity_individually(item):
    children = cmds.listRelatives(item, c=True)

    if children:
        cmds.parent(children, world=True)
        cmds.makeIdentity(item, apply=True)
        cmds.parent(children, item)
    else:
        cmds.makeIdentity(item, apply=True)


def is_joint_oriented_to_world(joint_name):
    """
    Check if a joint is oriented to the world (jointOrient is effectively zero).
    """
    # Get the joint's world matrix
    world_matrix = cmds.xform(joint_name, query=True, matrix=True, worldSpace=True)
    
    # Extract the axes from the matrix
    x_axis = world_matrix[0:3]
    y_axis = world_matrix[4:7]
    z_axis = world_matrix[8:11]

    # Check if the axes align with the world axes (tolerance for floating-point errors)
    tolerance = 1e-6
    is_x_aligned = abs(x_axis[0] - 1) < tolerance and abs(x_axis[1]) < tolerance and abs(x_axis[2]) < tolerance
    is_y_aligned = abs(y_axis[1] - 1) < tolerance and abs(y_axis[0]) < tolerance and abs(y_axis[2]) < tolerance
    is_z_aligned = abs(z_axis[2] - 1) < tolerance and abs(z_axis[0]) < tolerance and abs(z_axis[1]) < tolerance

    # Return True if all axes align with world axes
    return is_x_aligned and is_y_aligned and is_z_aligned


def bake_to_offset_parent_matrix(obj):
    if not cmds.objExists(obj):
        raise ValueError(f"Object '{obj}' does not exist.")

    # Get the object's current world matrix
    world_matrix = cmds.xform(obj, q=True, matrix=True, ws=True)
    print(world_matrix)
    # Apply the current world matrix to the offsetParentMatrix
    cmds.setAttr(f"{obj}.offsetParentMatrix", world_matrix, type="matrix")

    # Reset local transformations
    cmds.setAttr(f"{obj}.translate", 0, 0, 0)
    cmds.setAttr(f"{obj}.rotate", 0, 0, 0)
    cmds.setAttr(f"{obj}.scale", 1, 1, 1)


def update_existing_mirrored_joints(items):
    for i in items: 
        if cmds.objExists(i):
            cmds.delete(i)
            print(f"Updated existing mirrored root joint: {i}")


# main()
