#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

LButton::
Send, !{F4}
sleep, 200
Send, {c}
sleep, 200
Send, {Enter}
return
RButton::
Send, !{F4}
sleep, 200
Send, {Right}
sleep, 200
Send, {Enter}
return

LControl::ExitApp