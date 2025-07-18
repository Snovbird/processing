﻿#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#IfWinActive, ahk_exe explorer.exe
$c::
    send, ^+{c} ; Send "Copy as path" command
    send, {Rightq}
    pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")
    Run, pyw "%pythonScriptsDir%\collection.py"
    return
#IfWinActive

$q::ExitApp