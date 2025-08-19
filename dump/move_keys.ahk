#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#SingleInstance, force
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")

#IfWinActive, ahk_exe explorer.exe
$p::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    fullpath := "C:\Users\samahalabo\Desktop\5-clips\PressLeverFNCL"
    command := "py -3.10 """ A_ScriptDir "\move_on_key.py"" """ fullPath """"
    ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
    Run, % command
    return
$c::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    fullpath := "C:\Users\samahalabo\Desktop\5-clips\CheckMagazineFNCL"
    command := "py -3.10 """ A_ScriptDir "\move_on_key.py"" """ fullPath """"
    ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
    Run, % command
    return
$i::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    fullpath := "C:\Users\samahalabo\Desktop\5-clips\InteractionFNCL"
    command := "py -3.10 """ A_ScriptDir "\move_on_key.py"" """ fullPath """"
    ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
    Run, % command
    return
$a::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    fullpath := "C:\Users\samahalabo\Desktop\5-clips\LeverApproach"
    command := "py -3.10 """ A_ScriptDir "\move_on_key.py"" """ fullPath """"
    ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
    Run, % command
    return
$e::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    fullpath := "C:\Users\samahalabo\Desktop\5-clips\EnterMagazine"
    command := "py -3.10 """ A_ScriptDir "\move_on_key.py"" """ fullPath """"
    ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
    Run, % command
    return
$o::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    fullpath := "C:\Users\samahalabo\Desktop\5-clips\OrientFNCL"
    command := "py -3.10 """ A_ScriptDir "\move_on_key.py"" """ fullPath """"
    ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
    Run, % command
    return
; $r::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    fullpath := "C:\Users\samahalabo\Desktop\5-clips\RetractedLeverInteraction"
    command := "py -3.10 """ A_ScriptDir "\move_on_key.py"" """ fullPath """"
    ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
    Run, % command
    return
$r::
    send, ^+{c} ; Send "Copy as path" command
    Run, pyw "%pythonScriptsDir%\remove_one.py"
    return
#IfWinActive

$+Q::ExitApp