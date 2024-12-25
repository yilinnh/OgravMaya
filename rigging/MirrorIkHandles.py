import maya.cmds as cmds

def mirror_ik_handles():

    print("\n--------------------------------------------------")
    print("# IK HANDLE")
    print("--------------------------------------------------")

    # ik = 'l_leg_ikHandle'
    all_ik = [i for i in cmds.ls(type='ikHandle') if i.startswith('l_')]

    for ik in all_ik:

        # Get all connections 
        all_connections = cmds.listConnections(ik, c=True, p=False)

        connection_dict = {}

        for i in range(0, len(all_connections), 2):
            connection_dict[all_connections[i].split('.')[1]] = all_connections[i+1]

        # Get the end effector joint instead of effector itself
        end_effector = connection_dict['endEffector']
        end_joint = list(set(cmds.listConnections(end_effector, s=True, d=False)))
        if len(end_joint) == 1:
            end_joint = end_joint[0]
        else:
            cmds.warning(f'More than one end joint: {end_joint}')

        connection_dict['endEffector'] = end_joint

        # Mirror the dict
        mirrored_connection_dict = {key:value.replace('l_', 'r_', 1) for key,value in connection_dict.items()}

        # Create IK handle
        mirrored_ik = cmds.ikHandle(sj=mirrored_connection_dict['startJoint'], ee=mirrored_connection_dict['endEffector'], solver=mirrored_connection_dict['ikSolver'])

        # Rename IK handle and move to the appropriate
        # mirrored_ik = ['ikHandle1', 'effector2']
        mirrored_ik_name = mirrored_ik[0]
        mirrored_ik_name = cmds.rename(mirrored_ik_name, ik.replace('l_', 'r_', 1))
        ik_parent = cmds.listRelatives(ik, p=True)
        mirrored_ik_parent = ik_parent[0].replace('l_', 'r_', 1)
        cmds.parent(mirrored_ik_name, mirrored_ik_parent)

        print(f"- {ik.replace('l_', 'r_', 1)}")
        print(f"    - Start Joint: {mirrored_connection_dict['startJoint']}")
        print(f"    - End Joint: {mirrored_connection_dict['endEffector']}")
        print(f"    - IK Solver: {mirrored_connection_dict['ikSolver']}")


# mirror_ik_handles()