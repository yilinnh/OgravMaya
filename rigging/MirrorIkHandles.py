import maya.cmds as cmds
import importlib
AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
src = getattr(AutoMirror, 'src') 
mir = getattr(AutoMirror, 'mir')

def mirror_ik_handles():

    print("\n--------------------------------------------------")
    print("# IK HANDLE")
    print("--------------------------------------------------")

    # ik = 'l_leg_ikHandle'
    all_ik = [i for i in cmds.ls(type='ikHandle') if i.startswith(src)]

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
        mir_connection_dict = {key:value.replace(src, mir, 1) for key,value in connection_dict.items()}

        # Create IK handle
        mir_ik = cmds.ikHandle(sj=mir_connection_dict['startJoint'], ee=mir_connection_dict['endEffector'], solver=mir_connection_dict['ikSolver'])

        # Rename IK handle and move to the appropriate
        # mir_ik = ['ikHandle1', 'effector2']
        mir_ik_name = mir_ik[0]
        mir_ik_name = cmds.rename(mir_ik_name, ik.replace(src, mir, 1))
        ik_parent = cmds.listRelatives(ik, p=True)
        mir_ik_parent = ik_parent[0].replace(src, mir, 1)
        cmds.parent(mir_ik_name, mir_ik_parent)

        print(f"- {ik.replace(src, mir, 1)}")
        print(f"    - Start Joint: {mir_connection_dict['startJoint']}")
        print(f"    - End Joint: {mir_connection_dict['endEffector']}")
        print(f"    - IK Solver: {mir_connection_dict['ikSolver']}")


# mirror_ik_handles()