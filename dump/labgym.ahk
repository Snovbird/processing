#SingleInstance, force
place := "FF"

!+T::
; eck if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, This hotkey only works in File Explorer
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                Run, % "py -3.10 ""C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\newtrim.py"" """ fullPath """"
                return
            }
        }
    }
    MsgBox, Could not retrieve folder path
return

^+A::
run, "C:\Users\samahalabo\Desktop\.LabGym"
return
^+z::
run, "C:\Users\samahalabo\Videos"
return
!p::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\extractpng.py"
return
^!+l::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return
!+F::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\trial_formula.py"
return
!r::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\resize.py"
return

!+R::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\filenamereplaceappend.py"
return
!+C::
; eck if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, This hotkey only works in File Explorer
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                Run, % "py -3.10 ""C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\concatenate.py"" """ fullPath """"
                return
            }
        }
    }
    MsgBox, Could not retrieve folder path
return

!n::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\replacefilenames.py"
return
!m::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\markersquick.py"
return

!T::
; eck if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, This hotkey only works in File Explorer
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                Run, % "py -3.10 ""C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\TRIM.py"" """ fullPath """"
                return
            }
        }
    }
    MsgBox, Could not retrieve folder path
return


^!+A::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return

!g::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\convGIF.py"
return

!+M::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\markers.py"
return

#a::
run, cmd.exe /k LabGym
return

#IfWinActive, ahk_exe vlc.exe
; Initialize variables
actionQueue := 0

r::
    actionQueue += 3  ; Add 15 actions to the queue
    
    ; Start the queue processor if it's not already running
    if !IsProcessorRunning {
        SetTimer, ProcessQueue, 50  ; Run every 50ms
        IsProcessorRunning := true
    }
    return

ProcessQueue:
    if (actionQueue <= 0) {
        SetTimer, ProcessQueue, Off  ; Stop the timer when queue is empty
        actionQueue := 0
        IsProcessorRunning := false
        return
    }
    
    ; Your action here
    Send, e
    actionQueue -= 1
    return

; Initialize a global variable to track if the processor is running
IsProcessorRunning := false
#If, 

^!+r::
SplashTextOn,,, rebooting...
Sleep 325
SplashTextOff
run,"%A_ScriptDir%\labgym.ahk"
return

!f::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\frameoverlay.py"
return

!a::
run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\addtopss.py"
return

#IfWinActive, ahk_exe Photoshop.exe
$s::
InputBox, CAGENUMB, Cage, Cage number:
InputBox, thedate, Enter Date, Date formated as MM-DD:
send, ^!s
sleep, 150
SendRaw, cage%CAGENUMB%_06-%thedate%_2048 ; %place%
sleep, 100
send, {Tab}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {p}
sleep, 100
SendInput, {Enter}
sleep, 100
SendInput, {Enter}
sleep, 100
SendInput, {Enter}
sleep, 100

; SendInput, ^{w}
return
$d::
if place = FN
{
    place := "FF"
}
else if place = FF
{
    place := "FN"
}
SplashTextOn,,, %place%
Sleep, 350
SplashTextOff
return
#If, 
#IfWinActive, ahk_exe explorer.exe
!c::
Run, pyw "C:\Users\samahalabo\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\cagename.py"
return
#If