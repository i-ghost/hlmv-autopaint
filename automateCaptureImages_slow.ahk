#NoEnv
#WinActivateForce

FileSelectFile, vmtfile, 1, , Select RED VMT file, VMT files (*.vmt)
if ErrorLevel
 ExitApp
FileSelectFile, vmtfileblu, 1, , Select BLU VMT file, VMT files (*.vmt)
if ErrorLevel
 ExitApp
FileRead, vmtoriginal, %vmtfile%
if ErrorLevel 
{
  MsgBox, Failed to read RED VMT contents, terminating.
  ExitApp
}
FileRead, vmtoriginalblu, %vmtfileblu%
if ErrorLevel 
{
  MsgBox, Failed to read BLU VMT contents, terminating.
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
 Sleep, 2000
	Send !{PrintScreen}
 Sleep, 500
	
	WinActivate, Untitled-
 Sleep, 1000
	Send ^v
 Sleep, 1500
}

TakeImage("230 230 230")
TakeImage("216 190 216")
TakeImage("197 175 145")
TakeImage("126 126 126")
TakeImage("20 20 20")
TakeImage("105 77 58")
TakeImage("124 108 87")
TakeImage("165 117 69")
TakeImage("231 181 59")
TakeImage("240 230 140")
TakeImage("233 150 122")
TakeImage("207 115 54")
TakeImage("255 105 180")
TakeImage("125 64 113")
TakeImage("81 56 74")
TakeImage("47 79 79")
TakeImage("50 205 50")
TakeImage("114 158 66")
TakeImage("128 128 0")
TakeImage("66 79 59")
; new mint paints
TakeImage("188 221 179")
TakeImage("45 45 36")

; team paints, first RED

TakeImage("168 154 140")
TakeImage("59 31 35")
TakeImage("184 56 59")
TakeImage("72 56 56")
TakeImage("128 48 32")
TakeImage("101 71 64")
TakeImage("195 108 45")

; replace RED version with BLU

FileDelete, %vmtfile%
FileAppend, %vmtoriginalblu%, %vmtfile%
Sleep, 500

TakeImage("131 159 163")
TakeImage("24 35 61")
TakeImage("88 133 162")
TakeImage("56 66 72")
TakeImage("37 109 141")
TakeImage("40 57 77")
TakeImage("184 128 53")

; replace with original version

FileDelete, %vmtfile%
FileAppend, %vmtoriginal%, %vmtfile%

; run through one last time for unpainted variant using original vmt

WinActivate, models\
Sleep, 500
Send {F5}
Sleep, 2000
Send !{PrintScreen}
Sleep, 500

WinActivate, Untitled-
Sleep, 1000
Send ^v
Sleep, 1500

MsgBox, Done!