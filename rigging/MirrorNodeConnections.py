import maya.cmds as cmds

def mirror_node_connections():

    def replace_prefix(item):
        return item.replace('l_', 'r_', 1)
    
    def mirror_connection_node_and_attr_name(original_list, mirror_list):
        for a,b in original_list:
            a_node_name = a.split('.')[0]
            a_attr_name = a.split('.')[1]

            b_node_name = b.split('.')[0]
            b_attr_name = b.split('.')[1]

            ### mirror the name
            a_node_name = replace_prefix(a_node_name)
            b_node_name = replace_prefix(b_node_name)

            if a_attr_name.startswith('l_'):
                a_attr_name = replace_prefix(a_attr_name)
            if b_attr_name.startswith('l_'):
                b_attr_name = replace_prefix(b_attr_name)

            mirror_list.append([f'{a_node_name}.{a_attr_name}', f'{b_node_name}.{b_attr_name}'])

            # mirrored_node_name = replace_prefix(i)
            # if attr_name.startswith('l_'):
                # mirrored_attr_name = replace_prefix(attr_name)
            # mirror_list.append(f'{mirrored_node_name}.{mirrored_attr_name}')


    def exclude_connections(original_list, exclude_list):
        for a,b in original_list:
            a_node_name = a.split('.')[0]
            a_attr_name = a.split('.')[1]

            b_node_name = b.split('.')[0]
            b_attr_name = b.split('.')[1]

            ### exclude the node connections that don't have left prefix
            if not a_node_name.startswith('l_') or not b_node_name.startswith('l_'):
                exclude_list.append([a, b])
            ### exclude the connections with constarint.target, as this has already connected on the previous MirrorConstraints step and might also raise an error
            if cmds.objectType(b_node_name, isAType='constraint') and 'target' in b_attr_name:
                exclude_list.append([a, b])


    def mirror_utility_node_connections():
        print("\n--------------------------------------------------")
        print("# UTILITY NODE")
        print("--------------------------------------------------")

        utility_node_types = ('plusMinusAverage', 'multiplyDivide', 'condition', 'clamp', 'remapValue', 'remapColor', 'blendColors', 'reverse', 'distanceBetween', 'multMatrix')

        ### get all utility nodes that need to be mirrored
        original_node_list = []
        for t in utility_node_types:
            nodes = cmds.ls(type=f'{t}')
            if nodes:
                # original_node_list = [n for n in nodes if n.startswith('l_')]
                for n in nodes:
                    if n.startswith('l_'):
                        original_node_list.append(n)

        # original_node_dict = {}
        # for t in utility_node_types:
        #     nodes = cmds.ls(type=f'{t}')
        #     if nodes:
        #         for n in nodes:
        #             if n.startswith('l_'):
        #                 original_node_dict[n] = t

        ### assign the mirror node dict and get original node connections
        original_sour_connections, original_dest_connections = [], []
        # mirrored_node_dict = {}

        # for i in original_node_dict:
        for i in original_node_list:
            # mirrored_node_dict[replace_prefix(i)] = original_node_dict[i]

            ### source list: input <- output
            ### destination list: output -> input
            original_sour_connections += cmds.listConnections(i, s=True, d=False, c=True, p=True, scn=True) or []
            original_dest_connections += cmds.listConnections(i, s=False, d=True, c=True, p=True, scn=True) or []


        ### package the connection list:
        ### [a.attr, b.attr, c.attr, d.attr] to [[a.attr, b.attr], [c.attr, d.attr]]
        original_sour_connections = [[original_sour_connections[i], original_sour_connections[i+1]] for i in range(0, len(original_sour_connections), 2)]
        original_dest_connections = [[original_dest_connections[i], original_dest_connections[i+1]] for i in range(0, len(original_dest_connections), 2)]


        ### exclude the node connections that don't have left prefix
        exclude_sour_connections, exclude_dest_connections = [], []

        exclude_connections(original_sour_connections, exclude_sour_connections)
        exclude_connections(original_dest_connections, exclude_dest_connections)

        # for i in original_sour_connections:
        #     if not i[0].split('.')[0].startswith('l_') or not i[1].split('.')[0].startswith('l_'):
        #          exclude_sour_connections.append(i)

        # for i in original_dest_connections:
        #     if not i[0].split('.')[0].startswith('l_') or not i[1].split('.')[0].startswith('l_'):
        #          exclude_dest_connections.append(i)

        # for i in range(0, len(original_sour_connections), 2):
        #     if not original_sour_connections[i].split('.')[0].startswith('l_') or not original_sour_connections[i+1].split('.')[0].startswith('l_'):
        #         exclude_sour_connections += original_sour_connections[i], original_sour_connections[i+1]

        # for i in range(0, len(original_dest_connections), 2):
        #     if not original_dest_connections[i].split('.')[0].startswith('l_') or not original_dest_connections[i+1].split('.')[0].startswith('l_'):
        #         exclude_dest_connections += original_dest_connections[i], original_dest_connections[i+1]

        original_sour_connections = [i for i in original_sour_connections if i not in exclude_sour_connections]
        original_dest_connections = [i for i in original_dest_connections if i not in exclude_dest_connections]

        ### prevent repeating the connections from srouce connection list
        original_dest_connections = [i for i in original_dest_connections if i not in original_sour_connections]

        ### rename the connection 
        mirrored_sour_connections, mirrored_dest_connections = [], []
        mirror_connection_node_and_attr_name(original_sour_connections, mirrored_sour_connections)
        mirror_connection_node_and_attr_name(original_dest_connections, mirrored_dest_connections)
        

        ### get mirrored nodes name ready and duplicate original nodes
        mirrored_node_dict = {}
        for i in original_node_list:
            mirrored_node_dict[i] = cmds.duplicate(i, n='new_mirrored_utility_node')[0]
            # mirrored_node_list.append(cmds.rename(new_node_name, replace_prefix(new_node_name)[:1]))
        
        renamed_mirrored_node_dict = {}
        for i in mirrored_node_dict:
            renamed_mirrored_node_dict[i] = cmds.rename(mirrored_node_dict[i], replace_prefix(i))
        
        # print(renamed_mirrored_node_dict)
            
        # mirrored_node_list = cmds.duplicate(original_node_list, n='new_utility_node')
        # mirrored_node_list = [cmds.rename(i, replace_prefix(i)[:-1]) for i in mirrored_node_list]

        # for i in mirrored_node_dict:
        #     cmds.createNode(mirrored_node_dict[i], n=i)


        ### connect node attributes
        for i in mirrored_sour_connections:
            cmds.connectAttr(i[1], i[0], f=True)
            print(f'- {i[1]} -> {i[0]}')

        for i in mirrored_dest_connections:
            cmds.connectAttr(i[0], i[1], f=True)
            print(f'- {i[0]} -> {i[1]}')

        # for i in range(0, len(mirrored_sour_connections), 2):
        #     cmds.connectAttr(mirrored_sour_connections[i+1], mirrored_sour_connections[i], f=True)
        #     print(f'- {mirrored_sour_connections[i+1]} -> {mirrored_sour_connections[i]}')

        # for i in range(0, len(mirrored_dest_connections), 2):
        #     cmds.connectAttr(mirrored_dest_connections[i], mirrored_dest_connections[i+1], f=True)
        #     print(f'- {mirrored_dest_connections[i]} -> {mirrored_dest_connections[i+1]}')


    def mirror_contorl_attr_connections():
        print("\n--------------------------------------------------")
        print("# CONTROL ATTRIBUTE")
        print("--------------------------------------------------")

        all_objs = cmds.ls(dag=True, type='transform')
        ctrl_grps = [i for i in all_objs if i.startswith('l_') and 'ctrl_grp' in i]
        root_ctrl_grp = [i for i in ctrl_grps if not cmds.listRelatives(i, p=True)[0].startswith('l_')][0]

        all_descendants = cmds.listRelatives(root_ctrl_grp, ad=True)

        ### get original connections
        original_sour_connections, original_dest_connections = [], []

        for i in all_descendants:
            if i.startswith('l_') and cmds.objectType(i, isType='transform'):
                ### source list: input <- output
                ### destination list: output -> input
                original_sour_connections += cmds.listConnections(i, s=True, d=False, c=True, p=True, scn=True) or []
                original_dest_connections += cmds.listConnections(i, s=False, d=True, c=True, p=True, scn=True) or []

        ### package the connection list:
        ### [a.attr, b.attr, c.attr, d.attr] to [[a.attr, b.attr], [c.attr, d.attr]]
        original_sour_connections = [[original_sour_connections[i], original_sour_connections[i+1]] for i in range(0, len(original_sour_connections), 2)]
        original_dest_connections = [[original_dest_connections[i], original_dest_connections[i+1]] for i in range(0, len(original_dest_connections), 2)]

        ### exclude invalid connections
        exclude_sour_connections, exclude_dest_connections = [], []
        exclude_connections(original_sour_connections, exclude_sour_connections)
        exclude_connections(original_dest_connections, exclude_dest_connections)

        original_sour_connections = [i for i in original_sour_connections if i not in exclude_sour_connections]
        original_dest_connections = [i for i in original_dest_connections if i not in exclude_dest_connections]

        ### prevent repeating the connections from srouce connection list
        original_dest_connections = [i for i in original_dest_connections if i not in original_sour_connections]

        ### rename the connection 
        mirrored_sour_connections, mirrored_dest_connections = [], []
        mirror_connection_node_and_attr_name(original_sour_connections, mirrored_sour_connections)
        mirror_connection_node_and_attr_name(original_dest_connections, mirrored_dest_connections)
        
        
        for i in mirrored_sour_connections:
            cmds.connectAttr(i[1], i[0], f=True)
            print(f'- {i[1]} -> {i[0]}')

        for i in mirrored_dest_connections:
            cmds.connectAttr(i[0], i[1], f=True)
            print(f'- {i[0]} -> {i[1]}')


    mirror_utility_node_connections()
    mirror_contorl_attr_connections()


# mirror_node_connections()