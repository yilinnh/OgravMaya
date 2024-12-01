import maya.cmds as cmds

def main():
    # Prompt for the axis input
    axis = cmds.promptDialog(
        title='Rotate Object',
        message='Enter Axis (x, y, or z):',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )
    
    if axis == 'OK' or axis == 'Cancel':

        sel = cmds.ls(sl=True, type='transform')
        if not sel:
            print("No objects selected")
            return

        # Get the input value
        key = cmds.promptDialog(q=True, text=True).lower()
        if key in ['x', 'y', 'z', 'xx', 'yy', 'zz', 'xxx', 'yyy', 'zzz']:
            # Map axis to rotation vector
            rotation_dict = {'x': (90, 0, 0), 'y': (0, 90, 0), 'z': (0, 0, 90), 'xx': (180, 0, 0), 'yy': (0, 180, 0), 'zz': (0, 0, 180), 'xxx': (270, 0, 0), 'yyy': (0, 270, 0), 'zzz': (0, 0, 270)}
            rotation = rotation_dict[key]
            
            # Apply rotation to each selected object
            for obj in sel:
                cmds.rotate(rotation[0], rotation[1], rotation[2], obj, relative=True, os=True)
            
            cmds.inViewMessage(
                msg=f"Rotated {rotation}",
                pos='topCenter',
                fade=True
            )
        else:
            print("Invalid input")

# Run the function
# main()
