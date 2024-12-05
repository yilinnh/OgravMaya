import maya.cmds as cmds

def main():
    cmds.tumbleCtx(autoSetPivot=True)
    print("tumble auto set pivot has turned on")