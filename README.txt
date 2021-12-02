0: Make sure you have Beat Saber installed
1: Install Python using the attached install_python.ps1, right clicking and running with Powershell
2: Open ModAssistant.exe and agree, then install the mod HTTP Status ( If it isn't there, use the ModAssistant to install BSIPA, then BS Utils and websocket-sharp. \
	You can find the latest version of HTTP Status here: https://github.com/opl-/beatsaber-http-status/releases, drop the plugin folder in your beatsaber install directory )
3: In the config.json ( line 7 ) add your PiShock API Key ( Can be found on the PiShock website, under Account then API Key )
4: Create a share code ( or get one ) by clicking on the share icon ( the 3 dots ) on the website and then Generate Share Code
5: Enter that code both at line 28 and 52, under Miss and Bomb then Params
6: At the top, under Params, add your Username (it needs to be the one of the person that made the API Key, Name should be identical or can be something like Beat Saber.
7: Optionally, get the code of a buttplug.io share and enter it at line 62, and toggle Active to true at line 58.
8: Launch Beat Saber
9: Hold shift and right click in the folder that holds the beatsaber_pishock.py then click on Open Powershell Window Here
10: Enter python .\beatsaber_pishock.py
11: DONE!