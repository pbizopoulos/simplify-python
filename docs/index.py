from difflib import unified_diff
from js import document
from os import listdir
from pyodide.ffi.wrappers import add_event_listener
from source_code_simplifier import source_code_simplifier
import io


def main():
    for input_file_name in sorted(listdir('.')):
        option = document.createElement('option')
        option.value = input_file_name
        option.innerHTML = input_file_name
        document.getElementById('input-select').appendChild(option)
    on_keyup_input_textarea(None)
    on_select_input(None)
    on_select_input_simplified_difference(None)
    add_event_listener(document.getElementById('input-textarea'), 'keyup', on_keyup_input_textarea)
    add_event_listener(document.getElementById('input-select'), 'change', on_select_input)
    add_event_listener(document.getElementById('difference-simplified-select'), 'change', on_select_input_simplified_difference)


def on_keyup_input_textarea(_):
    document.getElementById('input-textarea').style.height = '1px'
    document.getElementById('input-textarea').style.height = f'{document.getElementById("input-textarea").scrollHeight}px'
    input_ = document.getElementById('input-textarea').value
    reader = io.BufferedReader(io.BytesIO(input_.encode('utf-8')))
    wrapper = io.TextIOWrapper(reader)
    try:
        simplified = source_code_simplifier(wrapper)
        difference_line_list = list(unified_diff(input_.splitlines(), simplified.splitlines(), n=1000))[3:]
        difference_styled_line_list = []
        for difference_line in difference_line_list:
            if difference_line.startswith('+'):
                difference_styled_line_list.append(f'<span style="color:green;">{difference_line}</span>')
            elif difference_line.startswith('-'):
                difference_styled_line_list.append(f'<span style="color:red;">{difference_line}</span>')
            else:
                difference_styled_line_list.append(difference_line)
        document.getElementById('difference-pre').innerHTML = '\n'.join(difference_styled_line_list)
        document.getElementById('simplified-pre').innerHTML = simplified
    except Exception as exception:
        document.getElementById('difference-pre').innerHTML = exception


def on_select_input(_):
    with open(document.getElementById('input-select').value) as file:
        document.getElementById('input-textarea').value = file.read()[:-1]
    document.getElementById('difference-pre').innerHTML = ''
    document.getElementById('simplified-pre').innerHTML = ''
    on_keyup_input_textarea(_)


def on_select_input_simplified_difference(_):
    if document.getElementById('difference-simplified-select').value == 'difference':
        document.getElementById('difference-pre').hidden = False
        document.getElementById('simplified-pre').hidden = True
    elif document.getElementById('difference-simplified-select').value == 'simplified':
        document.getElementById('difference-pre').hidden = True
        document.getElementById('simplified-pre').hidden = False


if __name__ == '__main__':
    main()
