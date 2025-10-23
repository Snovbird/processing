#SingleInstance, force

pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")
run, pyw "%pythonScriptsDir%\initiate_trimming_behavior_collection.py"

run, pyw "%pythonScriptsDir%\trim_loop.py"
run, explorer.exe "%A_Desktop%\5-clips\collected DS-"

#IfWinActive, ahk_exe explorer.exe
T::
send, ^+{c} ; Send "Copy as path" command
run, pyw "%pythonScriptsDir%\trim_collect.py"
Return
Q::
MsgBox, 4, Quit Trimming?, Are you sure you want to quit trimming?
IfMsgBox, Yes
{
    ExitApp
}
return