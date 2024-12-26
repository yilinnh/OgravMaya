import maya.cmds as cmds
import importlib
AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
### getattr will only get the variable, which won't run the module like using 'newvar = module.var' method
src = getattr(AutoMirror, 'src') 
mir = getattr(AutoMirror, 'mir')
mirror_axis = getattr(AutoMirror, 'mirror_axis') 

# src = AutoMirror.src
# mir = AutoMirror.mir
# from AutoMirror import src, mir

def mirror_joints():

    print("\n--------------------------------------------------")
    print("# JOINT")
    print("--------------------------------------------------")

    ### Get all left root joint to mirror
    all_joints = cmds.ls(dag=True, type='joint')
    all_src_joints = [i for i in all_joints if i.startswith(src)]
    all_src_root_joints = [i for i in all_src_joints if not cmds.listRelatives(i, p=True)[0].startswith(src)]
    # all_mir_joints = []

    if mirror_axis == 'x':
        for i in all_src_root_joints:
            mir_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorYZ=True)
            [cmds.rename(j, j.replace(src, mir, 1)[:-1]) for j in mir_joint_list if cmds.objectType(j, isType='joint')]

            # for j in mir_joint_list:
            #     if cmds.objectType(j, isType='joint'): ### e.g. it might include constraints
            #         mir_joint = cmds.rename(j, j.replace(src, mir, 1)[:-1])
            #         # all_mir_joints.append(mir_joint)

    elif mirror_axis == 'y':
        for i in all_src_root_joints:
            mir_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorXZ=True)
            [cmds.rename(j, j.replace(src, mir, 1)[:-1]) for j in mir_joint_list if cmds.objectType(j, isType='joint')]

    elif mirror_axis == 'z':
        for i in all_src_root_joints:
            mir_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorXY=True)
            [cmds.rename(j, j.replace(src, mir, 1)[:-1]) for j in mir_joint_list if cmds.objectType(j, isType='joint')]



    # all_joints = cmds.ls(dag=True, type='joint')
    # all_mir_joints = [i for i in all_joints if i.startswith(mir)]

    # for i in all_mir_joints:
        # cmds.rename(i, i.replace(src, mir, 1)) 
    # all_mir_joints = [i.replace(src, mir, 1)) for i in all_mir_joints]

    # all_mir_joints = [cmds.rename(i, i.replace(src, mir, 1)) for i in all_mir_joints]
    # all_mir_joints = [cmds.rename(i, i[:-1]) for i in all_mir_joints if i.endswith('1')]

    ### Delete all redundant and invalid nodes under right side joints
    # all_mir_root_joints = [i for i in all_mir_joints if not cmds.listRelatives(i, p=True)[0].startswith(mir)]

    all_mir_root_joints = [i.replace(src, mir, 1) for i in all_src_root_joints]
    # all_mir_joints = []
    all_joints = cmds.ls(dag=True, type='joint', l=True)

    for i in all_mir_root_joints:
        ad = cmds.listRelatives(i, ad=True)
        if ad:
            [cmds.delete(d) for d in ad if not cmds.objectType(d, isType='joint')]

        all_joint_descendants = cmds.listRelatives(i, ad=True, fullPath=True)

        # all_mir_joints.append(i)
        # if all_joint_descendants:
        #     all_mir_joints.extend(all_joint_descendants)

        print(f'- {i}')
        if all_joint_descendants:
            all_joint_descendants = [i for i in all_joints if i in all_joint_descendants]
            all_joint_descendant_list = [i.split('|')[all_joint_descendants.index(i):] for i in all_joint_descendants]
            all_joint_descendants = ('|').join(all_joint_descendant_list)

            for i in all_joint_descendants:
                split_list = i.split('|')
                print(i)
                print(f"{(len(split_list) - 2) * ' '}- {split_list[-1]}")
            

    ### reorient the joints that should orient to the world
    world_oriented_src_joints = [i for i in all_src_joints if is_joint_oriented_to_world(i)]
    world_oriented_mir_joints = [i.replace(src, mir, 1) for i in world_oriented_src_joints]

    print(f'world_oriented_src_joints: {world_oriented_mir_joints}')
    [cmds.joint(i, e=True, oj='none') for i in world_oriented_mir_joints]

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



mirror_joints()