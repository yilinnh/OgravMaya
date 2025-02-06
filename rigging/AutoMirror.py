import importlib
import maya.cmds as cmds
import re

# src = 'l_'
# mir = 'r_'
# ctrl_suffix = '_ctrl'
# mirror_axis = 'x'

main_folder = 'OgravMaya'
sub_folder = 'rigging.AutoMirrorModules'


class CheckBox:
    def __init__(self, module_name):
        self.path = cmds.checkBox(f'Ograv{module_name}', l=get_nice_name(module_name), v=True, cc=self.handle_change_command)
        self.module_name = module_name
        check_box_values.append(self.module_name)
    
    def handle_change_command(self, *args):
        state = cmds.checkBox(self.path, q=True, v=True)
        if state:
            check_box_values.append(self.module_name)
        else:
            check_box_values.remove(self.module_name)


class Module:
    def __init__(self, module_name):
        self.module = importlib.import_module(f'{main_folder}.{sub_folder}.{module_name}')

    def run_module(self):
        importlib.reload(self.module)
        self.module.main()


def main():

    create_ui()

    all_objs = cmds.ls()
    short_name_all_objs = [i.split('|')[-1] for i in all_objs]
    duplicated_names = list(set([i for i in short_name_all_objs if short_name_all_objs.count(i) > 1]))
    if duplicated_names:
        print("--------------------------------------------------")
        print(f"More than one object matches name:")
        for i in duplicated_names:
            print(i)
        return


def create_ui():
    global win, win_w, win_h
    win = 'AutoMirror'
    win_w = 300
    win_h = 270

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t='Auto Mirror', wh=(win_w,win_h), mxb=False, mnb=False, s=False)
    cmds.showWindow(win)

    global ofst_form
    base_form = cmds.formLayout()
    ofst_form = cmds.formLayout(p=base_form)

    cmds.formLayout(base_form, e=True, af=[(ofst_form,'top',10),(ofst_form,'right',10),(ofst_form,'bottom',10),(ofst_form,'left',10)])

    # main_column = cmds.rowColumnLayout(nr=10, p=ofst_form)

    mirror_axis_form = cmds.formLayout(p=ofst_form)
    global mirror_axis_menu
    mirror_axis_menu = cmds.optionMenu('MirrorAxisOptionMenu', l='Mirror Axis')
    cmds.menuItem(l='x')
    cmds.menuItem(l='y')
    cmds.menuItem(l='z')


    side_menu_form = cmds.formLayout(p=ofst_form, w=win_w-25)
    global src_side_menu, mir_side_menu, src_l_item, src_r_item, mir_l_item, mir_r_item
    src_side_menu = cmds.optionMenu('src_side', l='From')
    src_l_item = cmds.menuItem(l='l_')
    src_r_item = cmds.menuItem(l='r_')
    mir_side_menu = cmds.optionMenu('mir_side', l='To')
    mir_l_item = cmds.menuItem(l='r_')
    mir_r_item = cmds.menuItem(l='l_')

    global captilized_check
    captilized_check = cmds.checkBox(l='Capitalized', p=side_menu_form, cc=capitalize_side_prefix)
    # two_cols_form(side_menu_form, src_side_menu, mir_side_menu)
    # cmds.formLayout(side_menu_form, e=True, af=[(src_side_menu,'left',0)], ap=[(src_side_menu,'right',0,48), (mir_side_menu,'left',0,52)])
    cmds.formLayout(side_menu_form, edit=True, af=[(src_side_menu,'left',0), (captilized_check,'right',0)], ap=[(src_side_menu,'right',0,33), (mir_side_menu,'left',0,36), (mir_side_menu,'right',0,63), (captilized_check,'left',0,68)])

    ### declare the attrs for other modules
    global mirror_axis, src_side, mir_side
    mirror_axis = cmds.optionMenu(mirror_axis_menu, q=True, v=True)
    src_side = cmds.optionMenu(src_side_menu, q=True, v=True)
    mir_side = cmds.optionMenu(mir_side_menu, q=True, v=True)


    global check_box_values
    check_box_values = []

    global MirrorJoints, MirrorIkHandles, MirrorControls, MirrorConstraints, MirrorNodeConnections, MirroredAttrsCustomization

    check_box_form = cmds.formLayout(p=ofst_form)
    check_box_column = cmds.columnLayout()

    CheckBox('MirrorJoints')
    CheckBox('MirrorControls')
    CheckBox('MirrorIkHandles')
    CheckBox('MirrorConstraints')
    CheckBox('MirrorNodeConnections')
    CheckBox('MirroredAttrsCustomization')

    footer_hr = cmds.separator(st='single', p=ofst_form, w=win_w-20)

    footer_form = cmds.formLayout(p=ofst_form)
    apply_btn = cmds.button(l='Apply', c=handle_apply)
    close_btn = cmds.button(l='Close', c=handle_close)
    two_cols_form(footer_form, apply_btn, close_btn)

    cmds.formLayout(ofst_form, e=True, 
                    af=[(mirror_axis_form,'top',5),
                        (mirror_axis_form,'left',5),
                        (side_menu_form,'left',5),
                        (check_box_form,'left',10),
                        (footer_form,'bottom',0), 
                        (footer_form,'left',0), 
                        (footer_form,'right',0)
                    ],
                    ac=[(side_menu_form,'top',10,mirror_axis_form),
                        (check_box_form,'top',15,side_menu_form),
                        (footer_hr,'bottom',10,footer_form)
                    ])


