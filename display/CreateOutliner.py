import maya.cmds as cmds

def main():
    cmds.window(wh=[300,500])
    cmds.frameLayout( labelVisible=False )
    panel = cmds.outlinerPanel()
    outliner = cmds.outlinerPanel(panel, query=True,outlinerEditor=True)
    cmds.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter', ignoreHiddenAttribute=False, ignoreOutlinerColor=False )
    cmds.showWindow()
