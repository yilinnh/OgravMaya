import maya.cmds as cmds
import re

def main():
    create_ui()
    global symbol_dict, wrapped_symbol_list
    symbol_dict = {'(':')', ')':'(', '[':']', ']':'[', '{':'}', '}':'{'}
    wrapped_symbol_list = ['()', '[]', '{}', '(\)', '[\]', '{\}']

def create_ui():
    global win, win_w, win_h
    win = 'newWindow'
    win_w = 300
    win_h = 230

    if cmds.window(win, ex=True):
        cmds.deleteUI(win)

    cmds.window(win, t='New Window', wh=(win_w,win_h), mxb=False, mnb=False, s=False)
    cmds.showWindow(win)

    global main_form
    base_form = cmds.formLayout()
    main_form = cmds.formLayout(p=base_form)

    cmds.formLayout(base_form, e=True, af=[(main_form,'top',10),(main_form,'right',10),(main_form,'bottom',10),(main_form,'left',10)])

    global input_field
    input_row = one_col_layout()
    input_field = cmds.textField(searchField=True, receiveFocusCommand=handle_receive_focus, textChangedCommand=handle_text_change, enterCommand=handle_apply, aie=True, pht='[Pattern], [Replacement]')

    global pane, match_list, result_list
    pane = cmds.paneLayout(cn='single', p=main_form, w=win_w-18, st=4)

    match_col = cmds.columnLayout(p=pane, adj=True, rs=4)
    cmds.text(l='Matches', p=match_col)
    match_list = cmds.textScrollList(enableKeyboardFocus=False,allowMultiSelection=True, sc=handle_match_sel, p=match_col, w=win_w/8)

    result_col = cmds.columnLayout(p=pane, adj=True, rs=4)
    cmds.text(l='Results', p=result_col)
    result_list = cmds.textScrollList(enableKeyboardFocus=False, allowMultiSelection=True, sc=handle_result_sel,p=result_col, w=win_w/8)

    cmds.formLayout(main_form, e=True, ac=[(pane,'top',0,input_row)])


    # cmds.dockControl(l='Regex Match', area='right', content=win, allowedArea='all', splitLayout='vertical')


def create_row_column_layout(num_of_col, col_width, col_spacing, parent, **kwargs):
    cw = []
    cs = []
    for i in range(num_of_col):
        cw.append((i+1, col_width))
        if i == 0:
            cs.append((i+1, 0))
        else:
            cs.append((i+1, col_spacing))
    return cmds.rowColumnLayout(nc=num_of_col, cw=cw, cs=cs, p=parent, adj=True, **kwargs)

def one_col_layout(**kwargs):
    return create_row_column_layout(1, win_w-20, 0, main_form, **kwargs)

def two_cols_layout(**kwargs):
    return create_row_column_layout(2, win_w/2-12, 4, main_form, **kwargs)

def handle_match_sel(*args):
    selected_items = cmds.textScrollList(match_list, q=True, selectItem=True)
    query_exist_sel(match_list, selected_items)

def handle_result_sel(*args):
    selected_items = cmds.textScrollList(result_list, q=True, selectItem=True)
    query_exist_sel(result_list, selected_items)

def query_exist_sel(list, selected_items):
    all_objs = cmds.ls(dag=True)
    exist_sel = set(selected_items) & set(all_objs)
    if not exist_sel:
        cmds.textScrollList(list, e=True, deselectAll=True)
        return
    cmds.select(exist_sel)


def handle_receive_focus(*args):
    global all_objs
    sel = cmds.ls(sl=True)
    if sel:
        all_objs = sel
    else:
        all_objs = cmds.ls(dag=True)
    
    handle_text_change()


def handle_text_change(*args):
    text = cmds.textField(input_field, q=True, text=True)
    cmds.paneLayout(pane, e=True, cn="single")

    if not text:
        cmds.textScrollList(match_list, e=True, ra=True)
        cmds.textScrollList(result_list, e=True, ra=True)
        return
    
    if text.endswith(','):
        return

    if ', ' in text and not text.startswith(', '):
        global pattern, replacement

        splited_text = text.split(', ')
        pattern = splited_text[0]
        replacement = splited_text[1]

        # if replacement:
            # cmds.paneLayout(pane, e=True, cn="vertical2")

        if not omit_incomplete_input(pattern) or not pattern:
            return

        global matched_names, results

        matched_names = [i for i in all_objs if re.search(pattern, i)]

        cmds.textScrollList(match_list, e=True, ra=True)
        cmds.textScrollList(result_list, e=True, ra=True)

        cmds.textScrollList(match_list, e=True, a=matched_names)

        if not omit_incomplete_input(replacement) or not replacement:
            return

        results = [re.sub(pattern, replacement, i) for i in matched_names]
        results = sort_duplicated_results(results)

        cmds.paneLayout(pane, e=True, cn="vertical2")
        cmds.textScrollList(result_list, e=True, a=results)

    else:
        if not omit_incomplete_input(text):
            return

        matched_names = [i for i in all_objs if re.search(text, i)] 

        cmds.textScrollList(match_list, e=True, ra=True)
        cmds.textScrollList(result_list, e=True, ra=True)
        cmds.textScrollList(match_list, e=True, a=matched_names)


def sort_duplicated_results(result_list):
    counts = {}
    sorted_results = []

    for i in result_list:
        if i not in counts:
            counts[i] = 1 # initialize the first item
            sorted_results.append(f"{i}")
        else:
            if counts[i] == 1:
                sorted_results[sorted_results.index(i)] = f"{i}1"

            counts[i] += 1
            sorted_results.append(f"{i}{counts[i]}")
    
    return sorted_results


def omit_incomplete_input(input_text):
    if input_text.startswith(('*', '+', '?')):
        return

    if input_text.endswith('\\'):
        return 

    if [i for i in wrapped_symbol_list if i in input_text]:
        return

    typed_symbols = set(input_text) & set(symbol_dict)
    for i in typed_symbols:
        if input_text.count(i) != input_text.count(symbol_dict[i]):
            return 

    return True


def handle_apply(*args):
    if not cmds.textField(input_field, q=True, text=True):
        return

    # only apply the replacement to selection
    sel = cmds.ls(sl=True)
    if sel:
        name_dict = {}
        for m,r in zip(matched_names, results):
            name_dict[m] = r
        for i in sel:
            cmds.rename(i, name_dict[i])

    # apply the replacement to all objects
    else:
        for m,r in zip(matched_names, results):
            cmds.rename(m, r)
        
    cmds.textScrollList(result_list, e=True, si=results)
    cmds.select(results)
        
# main()