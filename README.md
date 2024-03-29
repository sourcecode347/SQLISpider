# SQLISpider
A very simple example of 'how the SQLI Spiders work' ...

<img src='screen.jpg' style='width:90%;height:auto;'></img>


Now imagine more advanced spiders searching the web for sqli vulnerabilities and finding them, then automatically running sqlmap and extracting all the data from a server database.

All automated!

I certainly would not give an advanced code that has made possible attacks in the past.

But I can show you an example of how to grow your own and have permanent spiders research the web for vulnerabilities.

To run such code you will need to have the latest version of Firefox and python installed.

Install the following Python libraries via pip.

    pip install selenium
    
    pip install termcolor

    pip install Random-Word

If you are on Windows, this utility library will also be needed for the terminal colors to work.

    pip install colorama

To set browser as headless add the -h parameter:
    
    python spider.py -h
    
To include forms for SQLI Testing add -f parameter:
    
    python spider.py -h -f

if you want to printing not detected SQLi Links add the -n parameter:

    python spider.py -h -f -n

    python spider.py -h -n

if you are in windows system add the -w parameter:

    python spider.py -w

Also to test firefox automatically, you will need to download the geckodriver and set its path to the executable_path variable in row <code>6</code> of the code.

This Repository is educational purposes and we are not responsible for how you use it.

Tested in Ubuntu 22.04 and works fine!

if you have troubles with snap versions of firefox profile execute these commands:

    sudo snap remove firefox

    sudo add-apt-repository ppa:mozillateam/ppa
    
    echo '
    Package: *
    Pin: release o=LP-PPA-mozillateam
    Pin-Priority: 1001
    ' | sudo tee /etc/apt/preferences.d/mozilla-firefox

    echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
        
    sudo apt install firefox

Be well everyone and always have positive energy.
