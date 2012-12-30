#NoEnv
#WinActivateForce

FileSelectFile, vmtfile, 1, , Select RED VMT file, VMT files (*.vmt)
if ErrorLevel
 ExitApp
FileRead, vmtoriginal, %vmtfile%
if ErrorLevel 
{
  MsgBox, Failed to read RED VMT contents, terminating.
  ExitApp
}

TakeImage(color)
{
	global vmtfile
 
	FileRead, vmt, %vmtfile%
 if ErrorLevel
 {
  MsgBox, Failed to read VMT contents, terminating.
  ExitApp
 }
  
	replacer = color2" "{%color%
	vmt := RegExReplace(vmt, "color2. ..[0-9]+ [0-9]+ [0-9]+", replacer, count, 1)
	If count = 1
	{
		FileDelete, %vmtfile%
		FileAppend, %vmt%, %vmtfile%
	}
	Else
	{	
		MsgBox, Failed to find "$color2", terminating.
		ExitApp
	}
 

	WinActivate, models\
 Sleep, 500
	Send {F5}
 Sleep, 1000
	Send !{PrintScreen}
 Sleep, 500
	
	WinActivate, Untitled-
 Sleep, 1000
	Send ^v
 Sleep, 1500
}

; new mint paints
TakeImage("188 221 179")
TakeImage("45 45 36")

; replace with original version

FileDelete, %vmtfile%
FileAppend, %vmtoriginal%, %vmtfile%

; run through one last time for unpainted variant
WinActivate, models\
Sleep, 500
Send {F5}
Sleep, 1000
Send !{PrintScreen}
Sleep, 500

WinActivate, Untitled-
Sleep, 1000
Send ^v
Sleep, 1500

MsgBox, Done!