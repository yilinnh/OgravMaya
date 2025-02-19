import maya.cmds as cmds
import importlib

AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_suffix = all_attrs['ctrl_suffix']
mirror_axis = all_attrs['mirror_axis']

def main():

    print("\n--------------------------------------------------")
    print("# IK HANDLE")
    print("--------------------------------------------------")

    # src_ik = 'l_leg_ikHandle'
    all_src_ik = [i for i in cmds.ls(type='ikHandle') if i.startswith(src)]

    if not all_src_ik:
        print("No source IK handles found")
        return

    all_mir_ik = [i.replace(src, mir, 1) for i in all_src_ik]
    update_existing_mirrored_ik_handles(all_mir_ik)

    for src_ik in all_src_ik:

        # Get all connections 
        all_connections = cmds.listConnections(src_ik, c=True, p=False)

        connection_dict = {}
        for i in range(0, len(all_connections), 2):
            connection_dict[all_connections[i].split('.')[1]] = all_connections[i+1]

        # Get the end effector joint instead of effector itself, which is the in-between node
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

        # Rename IK handle and move to the relevant parents
        # mir_ik list pattern: ['ikHandle1', 'effector2']
        mir_ik_name = mir_ik[0]
        mir_ik_name = cmds.rename(mir_ik_name, src_ik.replace(src, mir, 1))

        all_src_ik_parents = cmds.listRelatives(src_ik, p=True, f=True)[0].split('|')
        for i in all_src_ik_parents:
            if i.startswith(src):
                all_src_ik_parents = all_src_ik_parents[all_src_ik_parents.index(i):]
                break

        all_mir_ik_parent_dict = {i.replace(src, mir, 1):i for i in all_src_ik_parents}
        for i in all_mir_ik_parent_dict:
            if not cmds.objExists(i):
                cmds.duplicate(all_mir_ik_parent_dict[i], n=i, parentOnly=True)
            src_parent = cmds.listRelatives(all_mir_ik_parent_dict[i], p=True)[0]
            mir_parent = src_parent.replace(src, mir, 1)
            if cmds.listRelatives(i, p=True)[0] != mir_parent:
                cmds.parent(i, mir_parent)

        src_ik_parent = cmds.listRelatives(src_ik, p=True)[0]
        mir_ik_parent = src_ik_parent.replace(src, mir, 1)

        cmds.parent(mir_ik_name, mir_ik_parent)

        
        # Print out the results
        print(f"- {src_ik.replace(src, mir, 1)}")
        print(f"    - Start Joint: {mir_connection_dict['startJoint']}")
        print(f"    - End Joint: {mir_connection_dict['endEffector']}")
        print(f"    - IK Solver: {mir_connection_dict['ikSolver']}")

    cmds.select(cl=True)


def update_existing_mirrored_ik_handles(items):
    for i in items: 
        if cmds.objExists(i):
            cmds.delete(i)
            print(f"Updated existing mirrored IK handles: {i}")

# main()