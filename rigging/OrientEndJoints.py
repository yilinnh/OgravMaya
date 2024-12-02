import maya.cmds as cmds

def main():
    # List all joints in the scene
    all_joints = cmds.ls(type="joint")
    sel = cmds.ls(sl=True)
    if sel:
        all_joints = [i for i in sel if i in all_joints]

    end_joints = []
    
    for joint in all_joints:
        # Check if the joint has any children
        children = cmds.listRelatives(joint, children=True)
        if not children:  # If no children, it's an end joint
            end_joints.append(joint)
    
    for i in end_joints:
        cmds.joint(i, e=True, oj='none')

# main()