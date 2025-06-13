#SingleInstance, force
place := "FN"
!+T::
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\dump\vid_trim.py"
return
^+A::
run, "C:\Users\LaboSamaha\Desktop\.LabGym"
return

^!+l::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return

!r::
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\resize.py"
return

!+R::
send, ^{c}
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\filenamereplaceappend.py"
return

!m::
send, ^{c}
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\markersquick.py"
return

!T::
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\trimmultiple.py"
return

^!+A::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return

!g::
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\convGIF.py"
return

!+M::
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\markers.py"
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
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\frameoverlay.py"
return

!n::
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\renamefolders.py"
return

!a::
run, py "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\addtocss.py"
return

#IfWinActive, ahk_exe Photoshop.exe
$s::
InputBox, userInput, User Input, Cage number:
send, ^!s
sleep, 150
SendRaw, cage%userInput%-2048%place%
sleep, 100
send, {Tab}
sleep, 100
SendInput, {p}cage7-2048FF
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
SendInput, ^{s}
SendInput, ^{w}
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
SendInput, ^{c}
Run, pyw "C:\Users\LaboSamaha\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\cagename.py"
return