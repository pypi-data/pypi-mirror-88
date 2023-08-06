import sys

import shutil
import json
import logging

import PySimpleGUI as sg

from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')

#printsq = sg.Print
#sg.ChangeLookAndFeel('GreenTan')

from . import som_selector

LOG_FMT = (
    "%(asctime)s "
    "%(module)s.%(funcName)s(%(lineno)d) "
    "%(levelname)s %(message)s")

LOGGER = logging.getLogger(__name__)
root_logger = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(fmt=LOG_FMT, datefmt='%m/%d/%Y %H:%M:%S ')
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])

SETTINGS_KEYS_TO_SAVE = [
    '_output_dir_path_', '_data_input_path_', '_data_columns_excluded_',
    '_columns_', '_rows_', '_iterations_', '_grid_type_', '_number_clusters_']

HELP_KEYS_TO_MSG = {
    '_help_workspace_' : 'Directory to save SOM model weights and figures.' 
                         ' If directory exists it will be overwritten.',
    '_help_data_input_' : 'A CSV of the data to self organize. Each column is'
                          ' considered a feature of the data sample unless'
                          ' excluded below.',
    '_help_data_cols_' : 'Comma separated names for columns not to consider'
                         ' as data features for the SOM. For instance an ID'
                         ' column for the data features.',
    '_help_clusters_' : 'The number of clusters used to run a heirarchical'
                        ' clustering algorithm on the completed SOM weights.'
    } 


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas
    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
    # Return a handle which contains a reference to the photo object which
    # must be kept live or else the picture disappears
    return photo


def show_figure(fig, som_model_path):
    figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
    print(figure_x, figure_y, figure_w, figure_h)
    # define the window layout
    layout = [
        [sg.Text('Plot test')],
        [sg.Canvas(size=(figure_w, figure_h), key='canvas')],
        [sg.InputText(key='_save_input_', visible=False, change_submits=True, disabled=True)],
        [sg.SaveAs('Save Model', enable_events=True, 
                   file_types=(("Text Files", "*.txt"),),
                   key='_save_model_path_', target='_save_input_'),
            sg.Cancel(key='_cancel_')]]

    # create the window and show it without the plot
    fig_window = sg.Window(
        'Demo Application - Embedding Matplotlib In PySimpleGUI').Layout(layout).Finalize()


    # add the plot to the window
    fig_photo = draw_figure(fig_window.FindElement('canvas').TKCanvas, fig)

    # show it all again and get buttons
    while True:
        fig_event, fig_values = fig_window.Read()

        print(fig_event)
        if fig_event == '_save_input_':
            # Save the model to their place of choosing
            shutil.copy(som_model_path, fig_values['_save_input_'])
            break
        if fig_event == '_cancel_':
            break
        if event is None:
            break

    fig_window.Close()

#root = Tkinter.Tk()
#defaultbg = root.cget('bg')
#print(defaultbg)

def main():
    validated = False

    menu_def = [['File', ['Load', 'Save', 'Exit',]]]
    
    layout = [
        [sg.Menu(menu_def)],
        [sg.Text('Self Organizing Map Tool', size=(30, 1), font=("Helvetica", 14))],
        [sg.Text('_'  * 100, size=(70, 1))],
        [sg.Text('Workspace:', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputText(do_not_clear=True, key="_output_dir_path_"),
            sg.FolderBrowse(target = '_output_dir_path_'), 
            sg.Help('?', key='_help_workspace_')],
        [sg.Text('_'  * 100, size=(70, 1))],
        [sg.Text('Data Input (CSV):', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputText(do_not_clear=True, key="_data_input_path_"),
            sg.FileBrowse(target = '_data_input_path_'), 
            sg.Help('?', key='_help_data_input_')],
        [sg.Text('Excluded Data Columns:', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputText(do_not_clear=True, key='_data_columns_excluded_'), 
            sg.Sizer(60), sg.Help('?', key='_help_data_cols_')],
#        #################
#        # NOT IMPLEMENTED 
#        #[sg.Text('SOM Parameters:', size=(25, 1), auto_size_text=True, justification='right'),
#        #    sg.InputText(do_not_clear=True, key='_som_params_path_'),
#        #    sg.FileBrowse(target = '_som_params_path_')],
#        #################
        [sg.Text('Number of Grid Columns:', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputText(do_not_clear=True, key='_columns_')],
        [sg.Text('Number of Grid Rows:', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputText(do_not_clear=True, key='_rows_')],
        [sg.Text('SOM Iterations:', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputText(default_text='500', do_not_clear=True, key='_iterations_')],
        [sg.Text('SOM Grid Type:', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputCombo(['hex', 'square'], default_value='hex', key='_grid_type_')],
        [sg.Text('Number of Clusters:', size=(25, 1), auto_size_text=True, justification='right'),
            sg.InputText(do_not_clear=True, key='_number_clusters_'),
            sg.Sizer(60), sg.Help('?', tooltip="details here", key='_help_clusters_')],
        [sg.Text('', text_color=None, background_color=None, size=(70, 1), key='_success_message_')],
        [sg.Submit(), sg.Cancel(key='_cancel_')]]

    window = sg.Window('SOM Selector Tool', auto_size_text=True, default_element_size=(40, 1)).Layout(layout)

    # Event Loop
    while True:
        event, values = window.Read()
        if event is None:
            break
        if event == '_cancel_':
            break
        if event == 'Submit':
            try:
                # TODO: Should try to validate file inputs first
                results = som_selector.execute(values)
                som_fig = results['som_figure']
                som_model_path = results['model_weights_path']
                show_figure(som_fig, som_model_path)
                #print(values)
                pass
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            window.FindElement('_success_message_').Update(text_color="#24b73d")
            window.FindElement('_success_message_').Update('The Model Completed Successfully')
            window.FindElement('_cancel_').Update('Close')
        if event == 'Save':
            save_path = sg.PopupGetFile(
                'Select a file path to save window parameters.',
                default_extension = '.json', file_types = (("JSON Files", "*.json"),),
                no_window = True, save_as = True)
            if save_path != '':
                save_key_dict = {}
                for key, val in values.items():
                    if key in SETTINGS_KEYS_TO_SAVE:
                        save_key_dict[key] = val
                with open(save_path, 'w') as fp:
                    json.dump(save_key_dict, fp)
        if event == 'Load':
            load_path = sg.PopupGetFile(
                'Select the Window Parameters to Load.',
                default_extension = '.json', file_types = (("JSON Files", "*.json"),),
                no_window = True)
            if load_path != '':
                #window.LoadFromDisk(load_path)
                with open(load_path, 'r') as fp:
                    values = json.load(fp)
                    print(values)
                    window.Fill(values)
        if event.startswith("_help"):
            sg.popup_no_titlebar(HELP_KEYS_TO_MSG[event], background_color="#5a6366")
    print("Done.")

if __name__=="__main__":
    main()
