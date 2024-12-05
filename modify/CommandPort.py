import maya.cmds as cmds

def main():
    cmds.commandPort(name="localhost:7001", sourceType="mel")
    cmds.commandPort(name="localhost:5678", sourceType="python")
    print("vs code command port has been set")
