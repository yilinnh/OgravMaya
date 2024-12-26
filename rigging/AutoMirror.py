import importlib
import maya.cmds as cmds

src = 'l_'
mir = 'r_'
ctrl_grp_suffix = '_ctrl'
mirror_axis = 'x'

def main():

    all_objs = cmds.ls()
    short_name_all_objs = [i.split('|')[-1] for i in all_objs]
    duplicated_name_ctrls = list(set([i for i in short_name_all_objs if short_name_all_objs.count(i) > 1]))
    if duplicated_name_ctrls:
        print("--------------------------------------------------")
        cmds.warning(f"More than one object matches name:")
        for i in duplicated_name_ctrls:
            cmds.warning(i)
        return

    main_folder = 'OgravMaya'
    sub_folder = 'rigging'

    MirrorJoints = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorJoints')
    MirrorIkHandles = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorIkHandles')
    MirrorControls = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorControls')
    MirrorConstraints =  importlib.import_module(f'{main_folder}.{sub_folder}.MirrorConstraints')
    MirrorNodeConnections = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorNodeConnections')

    importlib.reload(MirrorJoints)
    importlib.reload(MirrorControls)
    importlib.reload(MirrorIkHandles)
    importlib.reload(MirrorConstraints)
    importlib.reload(MirrorNodeConnections)

    MirrorJoints.mirror_joints()
    MirrorControls.mirror_controls()
    MirrorIkHandles.mirror_ik_handles()
    MirrorConstraints.mirror_constraints()
    MirrorNodeConnections.mirror_node_connections()
    
main()