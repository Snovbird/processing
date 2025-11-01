import pandas,os,wx
from common.common import *
import timeit

def grid_selector(strings_list, options_list, title='Selection', message='Select options for each item'):
    """
    Create a grid selection window with radio buttons
    
    Args:
        strings_list: List of strings to display in first column
        options_list: List of options to display as column headers
        title: Window title
        message: Message to display at top
        
    Returns:
        dict: Dictionary where keys are strings and values are selected options
    """
    import wx
    
    app = wx.App(False)
    
    # Larger sizing for better visibility
    col_width = 150
    row_height = 45
    header_height = 35
    message_height = 40
    button_height = 40
    padding = 20
    
    # Calculate window size based on content
    num_cols = len(options_list) + 1
    num_rows = len(strings_list) + 1
    
    content_width = num_cols * col_width
    content_height = (num_rows * row_height) + header_height + message_height + button_height
    
    window_width = content_width + (padding * 2)
    window_height = content_height + (padding * 3)
    
    # Create dialog
    dialog = wx.Dialog(None, title=title, size=(window_width, window_height))
    dialog.CenterOnScreen()
    
    # Main panel
    panel = wx.Panel(dialog)
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    
    # Add message at top with larger font
    message_label = wx.StaticText(panel, label=message)
    message_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    message_label.SetFont(message_font)
    main_sizer.Add(message_label, 0, wx.ALL | wx.CENTER, 10)
    
    # Create grid sizer with larger spacing
    grid_sizer = wx.FlexGridSizer(num_rows, num_cols, 8, 8)
    
    # Set minimum column widths
    for col in range(num_cols):
        grid_sizer.AddGrowableCol(col, 1)
    
    # Row 1: Headers
    # Empty cell in top-left
    grid_sizer.Add(wx.StaticText(panel, label=""), 0, wx.ALIGN_CENTER)
    
    # Add option headers with larger font
    header_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    for option in options_list:
        header = wx.StaticText(panel, label=option)
        header.SetFont(header_font)
        grid_sizer.Add(header, 0, wx.ALIGN_CENTER | wx.ALL, 5)
    
    # Store radio buttons in a 2D structure for proper navigation
    radio_grid = []  # [row][col] structure
    radio_groups = {}
    
    # Larger font for string labels
    label_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    
    for row_idx, string_item in enumerate(strings_list):
        # First column: string label with larger font
        label = wx.StaticText(panel, label=string_item)
        label.SetFont(label_font)
        grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        
        # Create row for radio buttons
        radio_row = []
        radio_groups[string_item] = []
        
        for col_idx, option in enumerate(options_list):
            # Each row needs its own radio button group
            # Use a unique ID for each radio button group
            if col_idx == 0:
                # First radio button in each row starts a new group
                radio = wx.RadioButton(panel, style=wx.RB_GROUP, size=(25, 25))
            else:
                # Subsequent radio buttons in the same row
                radio = wx.RadioButton(panel, size=(25, 25))
            
            radio_groups[string_item].append(radio)
            radio_row.append(radio)
            
            # Set first option as default for first row only
            if row_idx == 0 and col_idx == 0:
                radio.SetValue(True)
            
            grid_sizer.Add(radio, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        radio_grid.append(radio_row)
    
    # Add grid to main sizer
    main_sizer.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, padding)
    
    # Buttons with larger size
    button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    ok_button = wx.Button(panel, wx.ID_OK, "OK", size=(80, 35))
    cancel_button = wx.Button(panel, wx.ID_CANCEL, "Cancel", size=(80, 35))
    
    # Larger button font
    button_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    ok_button.SetFont(button_font)
    cancel_button.SetFont(button_font)
    
    button_sizer.Add(ok_button, 0, wx.ALL, 8)
    button_sizer.Add(cancel_button, 0, wx.ALL, 8)
    main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
    
    panel.SetSizer(main_sizer)
    
    # Enhanced keyboard navigation using 2D grid
    def on_key_down(event):
        keycode = event.GetKeyCode()
        focused = wx.Window.FindFocus()
        
        # Find current position in grid
        current_row = -1
        current_col = -1
        
        for row in range(len(radio_grid)):
            for col in range(len(radio_grid[row])):
                if radio_grid[row][col] == focused:
                    current_row = row
                    current_col = col
                    break
            if current_row != -1:
                break
        
        if current_row != -1 and current_col != -1:
            new_row = current_row
            new_col = current_col
            
            if keycode == wx.WXK_DOWN:
                # Move down one row, same column
                new_row = min(current_row + 1, len(radio_grid) - 1)
                
            elif keycode == wx.WXK_UP:
                # Move up one row, same column
                new_row = max(current_row - 1, 0)
                
            elif keycode == wx.WXK_RIGHT:
                # Move right one column, same row
                new_col = min(current_col + 1, len(radio_grid[current_row]) - 1)
                
            elif keycode == wx.WXK_LEFT:
                # Move left one column, same row
                new_col = max(current_col - 1, 0)
                
            elif keycode == wx.WXK_RETURN:
                # Trigger OK button
                ok_button.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED))
                return
            
            # Move focus and select new radio button
            if (new_row != current_row or new_col != current_col):
                new_radio = radio_grid[new_row][new_col]
                new_radio.SetFocus()
                new_radio.SetValue(True)
        
        event.Skip()
    
    # Bind keyboard events
    dialog.Bind(wx.EVT_CHAR_HOOK, on_key_down)
    
    # Set focus to first radio button
    if radio_grid and radio_grid[0]:
        radio_grid[0][0].SetFocus()
    
    # Fit the dialog to its contents
    main_sizer.Fit(dialog)
    dialog.SetMinSize(dialog.GetSize())
    
    # Initialize result dictionary
    result = {}
    
    # Show dialog and process result
    if dialog.ShowModal() == wx.ID_OK:
        # Collect selected options for each string
        for string_item in strings_list:
            selected_option = None
            for i, radio in enumerate(radio_groups[string_item]):
                if radio.GetValue():
                    selected_option = options_list[i]
                    break
            result[string_item] = selected_option
    else:
        # Return empty dict if cancelled
        result = {}
    
    dialog.Destroy()
    app.Destroy()
    return result

# Example usage
strings = ["Item 1", "Item 2", "Item 3"]
options = ["Option A", "Option B"]

selections = grid_selector(
    strings_list=strings,
    options_list=options,
    title="Select Options",
    message="Choose which options apply to each item:"
)

print(selections)
# Output example: {'Item 1': ['Option A', 'Option C'], 'Item 2': ['Option B'], 'Item 3': []}