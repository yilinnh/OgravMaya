import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True, type='transform')
    
    if len(sel) < 2:
        cmds.error("Please select at least two transform nodes")
        return

    # freeze
    # If apply flag is true, the accumulated transforms are applied to the shape after the transforms are made identity, such that the world space positions of the transforms pivots are preserved, and the shapes do not move.
    cmds.makeIdentity(apply=True)

    # target_transform = sel[0]
    target_transform = cmds.listRelatives(sel, p=True)
    if not target_transform:
        target_transform = cmds.group(n="newCurve", empty=True)
    
    for s in sel:
        # Get all shape nodes under the selected transform
        shapes = cmds.listRelatives(s, ad=True, shapes=True, fullPath=True) or []
        
        for shape in shapes:
            # Parent the shape under the target transform
            cmds.parent(shape, target_transform, shape=True, relative=True)
        
        # Delete the empty sel transform
        cmds.delete(s)
    
    cmds.xform(target_transform, centerPivots=True)
    cmds.select(target_transform)

    print(f"Shapes combined into {target_transform}")

