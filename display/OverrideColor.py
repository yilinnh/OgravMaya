import maya.cmds as cmds

class ColorCanvas:

    def __init__(self, color):
        self.color = color
        self.canvas = cmds.canvas(rgbValue=color, pressCommand=self.run_script)

    def run_script(self, *args):
        global rgb_color_value
        global index_color_mode 
        index_color_mode = 0
        rgb_color_value = self.color
        self.selection = cmds.ls(sl=True)

        for i in self.selection:
            rgb = ("R","G","B")
            cmds.setAttr(f"{i}.overrideEnabled", 1)
            cmds.setAttr(f"{i}.overrideRGBColors", 1)

            for channel, color in zip(rgb, self.color):
                cmds.setAttr(f"{i}.overrideColor{channel}", color)


def main():
    global window
    window = "ColorPicker"
    global win_w 
    global win_h
    win_w = 220
    win_h = 160

    if cmds.window(window, exists=True):
        cmds.deleteUI(window)

    cmds.window(window, title="Color Picker", wh=(win_w, win_h), mnb=0, mxb=0, s=0)
    cmds.showWindow(window)
    create_ui()


def create_ui():
    base_form = cmds.formLayout()
    main_form = cmds.formLayout()

    # COLOR PALETTE
    f_color_palette_row = create_row_column_layout(7, win_w/8, 2, main_form, h=22)

    ColorCanvas((0.8,0,0)) # red
    ColorCanvas((0.9,0.4,0.2)) # orange
    ColorCanvas((0.9,0.9,0)) # yellow
    ColorCanvas((0.5,0.8,0.2)) # green
    ColorCanvas((0.2,0.5,1)) # blue
    ColorCanvas((0.4,0.2,1)) # purple
    ColorCanvas((0.0,0.0,1)) # dark blue
    s_color_palette_row = create_row_column_layout(7, win_w/8, 2, main_form, h=22)
    ColorCanvas((0.9,0.3,0.5)) # pink
    ColorCanvas((0.9,0.5,0.8)) # light pink
    ColorCanvas((0.7,0.9,0.5)) # light green
    ColorCanvas((0,0.8,1)) # cyan
    ColorCanvas((0.8,0.8,1)) 
    ColorCanvas((0.6,0.6,0.8)) 
    ColorCanvas((0.0,0.0,0.2))
    # ColorCanvas((0.0,0.1,0.0))
    # ColorCanvas((0.1,0.0,0.0))


    # COLOR SLIDER
    color_slider_sep = create_row_column_layout(1, win_w-20, 0, main_form)
    cmds.separator(st="in", p=color_slider_sep)

    color_slider_row = create_row_column_layout(1, win_w-20, 0, main_form)
    global index_color_slider
    index_color_slider = cmds.colorIndexSliderGrp(label='', columnAlign=[(1,"left"),(2,"left"),(3,"right")], cw=[(1,0),(2,30)], h=20, min=1, max=31, value=1, p=color_slider_row, changeCommand=get_index_slider_color)

    # BOTTOM
    footer_sep = create_row_column_layout(1, win_w-20, 0, main_form)
    cmds.separator(st="in", p=footer_sep)

    footer_row = create_row_column_layout(2, win_w/2-14, 8, main_form)
    apply_btn = cmds.button(l="Apply", p=footer_row, command=on_apply)
    close_btn = cmds.button(l="Close", p=footer_row, command=close_window)

    cmds.formLayout(base_form, e=True,
                    af=[(main_form,"top",15), (main_form,"left",10), (main_form,"right",10), (main_form,"bottom",10)])
    cmds.formLayout(main_form, e=True, 
                    af=[(f_color_palette_row,"left",3), (s_color_palette_row,"left",3), (footer_row,"bottom",0)], 
                    ac=[(s_color_palette_row,"top",5,f_color_palette_row), (color_slider_sep,"top",10,s_color_palette_row), (color_slider_row,"top",5,color_slider_sep), (footer_sep,"top",5,color_slider_row)])


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


def get_index_slider_color(*args):
    global index_color_value
    global index_color_mode
    index_color_mode = 1
    index_color_value = cmds.colorIndexSliderGrp(index_color_slider, query=True, value=True)


def on_apply(*args):
    global index_color_mode
    selection = cmds.ls(sl=True)

    if not selection:
        print("No objects selected")
        return

    for i in selection:
        cmds.setAttr(f"{i}.overrideEnabled", 1)

        if index_color_mode == 0:
            rgb = ("R","G","B")
            cmds.setAttr(f"{i}.overrideRGBColors", 1)

            for channel, color in zip(rgb, rgb_color_value):
                cmds.setAttr(f"{i}.overrideColor{channel}", color)

            print(f"rgb color applied: {rgb_color_value}")

        elif index_color_mode == 1:
            cmds.setAttr(f"{i}.overrideRGBColors", 0)
            cmds.setAttr(f"{i}.overrideColor", index_color_value)
            print(f"index color applied: {index_color_value}")
            index_color_mode = 0


def close_window(*args):
    cmds.deleteUI("ColorPicker")

# main()