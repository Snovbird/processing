#SingleInstance, force
; Resets collection folder attributes, starts the trimming python loop and rebinds "T" to start trimming process on a selected video in explorer  
pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")

trimLoopRunning := false
; Use WMI to get processes named pythonw.exe and check command line for specific script
for process in ComObjGet("winmgmts:").ExecQuery("SELECT CommandLine FROM Win32_Process WHERE Name = 'pythonw.exe'")
{
    if (InStr(process.CommandLine, "trim_loop.py")) {
        trimLoopRunning := true
        break
    }
}
if (trimLoopRunning = false) {
    run, pyw "%pythonScriptsDir%\initiate_trimming_behavior_collection.pyw"
    ; run, pyw "%pythonScriptsDir%\trim_loop.py"
    ; makes frame overlays for collected intervals, resets the cue variable in data.json and updates the folder count name

} else {
    MsgBox, 64, Info, Trimming script is already running., 1
    run, pyw "%pythonScriptsDir%\initiate_trimming_behavior_collection.pyw"
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
sleep, 100
WinSet, AlwaysOnTop, Toggle, A
sleep, 1000
WinSet, AlwaysOnTop, Toggle, A
Return
Q::
MsgBox, 4, Quit Trimming?, Are you sure you want to quit trimming?
IfMsgBox, Yes
{
    for process in ComObjGet("winmgmts:").ExecQuery("SELECT * FROM Win32_Process WHERE Name = 'pythonw.exe'")
    {
        if (InStr(process.CommandLine, "trim_loop.py")) {
            process.Terminate()
        }
    }
    ExitApp
}
return