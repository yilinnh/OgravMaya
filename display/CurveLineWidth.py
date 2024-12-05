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
    ofst_form = cmds.formLayout(w=100, p=base_form)

    cmds.formLayout(base_form, e=True, attachForm=[(ofst_form,"top",10), (ofst_form,"bottom",10), (ofst_form,"left",10), (ofst_form,"right",10)])

    slider_row = cmds.rowColumnLayout(nc=2, cw=[(1,win_w-50), (2,50)], cs=[(2,8)])
    global slider
    slider = cmds.floatSlider(min=1, max=2, value=1, dragCommand=handle_slider_change)
    global value_text
    value_text = cmds.text(l="1.0", align="left")

    # footer_row = create_row_column_layout(2, win_w/2-15, 10, ofst_form)
    footer_form = cmds.formLayout(p=ofst_form)
    apply_btn = cmds.button(l="Apply", c=handle_apply)
    close_btn = cmds.button(l="Close", c=handle_close)

    cmds.formLayout(ofst_form, e=True, 
                    af=[(footer_form,'left',0), (footer_form,'right',0)],
                    ac=[(footer_form,"top",10,slider_row)])

    two_col_form(footer_form, apply_btn, close_btn)

def two_col_form(form, l_col, r_col):
    cmds.formLayout(form, e=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,49), (r_col,'left',0,51)])


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