import maya.cmds as cmds
# sel = cmds.ls(sl=True, type="nurbsCurve")
# w = float(input())
# for i in sel:
# 	cmds.setAttr(f"{i}.lineWidth", w)
def main():
    global win
    win= "CurveLineWidth"

    win_w = 200
    win_h = 70

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t="Curve Line Width", wh=(win_w, win_h), s=False, mxb=False, mnb=False)
    cmds.showWindow(win)

    base_form = cmds.formLayout()
    main_form = cmds.formLayout(w=100, p=base_form)

    cmds.formLayout(base_form, e=True, attachForm=[(main_form,"top",10), (main_form,"bottom",10), (main_form,"left",10), (main_form,"right",10)])

    slider_row = create_row_column_layout(2, 155, 10, main_form)
    cmds.rowColumnLayout(slider_row, e=True, cw=(2,20))
    global slider
    slider = cmds.floatSlider(min=1, max=2, value=1, dragCommand=handle_slider_change)
    global value_text
    value_text = cmds.text(l="1.0", align="left")

    footer_row = create_row_column_layout(2, win_w/2-15, 10, main_form)
    cmds.button(l="Apply", c=handle_apply)
    cmds.button(l="Close", c=handle_close)

    cmds.formLayout(main_form, e=True, ac=[(footer_row,"top",10,slider_row)])


def create_row_column_layout(num_of_col, col_width, col_spacing, parent, **kwargs):
    cw = []
    cs = []
    for i in range(num_of_col):
        cw.append((i+1, col_width))
        if i == 0:
            cs.append((i+1, 0)) 
        else:    
            cs.append((i+1, col_spacing)) 
    return cmds.rowColumnLayout(nc=num_of_col, cw=cw, cs=cs, p=parent, **kwargs)


def handle_slider_change(*args):
    global value
    value = float(str(cmds.floatSlider(slider, q=True, v=True))[0:3])
    cmds.text(value_text, e=True, l=value)
    sel = cmds.ls(sl=True)
    if sel:
        for i in sel:
            cmds.setAttr(f"{i}.lineWidth", value)


def handle_apply(*args):
    value = float(str(cmds.floatSlider(slider, q=True, v=True))[0:3])
    sel = cmds.ls(sl=True)
    if sel:
        for i in sel:
            cmds.setAttr(f"{i}.lineWidth", value)


def handle_close(*args):
    cmds.deleteUI("CurveLineWidth")

# main()