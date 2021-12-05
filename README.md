# Beat Saber - PiShock Plugin

## Getting a PiShock API Key
* Login to the site: https://www.pishock.com
* Choose the `PiShock` option
* Click the Person icon ( `Account` ) in the bottom left corner
* Click `Generate API Key` button
* The API key is the value shown, Example: `abcd-1234555678-defg-12345`

## Getting a PiShock Share Code
1. On the PiShock website: 
	1. Create a share code ( or get one from another user ) 
		* Click on the Share icon ( the 3 dots )
		* Click `Generate Share Code`

## Installation
1. Make sure you have Beat Saber installed
1. Install Python using the attached `install_python.ps1`:
	1. Right click
	1. Run with Powershell
1. Setup Mod Assistant
    1. Launch ModAssistant.exe
	1. Click Agree
	1. Install the mod `HTTP Status`
		* If it isn't there, use the ModAssistant to install: `BSIPA`, `BS Utils`, and `websocket-sharp`. 
		* Then you can find the latest version of `HTTP Status` here: https://github.com/opl-/beatsaber-http-status/releases 
		  * Drop the plugin folder in your `Beat Saber` install directory

## Update the `config.json`
1. Update the `Params`:
	* Add the `Username` (it needs to be the one of the person that made the API Key
	* Add the `Name` should be _identical_ or can be something like: _Beat Saber_.

1. Update the `Apikey`:
	* Under `Params:`
	* Update `Apikey:` ( line 7 ) 
	* Add your API Key From the PiShock website (See: *Getting a PiShock API Key*)

1. In the `Miss:` section:
	1. Update the value for `code:` with the Share Code (on line 28)
1. In the `Bomb:` section:
	1. Update the value for `code:` with the Share Code (on line 52)

1. (Optional) Buttplug.io
	* Get the code of a buttplug.io share 
	* Enter it at line 62 (`Hit->Params->code`), 
	* Toggle Active to `true` at line 58.

## Running the Plugin
1. Launch Beat Saber
1. Launch the Plugin:
  1. Hold `shift` and `right click` in the folder that holds the `beatsaber_pishock.py` 
  1. Click on `Open Powershell Window Here`
1. Inside the Powershell window:
	1. Type `python .\beatsaber_pishock.py`
	1. Press `Enter` to launch the plugin

