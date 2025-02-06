import maya.cmds as cmds
import importlib

AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_suffix = all_attrs['ctrl_suffix']
mirror_axis = all_attrs['mirror_axis']

# src = getattr(AutoMirror, 'src') 
# mir = getattr(AutoMirror, 'mir')
# ctrl_suffix = getattr(AutoMirror, 'ctrl_suffix') 
# mirror_axis = getattr(AutoMirror, 'mirror_axis') 

main_folder = getattr(AutoMirror, 'main_folder')
sub_folder = getattr(AutoMirror, 'sub_folder')

def main():

    print("\n--------------------------------------------------")
    print("# CUSTOMIZED ATTRIBUTES")
    print("--------------------------------------------------")

    def customize_mirrored_controls_attrs():
        MirrorControls = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorControls')
        # importlib.reload(MirrorControls)

        if hasattr(MirrorControls, 'get_variables'):
            all_variables = MirrorControls.get_variables()
            all_mir_ctrls = all_variables['all_mir_ctrls']
            # all_mir_ctrls = [i for i in cmds.ls(dag=True, type='transform') if i.startswith(mir)]

            ### change fk_ik_switch mirrored text

            fk_ik_switch_tag = 'fkIkSwitch'

            if all_mir_ctrls:
                scale_ctrl_grp = []
                for i in all_mir_ctrls:
                    if fk_ik_switch_tag in i:
                        child = cmds.listRelatives(i, c=True)[0]

                        if cmds.objectType(child, isAType='shape'):
                            scale_ctrl_grp.append(cmds.listRelatives(i, p=True)[0])
                
                for i in scale_ctrl_grp:
                    # if fk_ik_switch_tag in i and fk_ik_switch_tag not in cmds.listRelatives(i, p=True)[0]:
                        if mirror_axis == 'x':
                            cmds.scale(-1, 1, 1, i)
                        elif mirror_axis == 'y':
                            cmds.scale(1, -1, 1, i)
                        elif mirror_axis == 'y':
                            cmds.scale(1, 1, -1, i)

                        # cmds.makeIdentity(i, apply=True, s=True, t=False, r=False)

                        print(f'- Controls mirrored in {mirror_axis} axis (in local space): {i}')
            
            ### change all ctrls line width
            # all_mir_ctrls = [i for i in all_mir_ctrls if ctrl_suffix in i]
            
            for i in all_mir_ctrls:
                try:
                    cmds.setAttr(f"{i}.lineWidth", 2)
                except:
                    continue
            
            ### connect attrs for mir ctrls from non-mirroed nodes
            all_src_ctrls = [i for i in cmds.ls(dag=True, type='transform') if i.startswith(src) and ctrl_suffix in i]

            sour_connections = []

            for i in all_src_ctrls:
                sour_connections += cmds.listConnections(i, s=True, d=False, c=True, p=True) or []

            ### filter the visibility connections
            vis_sour_connections = [[sour_connections[i], sour_connections[i+1]] for i in range(0, len(sour_connections), 2) if sour_connections[i].split('.')[1] == 'visibility' and not sour_connections[i+1].startswith(src)]

            mir_vis_sour_connections = [[vis_sour_connections[i][0].replace(src, mir, 1), vis_sour_connections[i][1]] for i in range(len(vis_sour_connections))]

            for i in mir_vis_sour_connections:
                if cmds.objExists(i[0].split('.')[0]):
                    cmds.connectAttr(i[1], i[0])
                    print(f'- {i[1]} -> {i[0]}')



    def customize_mirrored_nodes_attrs():
        MirrorNodeConnections = importlib.import_module(f'{main_folder}.{sub_folder}.MirrorNodeConnections')
        # importlib.reload(MirrorNodeConnections)

        if hasattr(MirrorNodeConnections, 'get_variables'):
            all_variables = MirrorNodeConnections.get_variables()
            all_mir_nodes = all_variables['all_mir_nodes']
            all_ori_nodes = all_variables['all_ori_nodes']

            # utility_node_types = ["addDoubleLinear", "angleBetween", "arrayMapper", "blendColors", "blendTwoAttr", "bump2d", "bump3d", "choice", "chooser", "clamp", "colorProfile", "condition", "contrast", "curveInfo", "decomposeMatrix", "distanceBetween", "frameCache", "gammaCorrect", "heightField", "hsvToRgb", "lightInfo", "luminance", "multDoubleLinear", "multiplyDivide", "place2dTexture", "place3dTexture", "plusMinusAverage", "projection", "particleSamplerInfo", "remapColor", "remapHsv", "remapValue", "reverse", "rgbToHsv", "samplerInfo", "setRange", "stencil", "surfaceInfo", "surfaceLuminance", "unitConversion", "uvChooser", "vectorProduct"]

            # ### get all utility nodes that need to be mirrored
            # all_mir_nodes = []
            # for t in utility_node_types:
            #     nodes = cmds.ls(type=f'{t}')
            #     all_mir_nodes.extend([n for n in nodes if n.startswith(mir)])

            slider_jnt_pos_rv_node_tags = ['bulge_trans', 'slide_trans']
            mir_slider_jnt_bulge_pos_rv_nodes = []


            if all_mir_nodes:
                for n in all_mir_nodes:
                    # mir_foot_twist_direction_md_nodes += [n for i in foot_twist_direction_md_node_tags if i in n]
                    mir_slider_jnt_bulge_pos_rv_nodes += [n for i in slider_jnt_pos_rv_node_tags if i in n and cmds.objectType(n, isType='remapValue')]

            
            if mir_slider_jnt_bulge_pos_rv_nodes:
                for i in mir_slider_jnt_bulge_pos_rv_nodes:
                    if cmds.objExists(i):
                        output_min = cmds.getAttr(f'{i}.outputMin')
                        output_max = cmds.getAttr(f'{i}.outputMax')
                        cmds.setAttr(f'{i}.outputMin', output_min * (-1))
                        cmds.setAttr(f'{i}.outputMax', output_max * (-1))
                        print(f'- {i}.outputMin -> {output_min * (-1)}')
                        print(f'- {i}.outputMax -> {output_max * (-1)}')

            ### change bank factor to oppsite value
            revFootBank_factor_md = ['revFootBank_factor_md']


            # foot_twist_direction_md_node_tags = ['toe_twist_direction_multi', 'heel_twist_direction_multi']
            # mir_foot_twist_direction_md_nodes = []

            # if mir_foot_twist_direction_md_nodes:
            #     for i in mir_foot_twist_direction_md_nodes:
            #         if cmds.objExists(i):
            #             attr_value = cmds.getAttr(f'{i}.input2X')
            #             cmds.setAttr(f'{i}.input2X', attr_value * (-1))
            #             print(f'- {i}.input2X -> {attr_value * (-1)}')


            ### filter the blendshape connections
            ori_dest_connections = []
            for i in all_ori_nodes:
                ori_dest_connections += cmds.listConnections(i, s=False, d=True, c=True, p=True, scn=True) or []


                # bs_sour_connections = [[sour_connections[i], sour_connections[i+1]] for i in range(0, len(sour_connections), 2) if cmds.objectType(sour_connections[i+1].split('.')[0], isType='blendShape')]

                # mir_bs_sour_connections = [[bs_sour_connections[i][0].replace(src, mir, 1), bs_sour_connections[i][1]] for i in range(len(bs_sour_connections))]

            ori_dest_connections = [[ori_dest_connections[i], ori_dest_connections[i+1]] for i in range(0, len(ori_dest_connections), 2)]

            ori_bs_dest_connections = [i for i in ori_dest_connections if cmds.objectType(i[1].split('.')[0], isType='blendShape') and i[1].split('.')[1].startswith(src)]

            mir_bs_dest_connections = []

            for i in ori_bs_dest_connections:
                dest_node = i[1].split('.')[0]
                dest_attr = i[1].split('.')[1]
                if dest_attr.startswith(src):
                    mir_bs_dest_connections.append([i[0].replace(src, mir, 1), f'{dest_node}.{dest_attr.replace(src, mir, 1)}'])
                    
            for i in mir_bs_dest_connections:
                if cmds.objExists(i[0].split('.')[0]):
                    cmds.connectAttr(i[0], i[1])
                    print(f'- {i[0]} -> {i[1]}')


    customize_mirrored_controls_attrs()
    customize_mirrored_nodes_attrs()

    cmds.select(cl=True)


def make_identity_individually(item):
    children = cmds.listRelatives(item, c=True)

    if children:
        cmds.parent(children, world=True)
        cmds.makeIdentity(item, apply=True)
        cmds.parent(children, item)
    else:
        cmds.makeIdentity(item, apply=True)
    

# main()