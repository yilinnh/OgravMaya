import importlib
import maya.cmds as cmds
import re

# src = 'l_'
# mir = 'r_'
# ctrl_grp_suffix = '_ctrl'
# mirror_axis = 'x'

main_folder = 'OgravMaya'
sub_folder = 'rigging.AutoMirrorModules'


class CheckBox:
    def __init__(self, module_name):
        self.path = cmds.checkBox(f'Ograv{module_name}', l=get_nice_name(module_name), v=True, cc=self.handle_change_command)
        self.module_name = module_name
        check_box_values.append(self.module_name)

        # self.module = importlib.import_module(f'{main_folder}.{sub_folder}.{module_name}')
    
    def handle_change_command(self, *args):
        state = cmds.checkBox(self.path, q=True, v=True)
        if state:
            check_box_values.append(self.module_name)
        else:
            check_box_values.remove(self.module_name)

    # def run_module(self):
    #     importlib.reload(self.module)
    #     self.module.main()


class Module:
    def __init__(self, module_name):
        self.module = importlib.import_module(f'{main_folder}.{sub_folder}.{module_name}')

    def run_module(self):
        importlib.reload(self.module)
        self.module.main()


def main():
    all_objs = cmds.ls()
    short_name_all_objs = [i.split('|')[-1] for i in all_objs]
    duplicated_name_ctrls = list(set([i for i in short_name_all_objs if short_name_all_objs.count(i) > 1]))
    if duplicated_name_ctrls:
        print("--------------------------------------------------")
        cmds.warning(f"More than one object matches name:")
        for i in duplicated_name_ctrls:
            cmds.warning(i)
        return

    create_ui()


def create_ui():
    global win, win_w, win_h
    win = 'AutoMirror'
    win_w = 300
    win_h = 200

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t=get_nice_name(win), wh=(win_w,win_h), mxb=False, mnb=False, s=False)
    cmds.showWindow(win)

    global ofst_form
    base_form = cmds.formLayout()
    ofst_form = cmds.formLayout(p=base_form)

    cmds.formLayout(base_form, e=True, af=[(ofst_form,'top',10),(ofst_form,'right',10),(ofst_form,'bottom',10),(ofst_form,'left',10)])

    # main_column = cmds.rowColumnLayout(nr=10, p=ofst_form)
    main_column = cmds.columnLayout(p=ofst_form)

    global dropdown
    dropdown = cmds.optionMenu('MirrorAxisOptionMenu', l='Mirror Axis')
    cmds.menuItem(l='x')
    cmds.menuItem(l='y')
    cmds.menuItem(l='z')


    global check_box_values
    check_box_values = []

    global MirrorJoints, MirrorIkHandles, MirrorControls, MirrorConstraints, MirrorNodeConnections, MirroredAttrsCustomization

    CheckBox('MirrorJoints')
    CheckBox('MirrorControls')
    CheckBox('MirrorIkHandles')
    CheckBox('MirrorConstraints')
    CheckBox('MirrorNodeConnections')
    CheckBox('MirroredAttrsCustomization')

    MirrorJoints = Module('MirrorJoints')
    MirrorControls = Module('MirrorControls')
    MirrorIkHandles = Module('MirrorIkHandles')
    MirrorConstraints = Module('MirrorConstraints')
    MirrorNodeConnections = Module('MirrorNodeConnections')
    MirroredAttrsCustomization = Module('MirroredAttrsCustomization')

    cmds.button(l='Apply', c=handle_apply)



def get_nice_name(name):
    return re.sub(r"(?<!^)(?=[A-Z])", " ", name)


def handle_apply(*args):

    global mirror_axis
    mirror_axis = cmds.optionMenu('MirrorAxisOptionMenu', q=True, v=True)

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


def get_attrs():

    return {
        'src': 'l_',
        'mir': 'r_',
        'ctrl_grp_suffix': '_ctrl',
        'mirror_axis': mirror_axis
    }

# main()
