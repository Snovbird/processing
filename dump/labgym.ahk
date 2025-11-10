#SingleInstance, force

pythonScriptsDir := StrReplace(A_ScriptDir, "\dump", "")

^+P::
Run, py "%pythonScriptsDir%\process_recordings.py" 
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
^!+q::
    run, "%A_ScriptDir%/move_keys.ahk"
Return
!k::
    Run, pyw "%pythonScriptsDir%\add count to folder names.py"
return
#IfWinActive, ahk_exe explorer.exe
!c::
    run, pyw "%pythonScriptsDir%\cagename.py"
return
#if
^+A::
run, explorer.exe "C:\Users\%Username%\Desktop"
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
^!+T:: 
    Run, "%A_ScriptDir%\start_trimming.ahk"
return
^!+l::
    Run "C:\Users\%Username%\AppData\Local\Programs\Microsoft VS Code\Code.exe" "%A_ScriptDir%\labgym.ahk"
return
!+F::
run, pyw "%pythonScriptsDir%\trial_formula.py"
return
; $!r::
; run, pyw "%pythonScriptsDir%\resize.py" ; resize is in dump now
; return
$!s::
    run, pyw "%pythonScriptsDir%\sort_generated_pairs_to_folder.py"
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
!f::
; Check if the active window is File Explorer
    WinGetClass, activeClass, A
    if (activeClass != "CabinetWClass" && activeClass != "ExploreWClass") {
        MsgBox, , TIP, TIP: Focus your recordings folder before pressing 'Alt + F' to start navigating there
        Run, py "%pythonScriptsDir%\frameoverlay.py" 
        return
    }

    ; Use the Explorer COM object to get the actual path
    for window in ComObjCreate("Shell.Application").Windows {
        try {
            if (window.HWND == WinExist("A")) {
                fullPath := window.Document.Folder.Self.Path
                command := "py -3.10 """ pythonScriptsDir "\frameoverlay.py"" """ fullPath """"
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

!a::
run, pyw "%pythonScriptsDir%\addtopss.py"
return

#a::
run, cmd.exe /k LabGym
return
!r::
run, pyw "%pythonScriptsDir%\filenamereplaceappend.py"
return
^!+r::
SplashTextOn,,, rebooting...
Sleep 325
SplashTextOff
reload
return
