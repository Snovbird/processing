#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

loop {
    WinGet, id, list
    Loop, %id%
    {
        this_id := id%A_Index%
        WinGetTitle, this_title, ahk_id %this_id%
        if InStr(this_title, "(T)")
            WinSet, AlwaysOnTop, ON, ahk_id %this_id%
    }
    Sleep, 500
}