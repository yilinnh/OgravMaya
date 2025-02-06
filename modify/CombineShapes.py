import maya.cmds as cmds

def main():
    sel = cmds.ls(sl=True)
    
    if len(sel) > 1:
        cmds.warning("Please select a target transform node")
        return
    
    target_transform = sel[0]

    ad = cmds.listRelatives(target_transform, ad=True)
    shape_ad = [i for i in ad if cmds.objectType(i, isAType='shape')]
    shape_ad = [i for i in shape_ad if cmds.listRelatives(i, p=True)[0] != target_transform]

    [cmds.parent(i, target_transform, s=True, r=True) for i in shape_ad if cmds.listRelatives(i, p=True) != target_transform]

    [cmds.delete(i) for i in ad if not cmds.objectType(i, isAType='shape')]
    cmds.xform(target_transform, centerPivots=True)
    cmds.select(target_transform)

    # freeze
    # If apply flag is true, the accumulated transforms are applied to the shape after the transforms are made identity, such that the world space positions of the transforms pivots are preserved, and the shapes do not move.
    # cmds.makeIdentity(apply=True)

    # target_transform = sel[0]
    # target_transform = cmds.listRelatives(sel[-1], p=True)
    # if not target_transform:
    #     target_transform = cmds.group(n="newCurve", empty=True)

    # cmds.parent(sel, target_transform, s=True, r=True)
    
    # for i in sel:
    #     # Get all shape nodes under the selected transform
    #     shapes = cmds.listRelatives(i, ad=True, shapes=True, fullPath=True) or []
        
    #     for shape in shapes:
    #         # Parent the shape under the target transform
    #         cmds.parent(shape, target_transform, shape=True, relative=True)
        
    #     # Delete the empty sel transform
    #     cmds.delete(i)
    
    # cmds.select(target_transform)

    # print(f"Shapes combined into {target_transform}")


# main()