#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#SingleInstance, force
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")

; start the script that processes the clips (trimmer)
run, py "%pythonScriptsDir%\trim_loop.py"


#IfWinActive, ahk_exe explorer.exe
$c::
F7::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    
    Run, pyw "%pythonScriptsDir%\collection.py"
    return

$t::
vk6B:: ; Numpad "+"
    send, ^+{c} ; Send "Copy as path" command
    ; send, {Enter}
    send, {Right}
    Run, pyw "%pythonScriptsDir%\trim_collect.py"
    return
$n::
    send, ^+{c} ; Send "Copy as path" command
    send, {Right}
    Run, pyw "%pythonScriptsDir%\sort_name.py"
    return

$m::
    send, ^+{c} ; Send "Copy as path" command
    Run, pyw "%pythonScriptsDir%\remove_one.py"
    return
#IfWinActive

$q::ExitApp