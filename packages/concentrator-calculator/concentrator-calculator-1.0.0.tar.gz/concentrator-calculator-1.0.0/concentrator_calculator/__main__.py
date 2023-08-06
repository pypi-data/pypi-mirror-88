import PySimpleGUI as sg
import pandas as pd
import pkg_resources
import numpy as np
from concentrator_calculator.time_calculator import calculate_time

data = pkg_resources.resource_filename(__name__, 'data/centrifuge_data.xlsx')

## main function to start the GUI
def main():
    ## collect data needed for gui computation
    gui_data = pd.read_excel(data)

    ## collect concentrator names
    infile = pd.ExcelFile(data)
    concentrator_types = infile.sheet_names
    infile.close()

    ## collect liquids and temperatures
    liquids = gui_data['Liquid'].unique()
    temps = gui_data['Temperature [°C]'].unique()

    ## layout definition
    layout = [
    [sg.Frame(layout = [
    [sg.Radio(type, "TYPE", key = '{}'.format(type)) for type in concentrator_types]],
    title = 'Select the type of concentrator')],
    [sg.Frame(layout = [
    [sg.Radio(liquid, 'LIQUID', key = '{}'.format(liquid)) for liquid in liquids]],
    title = 'Liquid to concentrate')],
    [sg.Frame(layout = [
    [sg.Radio('{} °C'.format(temp), 'TEMP', key = '{}'.format(temp)) for temp in temps]],
    title = 'Select a temperature')],
    [sg.Frame(layout = [
    [sg.Text('Starting volume:'), sg.Spin([i for i in range(1, 501)], size = (4, 1), key = 'STARTING_VOL')],
    [sg.Text('Desired volume:'), sg.Spin([i for i in range(1, 501)], size = (4, 1), key = 'DESIRED_VOL')],
    [sg.Text('', size = (20, 1), key = 'OUTPUT')]],
    title = 'Volume information')]
    ]

    window = sg.Window('Concentrator calculator', layout)

    while True:
        event, values = window.read(timeout = 100)

        ## if x or exit are clicked, close the window
        if event == None or event == 'Exit':
            break

        ## update the output element
        ## seems there is no better way to get the keys than looping through them
        func_params = [key for key in values.keys() if values[key]]

        ## if all parameters are selected show output
        ## and a valid input volume is selected
        ## will be updated if more volume data is available
        try:
            if len(func_params) == 5:
                window.Element('OUTPUT').Update('Estimated time: {}'.format(calculate_time(data, func_params[0], func_params[1], func_params[2], values['STARTING_VOL'], values['DESIRED_VOL'])))
        except np.core._exceptions.UFuncTypeError:
            if len(func_params) == 5:
                window.Element('OUTPUT').Update('Select a valid volume.')

    window.close()

## run if called as a toplevel script
if __name__ == "__main__":
    main()
