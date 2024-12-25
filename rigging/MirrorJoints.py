import maya.cmds as cmds

def mirror_joints():

    print("\n--------------------------------------------------")
    print("# JOINT")
    print("--------------------------------------------------")

    # Get all left root joint to mirror
    all_joints = cmds.ls(dag=True, type='joint')
    all_original_joint = [i for i in all_joints if i.startswith('l_')]
    all_root_original_joints = [i for i in all_original_joint if not cmds.listRelatives(i, p=True)[0].startswith('l_')]
    all_mirrored_joints = []
    for i in all_root_original_joints:
        mirrored_joint_list = cmds.mirrorJoint(i, mirrorBehavior=True, mirrorYZ=True)
        for j in list(mirrored_joint_list):
            if cmds.objectType(j, isType='joint'):
                mirrored_joint = cmds.rename(j, j.replace('l_', 'r_', 1)[:-1])
                all_mirrored_joints.append(mirrored_joint)

    # all_joints = cmds.ls(dag=True, type='joint')
    # all_mirrored_joints = [i for i in all_joints if i.startswith('r_')]

    # for i in all_mirrored_joints:
        # cmds.rename(i, i.replace('l_', 'r_', 1)) 
    # all_mirrored_joints = [i.replace('l_', 'r_', 1)) for i in all_mirrored_joints]

    # all_mirrored_joints = [cmds.rename(i, i.replace('l_', 'r_', 1)) for i in all_mirrored_joints]
    # all_mirrored_joints = [cmds.rename(i, i[:-1]) for i in all_mirrored_joints if i.endswith('1')]

    # Delete all redundant and invalid nodes under right side joints
    # all_root_mirrored_joints = [i for i in all_mirrored_joints if not cmds.listRelatives(i, p=True)[0].startswith('r_')]

    all_root_mirrored_joints = [i.replace('l_', 'r_', 1) for i in all_root_original_joints]

    all_mirrored_joint_descendants = []

    for i in all_root_mirrored_joints:
        descendants = cmds.listRelatives(i, ad=True) 
        if descendants:
            all_mirrored_joint_descendants += descendants
        print(f'- {i}')

    for i in all_mirrored_joint_descendants:
        if not cmds.objectType(i, isType='joint'):
            cmds.delete(i)


# mirror_joints()