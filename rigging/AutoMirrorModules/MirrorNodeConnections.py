import maya.cmds as cmds
import importlib

AutoMirror = importlib.import_module('OgravMaya.rigging.AutoMirror')
# importlib.reload(AutoMirror)

all_attrs = AutoMirror.get_attrs()
src = all_attrs['src']
mir = all_attrs['mir']
ctrl_grp_suffix = all_attrs['ctrl_grp_suffix']
mirror_axis = all_attrs['mirror_axis']

def main():
    
    def mirror_connection_node_and_attr_name(ori_list, mir_list):
        for a,b in ori_list:
            a_node_name = a.split('.')[0]
            a_attr_name = a.split('.')[1]

            b_node_name = b.split('.')[0]
            b_attr_name = b.split('.')[1]

            ### mirror the name
            a_node_name = a_node_name.replace(src, mir, 1)
            b_node_name = b_node_name.replace(src, mir, 1)

            if a_attr_name.startswith(src):
                a_attr_name = a_attr_name.replace(src, mir, 1)
            if b_attr_name.startswith(src):
                b_attr_name = b_attr_name.replace(src, mir, 1)

            mir_list.append([f'{a_node_name}.{a_attr_name}', f'{b_node_name}.{b_attr_name}'])


    def exclude_connections(ori_list, exclude_list):
        for a,b in ori_list:
            a_node_name = a.split('.')[0]
            a_attr_name = a.split('.')[1]

            b_node_name = b.split('.')[0]
            b_attr_name = b.split('.')[1]

            ### exclude the node connections that don't have left prefix
            if not a_node_name.startswith(src) or not b_node_name.startswith(src):
                exclude_list.append([a, b])
            ### exclude the connections with constarint.target, as this has already connected on the previous MirrorConstraints step and might also raise an error
            if cmds.objectType(b_node_name, isAType='constraint') and 'target' in b_attr_name:
                exclude_list.append([a, b])


    def mirror_utility_node_connections():
        print("\n--------------------------------------------------")
        print("# UTILITY NODE")
        print("--------------------------------------------------")

        # utility_node_types = ('plusMinusAverage', 'multiplyDivide', 'condition', 'clamp', 'remapValue', 'remapColor', 'blendColors', 'reverse', 'distanceBetween', 'multMatrix')

        utility_node_types = ["addDoubleLinear", "angleBetween", "arrayMapper", "blendColors", "blendTwoAttr", "bump2d", "bump3d", "choice", "chooser", "clamp", "clearCoat", "colorProfile", "condition", "contrast", "curveInfo", "decomposeMatrix", "distanceBetween", "doubleSwitch", "frameCache", "gammaCorrect", "heightField", "hsvToRgb", "lightInfo", "lookdevKit", "luminance", "multDoubleLinear", "multiplyDivide", "place2dTexture", "place3dTexture", "plusMinusAverage", "projection", "particleSamplerInfo", "quadSwitch", "remapColor", "remapHsv", "remapValue", "reverse", "rgbToHsv", "samplerInfo", "setRange", "singleSwitch", "smear", "stencil", "studioClearCoat", "surfaceInfo", "surfaceLuminance", "tripleSwitch", "unitConversion", "uvChooser", "vectorProduct", "matrixNodes"]



        ### get all utility nodes that need to be mirrored
        all_ori_nodes = []
        for t in utility_node_types:
            nodes = cmds.ls(type=f'{t}')
            all_ori_nodes.extend([n for n in nodes if n.startswith(src)])

        global all_mir_nodes
        all_mir_nodes = [i.replace(src, mir, 1) for i in all_ori_nodes]
        update_existing_mirrored_nodes(all_mir_nodes)

         ### assign the mirror node dict and get original node connections
        ori_sour_connections, ori_dest_connections = [], []
        # mir_node_dict = {}

        # for i in ori_node_dict:
        for i in all_ori_nodes:
            ### source list: input <- output
            ### destination list: output -> input
            ori_sour_connections += cmds.listConnections(i, s=True, d=False, c=True, p=True, scn=True) or []
            ori_dest_connections += cmds.listConnections(i, s=False, d=True, c=True, p=True, scn=True) or []


        ### package the connection list:
        ### [a.attr, b.attr, c.attr, d.attr] to [[a.attr, b.attr], [c.attr, d.attr]]
        ori_sour_connections = [[ori_sour_connections[i], ori_sour_connections[i+1]] for i in range(0, len(ori_sour_connections), 2)]
        ori_dest_connections = [[ori_dest_connections[i], ori_dest_connections[i+1]] for i in range(0, len(ori_dest_connections), 2)]


        ### exclude the node connections that don't have left prefix
        exclude_sour_connections, exclude_dest_connections = [], []

        exclude_connections(ori_sour_connections, exclude_sour_connections)
        exclude_connections(ori_dest_connections, exclude_dest_connections)


        ori_sour_connections = [i for i in ori_sour_connections if i not in exclude_sour_connections]
        ori_dest_connections = [i for i in ori_dest_connections if i not in exclude_dest_connections]

        ### prevent repeating the connections from srouce connection list
        ori_dest_connections = [i for i in ori_dest_connections if i not in ori_sour_connections]

        ### rename the connection 
        mir_sour_connections, mir_dest_connections = [], []
        mirror_connection_node_and_attr_name(ori_sour_connections, mir_sour_connections)
        mirror_connection_node_and_attr_name(ori_dest_connections, mir_dest_connections)
        

        ### get mirrored nodes name ready and duplicate original nodes
        mir_node_dict = {}
        for i in all_ori_nodes:
            mir_node_dict[i] = cmds.duplicate(i, n='tmp_mir_utility_node')[0]
        
        renamed_mir_node_dict = {}
        for i in mir_node_dict:
            renamed_mir_node_dict[i] = cmds.rename(mir_node_dict[i], i.replace(src, mir, 1))
        
        ### connect node attributes
        for i in mir_sour_connections:
            if cmds.isConnected(i[1], i[0]):
                continue
            else:
                cmds.connectAttr(i[1], i[0], f=True)
                print(f'- {i[1]} -> {i[0]}')

        for i in mir_dest_connections:
            if cmds.isConnected(i[0], i[1]):
                continue
            else:
                cmds.connectAttr(i[0], i[1], f=True)
                print(f'- {i[0]} -> {i[1]}')



    def mirror_contorl_attr_connections():
        print("\n--------------------------------------------------")
        print("# CONTROL ATTRIBUTE")
        print("--------------------------------------------------")

        all_objs = cmds.ls(dag=True, type='transform')
        ctrl_grps = [i for i in all_objs if i.startswith(src) and 'ctrl_grp' in i]
        root_ctrl_grp = [i for i in ctrl_grps if not cmds.listRelatives(i, p=True)[0].startswith(src)][0]

        all_descendants = cmds.listRelatives(root_ctrl_grp, ad=True)

        ### get original connections
        ori_sour_connections, ori_dest_connections = [], []

        for i in all_descendants:
            if i.startswith(src) and cmds.objectType(i, isType='transform'):
                ### source list: input <- output
                ### destination list: output -> input
                ori_sour_connections += cmds.listConnections(i, s=True, d=False, c=True, p=True, scn=True) or []
                ori_dest_connections += cmds.listConnections(i, s=False, d=True, c=True, p=True, scn=True) or []

        ### package the connection list:
        ### [a.attr, b.attr, c.attr, d.attr] to [[a.attr, b.attr], [c.attr, d.attr]]
        ori_sour_connections = [[ori_sour_connections[i], ori_sour_connections[i+1]] for i in range(0, len(ori_sour_connections), 2)]
        ori_dest_connections = [[ori_dest_connections[i], ori_dest_connections[i+1]] for i in range(0, len(ori_dest_connections), 2)]

        ### exclude invalid connections
        exclude_sour_connections, exclude_dest_connections = [], []
        exclude_connections(ori_sour_connections, exclude_sour_connections)
        exclude_connections(ori_dest_connections, exclude_dest_connections)

        ori_sour_connections = [i for i in ori_sour_connections if i not in exclude_sour_connections]
        ori_dest_connections = [i for i in ori_dest_connections if i not in exclude_dest_connections]

        ### prevent repeating the connections from srouce connection list
        ori_dest_connections = [i for i in ori_dest_connections if i not in ori_sour_connections]

        ### rename the connection 
        mir_sour_connections, mir_dest_connections = [], []
        mirror_connection_node_and_attr_name(ori_sour_connections, mir_sour_connections)
        mirror_connection_node_and_attr_name(ori_dest_connections, mir_dest_connections)
        
        
        for i in mir_sour_connections:
            if cmds.isConnected(i[1], i[0]):
                continue
            else:
                cmds.connectAttr(i[1], i[0], f=True)
                print(f'- {i[1]} -> {i[0]}')

        for i in mir_dest_connections:
            if cmds.isConnected(i[0], i[1]):
                continue
            else:
                cmds.connectAttr(i[0], i[1], f=True)
                print(f'- {i[0]} -> {i[1]}')


    mirror_utility_node_connections()
    mirror_contorl_attr_connections()


def update_existing_mirrored_nodes(items):
    for i in items: 
        if cmds.objExists(i):
            cmds.delete(i)
            print(f"Updated existing mirrored nodes: {i}")


def get_variables():
    return {
        'all_mir_nodes': all_mir_nodes
    }

# main()