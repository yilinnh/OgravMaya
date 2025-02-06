import maya.cmds as cmds

# match two transform node 
def main():
    sel = cmds.ls(sl=True)
    
    if len(sel) < 2: 
        print("Not enough objects selected")
        return
    
    half_len = int(len(sel)/2)
    source = sel[:half_len]
    target = sel[half_len:]

    if len(source) != len(target):
        print("Not matched objects quantity")
        return

    proxy = cmds.group(n='proxy',empty=True) 

    for i in source:
        cmds.matchTransform(proxy, i, pos=True, scl=True)
        cmds.makeIdentity(proxy, apply=True)
        cmds.matchTransform(proxy, target[source.index(i)], rot=True)

        sel_parent = cmds.listRelatives(i, p=True)
        cmds.parent(i, proxy)
        cmds.makeIdentity(i, apply=True, r=True, t=False, s=False)

        if sel_parent:
            cmds.parent(i, sel_parent)
        else:
            cmds.parent(i, world=True)

    cmds.delete(proxy)

# main()