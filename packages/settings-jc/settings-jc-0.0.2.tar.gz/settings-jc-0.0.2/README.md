# settings_jc

Application settings package, where defaults are located 
in a text file.  The location of text file is root of project or 
available from environment variable SETTINGS_JC.
***
Installation<br>
<code>
pip install settings_jc
</code>

Update<br>
<code>
pip install -U settings_jc
</code>

***
## Features
## Documentation

The default default settings are in the form:<br>
setting_name=value<br>

For example, if you wish to save the default value for X then your default settings file would contain
the following:<br>
X=123

Comments are lines starting with #, so an example file may be:<br>
<pre>
# 
# settings.txt
#
# default settings for my application
#
X=123
</pre>

The actual settings are stored in the following folder depending on OS.  The settings are stored in:<br>  
Windows: %appdata%\appname\settings<br>
Unix/Linux: $HOME/appname/settings<br>

The settings file is encrypted with a key derived from the computer's system id.  
This system id should be specific to the execution system.  Please note, it is 
very unlikely you could copy the settings file from one system and use 
on another system.  Since the system id is unique to the system, the encryption key
will be different for each system.

## ToDo
## Bugs/Requests
## License
Copyright Jim Carter, 2020.
Distributed under the terms of the MIT License, settings_jc is free and open source software.
