#SingleInstance, force
!+T::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\dump\vid_trim.py"
return
^+A::
run, "C:\Users\Labo Samaha\Desktop\.LabGym"
return

^!+l::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return

; !r::
; run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\resize.py"
; return

!r::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\resizechoose.py"
return

!m::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\markersquick.py"
return

!T::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\trimmultiple.py"
return

^!+A::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return

!+M::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\markers.py"
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
Sleep 450
SplashTextOff
run,"%A_ScriptDir%\labgym.ahk"
return

!f::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\frameoverlay.py"
return

!n::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\renamefolders.py"
return

!a::
run, py "C:\Users\Labo SamahA\Desktop\.LabGym\z_misc_DONOTTOUCH\pythonfiles\addtocss.py"
return