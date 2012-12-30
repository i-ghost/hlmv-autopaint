#NoEnv
#WinActivateForce

FileSelectFile, vmtfile, 1, , Select RED VMT file, VMT files (*.vmt)
if ErrorLevel
 ExitApp
FileSelectFile, vmtfileblu, 1, , Select BLU VMT file, VMT files (*.vmt)
if ErrorLevel
 ExitApp
 
MsgBox, 4,, Specify additional VMT pair?
IfMsgBox, Yes
{
  FileSelectFile, _vmtfile, 1, , Select additional RED VMT file, VMT files (*.vmt)
  if ErrorLevel
  ExitApp
  FileSelectFile, _vmtfileblu, 1, , Select additional BLU VMT file, VMT files (*.vmt)
  if ErrorLevel
  ExitApp
}
if _vmtfile
 _add = 1

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

if _add
{
FileRead, _vmtoriginal, %_vmtfile%
if ErrorLevel
{
  MsgBox, Failed to read additional RED VMT contents, terminating.
  ExitApp
}
FileRead, _vmtoriginalblu, %_vmtfileblu%
if ErrorLevel 
{
  MsgBox, Failed to read additional BLU VMT contents, terminating.
  ExitApp
}
} 

TakeImage(color)
{
	global vmtfile
	global _vmtfile
	global _add
	
	FileRead, vmt, %vmtfile%
 if ErrorLevel
 {
  MsgBox, Failed to read VMT contents, terminating.
  ExitApp
 }

if _add
{
	FileRead, _vmt, %_vmtfile%
 if ErrorLevel
 {
  MsgBox, Failed to read additional VMT contents, terminating.
  ExitApp
 }
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
	if _add
	{
	_vmt := RegExReplace(_vmt, "color2. ..[0-9]+ [0-9]+ [0-9]+", replacer, _count, 1)
	if _count = 1
	{
		FileDelete, %_vmtfile%
		FileAppend, %_vmt%, %_vmtfile%
	}
	Else
	{	
		MsgBox, Failed to find "$color2" in additional VMT, terminating.
		ExitApp
	}
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
if _add
{
FileDelete, %_vmtfile%
FileAppend, %_vmtoriginalblu%, %_vmtfile%
}
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
if _add
{
FileDelete, %_vmtfile%
FileAppend, %_vmtoriginal%, %_vmtfile%
}

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