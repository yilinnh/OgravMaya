import maya.cmds as cmds
import maya.api.OpenMaya as om

def match_object_to_vertex(target_object, vertex):
    # Get the selection list from the vertex name
    sel = om.MSelectionList()
    sel.add(vertex)
    
    # Get the component object
    dag_path, component = sel.getComponent(0)
    
    # Access the mesh's MFnMesh
    mesh_fn = om.MFnMesh(dag_path)
    
    # Extract the vertex indices from the component
    vertex_indices = om.MFnSingleIndexedComponent(component).getElements()
    
    # Ensure there's exactly one vertex
    if len(vertex_indices) != 1:
        cmds.error("Please select exactly one vertex.")
        return
    
    # Get the world space position of the vertex
    vertex_position = mesh_fn.getPoint(vertex_indices[0], om.MSpace.kWorld)
    
    # Set the translation of the target object
    cmds.xform(target_object, ws=True, t=(vertex_position.x, vertex_position.y, vertex_position.z))


def main():
    sel = cmds.ls(sl=True)
    half_len = int(len(sel)/2)
    f_half = sel[:half_len]
    s_half = sel[half_len:]
    for i in f_half:
        match_object_to_vertex(i, s_half[f_half.index(i)])
