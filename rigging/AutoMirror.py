import importlib

def main():
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
    # MirrorIkHandles.mirror_ik_handles()
    # MirrorConstraints.mirror_constraints()
    # MirrorNodeConnections.mirror_node_connections()
    
main()