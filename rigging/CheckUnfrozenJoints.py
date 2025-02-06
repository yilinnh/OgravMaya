import maya.cmds as cmds

def main():

    def is_joint_frozen(joint):
        if not cmds.objectType(joint, isType="joint"):
            raise ValueError(f"{joint} is not a joint.")
        
        rotation = cmds.getAttr(f"{joint}.rotate")[0]
        return all(abs(value) < 1e-5 for value in rotation)


    all_joints = cmds.ls(type='joint')
    frozen_rot = [(0.0, 0.0, 0.0)]
    all_unfrozen_joints = [i for i in all_joints if not is_joint_frozen(i)]
    if all_unfrozen_joints:
        print(f"Detected unfrozen joints: {all_unfrozen_joints}")
        cmds.select(all_unfrozen_joints)
    else:
        print("All joints are rig-ready")


