import PySimpleGUI as sg


sg.theme('LightGrey1')
str_of_term = str()
operations = ('+', '-', '*', '/', '**')


def count(count_arr):
    res = 0
    op = count_arr[1]
    if op == '*':
        res = float(count_arr[0]) * float(count_arr[2])
    elif op == '/':
        res = float(count_arr[0]) / float(count_arr[2])
    elif op == '-':
        res = float(count_arr[0]) - float(count_arr[2])
    elif op == '+':
        res = float(count_arr[0]) + float(count_arr[2])
    elif op == '**':
        res = float(count_arr[0]) ** float(count_arr[2])
    if int(res) == res:
        return int(res)
    else:
        return '{:.2f}'.format(res)


def disassembly(dis_array):
    main_index = 0
    while len(dis_array) != 1:
        main_index += 1
        if dis_array[main_index] in operations:
            if len(dis_array) == 3:
                return count(dis_array)
            elif ((array[main_index] == '+' or array[main_index] == '-') and
                  (array[main_index+2] == '-' or array[main_index+2] == '+')) or\
                ((array[main_index] == '*' or array[main_index] == '/' or array[main_index] == '**') and
                 (array[main_index+2] == '+' or array[main_index+2] == '-')) or\
                ((array[main_index] == '*' or array[main_index] == '/' or array[main_index] == '**') and
                 (array[main_index+2] == '*' or array[main_index+2] == '/')):
                res = count(dis_array[main_index-1:main_index+2])
                del dis_array[main_index-1:main_index+2]
                dis_array.insert(0, res)
                main_index -= 3
            elif dis_array[main_index+2] in operations:
                res = disassembly(dis_array[main_index+1:])
                del dis_array[main_index+1:]
                dis_array.insert(main_index + 1, res)
                main_index -= 5
        elif dis_array[main_index] == '(':
            arr_of_st = [main_index]
            index = main_index
            while arr_of_st:
                index += 1
                if dis_array[index] == '(':
                    arr_of_st.append(index)
                elif dis_array[index] == ')':
                    last_st = arr_of_st.pop()
                    res = disassembly(dis_array[last_st + 1:index])
                    del dis_array[last_st:index+1]
                    dis_array.insert(last_st, str(res))
                    index = last_st
            main_index -= 2
    return dis_array


layout = [
    [sg.Output(size=(200, 3), font=("Franklin Gothic Medium", 18), key='_output_')],
    [sg.B('1', border_width=0), sg.B('2', border_width=0), sg.B('3', border_width=0)],
    [sg.B('4', border_width=0), sg.B('5', border_width=0), sg.B('6', border_width=0)],
    [sg.B('7', border_width=0), sg.B('8', border_width=0), sg.B('9', border_width=0)],
    [sg.B('+', border_width=0), sg.B('0', border_width=0), sg.B('-', border_width=0)],
    [sg.B('*', border_width=0), sg.B('/', border_width=0), sg.B('**', border_width=0)],
    [sg.B('⌫', border_width=0), sg.B('C', border_width=0), sg.B('=', border_width=0)],
    [sg.B('(', border_width=0), sg.B(')', border_width=0), sg.B('.', border_width=0)]
]
window = sg.Window('Calculator', layout, size=(260, 550), auto_size_buttons=False,
                   default_button_element_size=(8, 3), background_color='black',
                   return_keyboard_events=True)


while True:
    event = window.read()[0]
    if event in (None, 'Exit', 'Cancel'):
        break
    elif event != '=':
        if event.isdigit():
            print(event, end='')
            str_of_term += event
        elif event in operations:
            if event == '-' and str_of_term[-1] in operations:
                print(event, end='')
                str_of_term += ' ' + event
            else:
                print(' ' + event, end=' ')
                str_of_term += ' ' + event + ' '
        elif event == '.':
            print(event, end='')
            str_of_term += event
        elif event == 'C' or event == 'c':
            window.FindElement('_output_').Update(' '.join(str_of_term.split('\n')[:-1]))
            str_of_term = str()
            num = ''
        elif event == '⌫' or event == 'BackSpace:8':
            if str_of_term[-1] != ' ':
                str_of_term = str_of_term[:-1]
            else:
                str_of_term = str_of_term[:-3]
            window.FindElement('_output_').Update(str_of_term)
        elif event == '(':
            print(event, end=' ')
            str_of_term += event + ' '
        elif event == ')':
            print(' ' + event, end='')
            str_of_term += ' ' + event
    else:
        print(' = ', end='')
        try:
            array = (str_of_term.split('\n')[-1]).split(' ')
            result = disassembly(array)
            print(result)
            str_of_term += ' ' + '=' + ' ' + str(result) + '\n'
        except ZeroDivisionError:
            sg.Popup('Ошибка, нельзя делить на ноль', auto_close=True, auto_close_duration=5)
            window.FindElement('_output_').Update(' '.join(str_of_term.split('\n')[:-1]))
            str_of_term = ' '.join(str_of_term.split('\n')[:-1])
        except IndexError:
            sg.Popup('Ошибка, попробуйте заново', auto_close=True, auto_close_duration=5)
            window.FindElement('_output_').Update(' '.join(str_of_term.split('\n')[:-1]))
            str_of_term = ' '.join(str_of_term.split('\n')[:-1])
