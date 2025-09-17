import pandas, wx,os
def fit_columns(worksheet):
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width

def custom_dialog(msg,title='',op1="yes",op2="No") -> str | None:

    class custom_dialog(wx.Dialog):
        def __init__(self, parent, title, message, option1=op1, option2=op2):
            super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE)
            vbox = wx.BoxSizer(wx.VERTICAL)
            message_label = wx.StaticText(self, label=message, style=wx.ALIGN_CENTER)
            vbox.Add(message_label, 1, wx.ALL | wx.EXPAND, 10)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            
            self.option1_button = wx.Button(self, label=option1)
            self.option1_button.Bind(wx.EVT_BUTTON, self.on_button1)
            hbox.Add(self.option1_button, 1, wx.ALL | wx.EXPAND, 5)
        
            self.option2_button = wx.Button(self, label=option2)
            self.option2_button.Bind(wx.EVT_BUTTON, self.on_button2)

            hbox.Add(self.option2_button, 1, wx.ALL | wx.EXPAND, 5)
            vbox.Add(hbox, 0, wx.ALL | wx.EXPAND, 10)
            self.SetSizer(vbox)
            self.Centre()
            self.result = None

        def on_button1(self, event):
            self.result = self.option1_button.GetLabel()  # Store the button label as the result
            self.EndModal(wx.ID_OK)  # Close the dialog with OK status

        def on_button2(self, event):
            self.result = self.option2_button.GetLabel()  # Store the button label as the result
            self.EndModal(wx.ID_CANCEL)  # Close the dialog with Cancel status
    
    app = wx.App()
    dialog = custom_dialog(None, title=title, message=msg, option1=f'{op1}', option2=f'{op2}')
    
    if dialog.ShowModal() == wx.ID_OK:
        dialog.Destroy()
        return dialog.result
    else:
        dialog.Destroy()
        return dialog.result

def folder_explorer(title:str) -> str|None:
    app = wx.App(False)
    with wx.DirDialog(None, title,style=wx.DD_DEFAULT_STYLE) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            folder_path = dlg.GetPath()
            return folder_path

def file_explorer(title:str,xlsx_only = False) -> list[str]|None:
    app = wx.App(False)
    if xlsx_only:
        files = "Excel files (*.xlsx)|*.xlsx"
    else:
        files = "Any files (*.*)|*.*)"
    with wx.FileDialog(None,message=title,wildcard=files,style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as file_dialog:
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return []
        video_paths = file_dialog.GetPaths()
        return video_paths

def msgbox(msg:str,title:str=' '):
    app = wx.App(False)
    wx.MessageBox(f"{msg}", f"{title}", wx.OK | wx.ICON_INFORMATION)

def error(msg:str,title:str="ERROR"):
    app = wx.App(False)
    wx.MessageBox(f"Error: {msg}", f"{title}", wx.OK | wx.ICON_ERROR)

def dropdown(choices: list[str], title='') -> str:
    """
    Args:
    choices: list of string (options) to display in the dropdown
    title: Title in the top left of the window
    icon_name:  **`star`**, **`check`**
    """

    app = wx.GetApp()

    dialog = wx.Dialog(None, title=title, size=(315, 150))

    dialog.CenterOnScreen()
    
    panel = wx.Panel(dialog)
    dropdown_ctrl = wx.Choice(panel, choices=choices, pos=(50, 20), size=(200, -1))
    dropdown_ctrl.SetSelection(0)
    
    selected_item = [None]
    
    button_width = 70
    button_spacing = 10
    total_button_width = (button_width * 2) + button_spacing
    start_x = (300 - total_button_width) // 2
    
    ok_button = wx.Button(panel, label="OK", pos=(start_x, 70), size=(button_width, 30))
    cancel_button = wx.Button(panel, label="Cancel", pos=(start_x + button_width + button_spacing, 70), size=(button_width, 30))
    
    def on_key_press(event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            selected_item[0] = dropdown_ctrl.GetString(dropdown_ctrl.GetSelection())
            dialog.EndModal(wx.ID_OK)
        else:
            event.Skip()
    
    def on_ok(event):
        selected_item[0] = dropdown_ctrl.GetString(dropdown_ctrl.GetSelection())
        dialog.EndModal(wx.ID_OK)
    
    def on_cancel(event):
        selected_item[0] = None
        dialog.EndModal(wx.ID_CANCEL)
    
    dialog.Bind(wx.EVT_CHAR_HOOK, on_key_press)
    ok_button.Bind(wx.EVT_BUTTON, on_ok)
    cancel_button.Bind(wx.EVT_BUTTON, on_cancel)
    
    # Always use ShowModal for dialogs
    dialog.ShowModal()
    dialog.Destroy()
    
    return selected_item[0]

def list_files(dir:str) -> list[str]:
    """
    files names (ex: ['apples.mp4', 'banana.mp4'])
    """
    if os.path.isdir(dir):
        return [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]

def list_folders(dir:str) -> list[str]:
    """
    folder names (ex: ['apples', 'banana'])
    """
    if os.path.isdir(dir):
        return [folder for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]

def list_filespaths(dir:str) -> list[str]:
    """
    returns: the FULL path of files in a directory

    ex: `C:/users/me/apples.mp4, C:/users/me/banana.mp4`
    """
    return [os.path.join(dir, file) for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]

def list_folderspaths(dir:str) -> list[str]:
    """
    returns: the FULL path of folders in a directory

    ex: `C:/users/me/apples/, C:/users/me/banana/`
    """
    return [os.path.join(dir, folder) for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]

def checkbox_dialog(options:list[str]|set,msg:str="Choose options",title:str="Selections") -> list[str]:

    app = wx.App(False)
    if isinstance(options,set):
        options = list(options)
    dialog1=wx.MultiChoiceDialog(None,message=msg,caption=title,choices=options)

    if dialog1.ShowModal()==wx.ID_OK:
        indexes:list[int] = dialog1.GetSelections() # returns indexes such as [0,1]
        return [options[index] for index in indexes]

