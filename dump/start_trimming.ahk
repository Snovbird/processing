#SingleInstance, force

pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")
run, pyw "%pythonScriptsDir%\initiate_trimming_behavior_collection.pyw"

pidList := ""
; Use WMI to get processes named pythonw.exe or pyw.exe
for process in ComObjGet("winmgmts:").ExecQuery("SELECT ProcessId FROM Win32_Process WHERE Name = 'pythonw.exe'") ; OR Name = 'pyw.exe'")
{
    pidList .= process.ProcessId . "`n"
}
if (pidList = "") {
    run, pyw "%pythonScriptsDir%\trim_loop.py"
} else {
    MsgBox, 64, Info, Trimming script is already running., 1
    
}

SetTitleMatchMode, 2 ; Match a window if the title contains the specified string
if WinExist("DS- ahk_class CabinetWClass") {
    WinActivate, DS- ahk_class CabinetWClass
} else {
    run, explorer.exe "%A_Desktop%\5-clips\DS-"
}

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