### column form templates
def one_col_form(form, col):
    cmds.formLayout(form, e=True, af=[(col,'left',0), (col,'right',0)])

def two_cols_form(form, l_col, r_col):
    cmds.formLayout(form, e=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,49), (r_col,'left',0,51)])

def three_cols_form(form, l_col, m_col, r_col):
    cmds.formLayout(form, edit=True, af=[(l_col,'left',0), (r_col,'right',0)], ap=[(l_col,'right',0,33), (m_col,'left',0,34), (m_col,'right',0,66), (r_col,'left',0,67)])


### add space before caplitized character
def get_nice_name(name):
    return re.sub(r"(?<!^)(?=[A-Z])", " ", name)


def capitalize_side_prefix(*args):
    check = cmds.checkBox(captilized_check, q=True, v=True)
    item_list = [src_l_item, src_r_item, mir_l_item, mir_r_item]
    if check:
        for i in item_list:
            lable = cmds.menuItem(i, q=True, l=True)
            cmds.menuItem(i, e=True, l=lable.upper())
    else:
        for i in item_list:
            lable = cmds.menuItem(i, q=True, l=True)
            cmds.menuItem(i, e=True, l=lable.lower())


def handle_apply(*args):

    global mirror_axis, src_side, mir_side
    mirror_axis = cmds.optionMenu(mirror_axis_menu, q=True, v=True)
    src_side = cmds.optionMenu(src_side_menu, q=True, v=True)
    mir_side = cmds.optionMenu(mir_side_menu, q=True, v=True)

    MirrorJoints = Module('MirrorJoints')
    MirrorControls = Module('MirrorControls')
    MirrorIkHandles = Module('MirrorIkHandles')
    MirrorConstraints = Module('MirrorConstraints')
    MirrorNodeConnections = Module('MirrorNodeConnections')
    MirroredAttrsCustomization = Module('MirroredAttrsCustomization')

    ordered_execution_dict = {
        'MirrorJoints': MirrorJoints,
        'MirrorControls': MirrorControls,
        'MirrorIkHandles': MirrorIkHandles,
        'MirrorConstraints': MirrorConstraints,
        'MirrorNodeConnections': MirrorNodeConnections,
        'MirroredAttrsCustomization': MirroredAttrsCustomization
        }

    global check_box_values
    check_box_values = [i for i in ordered_execution_dict if i in check_box_values]
    if check_box_values:
        for i in check_box_values:
            ordered_execution_dict[i].run_module()

    # print(check_box_values)


def handle_close(*args):
    cmds.deleteUI(win)


def get_attrs():

    return {
        'src': src_side,
        'mir': mir_side,
        'ctrl_suffix': '_ctrl',
        'mirror_axis': mirror_axis
    }

# main()
