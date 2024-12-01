import maya.cmds as cmds
import maya.mel as mm 

def main():
    softSelectEnabled = cmds.softSelect(query=True, sse=True)
    if softSelectEnabled:
        cmds.softSelect(sse=0)
        print("Soft selection off")
    else:
        cmds.softSelect(sse=1)
        print("Soft selection on")
