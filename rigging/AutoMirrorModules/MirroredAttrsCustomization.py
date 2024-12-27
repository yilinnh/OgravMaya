import maya.cmds as cmds
import importlib

AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_grp_suffix = all_attrs['ctrl_grp_suffix']
mirror_axis = all_attrs['mirror_axis']

# src = getattr(AutoMirror, 'src') 
# mir = getattr(AutoMirror, 'mir')
# ctrl_grp_suffix = getattr(AutoMirror, 'ctrl_grp_suffix') 
# mirror_axis = getattr(AutoMirror, 'mirror_axis') 

main_folder = getattr(AutoMirror, 'main_folder')
sub_folder = getattr(AutoMirror, 'sub_folder')

def main():

    def customize_mirrored_controls_attrs():
        MirrorControls = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorControls')
        importlib.reload(MirrorControls)

        if hasattr(MirrorControls, 'get_variables'):
            all_variables = MirrorControls.get_variables()

            ### change fk_ik_switch mirrored text
            all_mir_ctrls = all_variables['all_mir_ctrls']
            fk_ik_switch_tag = 'fkIkSwitch'

            for i in all_mir_ctrls:
                if fk_ik_switch_tag in i and fk_ik_switch_tag not in cmds.listRelatives(i, p=True)[0]:
                    if mirror_axis == 'x':
                        cmds.scale(-1, 1, 1, i)
                    elif mirror_axis == 'y':
                        cmds.scale(1, -1, 1, i)
                    elif mirror_axis == 'y':
                        cmds.scale(1, 1, -1, i)

                    make_identity_individually(i)

    def customize_mirrored_nodes_attrs():
        MirrorNodeConnections = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorNodeConnections')
        importlib.reload(MirrorNodeConnections)

        if hasattr(MirrorNodeConnections, 'get_variables'):
            all_variables = MirrorNodeConnections.get_variables()

            ### change utility node attributes
            all_mir_nodes = all_variables['all_mir_nodes']
            multi_nodes_tag = ['toe_twist_direction_multi', 'heel_twist_direction_multi']

            mirrored_multi_nodes = []
            for n in all_mir_nodes:
                mirrored_multi_nodes += [n for i in multi_nodes_tag if i in n]

            for i in mirrored_multi_nodes:
                attr_value = cmds.getAttr(f'{i}.input2X')
                cmds.setAttr(f'{i}.input2X', attr_value * (-1))


    customize_mirrored_controls_attrs()
    customize_mirrored_nodes_attrs()


def make_identity_individually(item):
    children = cmds.listRelatives(item, c=True)

    if children:
        cmds.parent(children, world=True)
        cmds.makeIdentity(item, apply=True)
        cmds.parent(children, item)
    else:
        cmds.makeIdentity(item, apply=True)
    

# main()