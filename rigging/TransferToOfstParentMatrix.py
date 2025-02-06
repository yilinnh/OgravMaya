import maya.cmds as cmds
import maya.api.OpenMaya as om


def main():
    sel = cmds.ls(sl=True)
    for i in sel:
        transfer_to_offset_parent_matrix(i)


def transfer_to_offset_parent_matrix(obj):
    if not cmds.objExists(obj):
        raise ValueError(f"Object '{obj}' does not exist.")

    # Get transformation values
    translate = cmds.getAttr(f"{obj}.translate")[0]
    rotate = cmds.getAttr(f"{obj}.rotate")[0]
    scale = cmds.getAttr(f"{obj}.scale")[0]
    
    # Create a transformation matrix
    transform_matrix = om.MMatrix()
    transform_fn = om.MTransformationMatrix(transform_matrix)

    # Set translate, rotate, and scale
    transform_fn.setTranslation(om.MVector(*translate), om.MSpace.kTransform)
    transform_fn.setRotation(om.MEulerRotation(*[om.MAngle(angle, om.MAngle.kDegrees).asRadians() for angle in rotate]))
    transform_fn.setScale(scale, om.MSpace.kTransform)

    # Get the resulting matrix
    new_matrix = transform_fn.asMatrix()

    # Apply the matrix to the offsetParentMatrix attribute
    cmds.setAttr(f"{obj}.offsetParentMatrix", list(new_matrix), type="matrix")

    # Reset translate, rotate, and scale to defaults
    cmds.setAttr(f"{obj}.translate", 0, 0, 0)
    cmds.setAttr(f"{obj}.rotate", 0, 0, 0)
    cmds.setAttr(f"{obj}.scale", 1, 1, 1)


# main()