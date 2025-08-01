#SingleInstance, force
place := "FF"

; The Haystack is A_ScriptDir, the Needle is "\dump".
; Since we want to remove it, the ReplaceText is an empty string "".
pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")

; Now, pythonScriptsDir will hold "c:\Users\%Username%\Desktop\.LabGym\misc\pythonfiles"

^+P::
; Check if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, , TIP, TIP: Focus your recordings folder before pressing 'Ctrl + Shift + P' to start navigating there
        Run, py "%pythonScriptsDir%\process_recordings.py" 
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                command := "py -3.10 """ pythonScriptsDir "\process_recordings.py"" """ fullPath """"
                ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
                Run, % command
                return
            }
        }
    }
    ; MsgBox, 16, Error, Could not retrieve the folder path from File Explorer.
return

!+T::
; Check if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, ,TIP, TIP: Focus your recordings folder before pressing 'Ctrl + Shift + P' to start navigating there
        Run, py "%pythonScriptsDir%\newtrim.py" 
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                command := "py -3.10 """ pythonScriptsDir "\newtrim.py"" """ fullPath """"
                ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
                Run, % command
                return
            }
        }
    }
    ; MsgBox, 16, Error, Could not retrieve the folder path from File Explorer.
return

^+A::
run, "C:\Users\%Username%\Desktop"
return
^+z::
run, "C:\Users\%Username%\Videos"
return
!p::
; Check if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, ,TIP, TIP: Focus your recordings folder before pressing 'Ctrl + Shift + P' to start navigating there
        Run, py "%pythonScriptsDir%\extractpng.py" 
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                command := "py -3.10 """ pythonScriptsDir "\extractpng.py"" """ fullPath """"
                ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
                Run, % command
                return
            }
        }
    }
    ; MsgBox, 16, Error, Could not retrieve the folder path from File Explorer.
return

^!+l::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return
!+F::
run, pyw "%pythonScriptsDir%\trial_formula.py"
return
$!r::
run, pyw "%pythonScriptsDir%\resize.py"
return
$!s::
run,pyw "%pythonScriptsDir%\sort_generated_pairs_to_folder.py"
return
!+C::
; Check if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, ,TIP, TIP: Focus your recordings folder before pressing 'Ctrl + Shift + P' to start navigating there
        Run, py "%pythonScriptsDir%\concatenate.py" 
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                command := "py -3.10 """ pythonScriptsDir "\concatenate.py"" """ fullPath """"
                ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
                Run, % command
                return
            }
        }
    }
    ; MsgBox, 16, Error, Could not retrieve the folder path from File Explorer.
return

!n::
run, pyw "%pythonScriptsDir%\rename_files.py"
return
!m::
; Check if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, ,TIP, TIP: Focus your recordings folder before pressing 'Ctrl + Shift + P' to start navigating there
        Run, py "%pythonScriptsDir%\markersquick.py" 
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                command := "py -3.10 """ pythonScriptsDir "\markersquick.py"" """ fullPath """"
                ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
                Run, % command
                return
            }
        }
    }
    ; MsgBox, 16, Error, Could not retrieve the folder path from File Explorer.
return

!T::
; Check if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, , TIP, TIP: Focus your recordings folder before pressing 'Ctrl + Shift + P' to start navigating there
        Run, py "%pythonScriptsDir%\trim.py" 
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                command := "py -3.10 """ pythonScriptsDir "\trim.py"" """ fullPath """"
                ; MsgBox, For debugging, the command is:`n%command% ; <-- UNCOMMENT THIS LINE TO DEBUG
                Run, % command
                return
            }
        }
    }
    ; MsgBox, 16, Error, Could not retrieve the folder path from File Explorer.
return

^!+A::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return

!g::
run, pyw "%pythonScriptsDir%\convGIF.py"
return

!+M::
run, pyw "%pythonScriptsDir%\markers.py"
return

#a::
run, cmd.exe /k LabGym
return

; #IfWinActive, ahk_exe vlc.exe
; Initialize variables
; actionQueue := 0

; r::
;     actionQueue += 3  ; Add 15 actions to the queue
    
;     ; Start the queue processor if it's not already running
;     if !IsProcessorRunning {
;         SetTimer, ProcessQueue, 50  ; Run every 50ms
;         IsProcessorRunning := true
;     }
;     return

; ProcessQueue:
;     if (actionQueue <= 0) {
;         SetTimer, ProcessQueue, Off  ; Stop the timer when queue is empty
;         actionQueue := 0
;         IsProcessorRunning := false
;         return
;     }
    
;     ; Your action here
;     Send, e
;     actionQueue -= 1
;     return

; ; Initialize a global variable to track if the processor is running
; IsProcessorRunning := false
; #If, 

^!+r::
SplashTextOn,,, rebooting...
Sleep 325
SplashTextOff
run,"%A_ScriptDir%\labgym.ahk"
return

$!f::
run, pyw "%pythonScriptsDir%\frameoverlay.py"
return

!a::
run, pyw "%pythonScriptsDir%\addtopss.py"
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
Run, pyw "%pythonScriptsDir%\cagename.py"
return
!+R::
run, pyw "%pythonScriptsDir%\filenamereplaceappend.py"
return

^!+c::
Run, "%A_ScriptDir%\collection.ahk"
return
#If