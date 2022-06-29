# Sphero RVR

### Hardware

- Sphero RVR (pronounced rover): https://sphero.com/collections/all/products/rvr
  Includes:
  - Sphero Robot
  - Battery Pack
  - USB to USB-C cable for charging battery

- Raspberry Pi 3 B+
  NEEDS:
  - micro SD card (we have been using 32GB card)
  - micro USB power cable
  - HDMI (regular size) monitor cable (or HDMI<=>HDMI with converter)
  - Monitor
  - Mouse
  - USB (regular) to micro USB for power from RVR to RPi (short one)

- Raspberry Pi 4
  NEEDS:
  - micro SD card (we have been using 32GB card)
  - USB-C power cable
  - micro HDMI monitor cable (or HDMI<=>HDMI with converter)
  - Monitor
  - Mouse
  - USB (regular) to USB-C for power from RVR to Rpi (short one)

- Female-to-Female cable (relatively long) 3x1 to 3x1 RVR-to-Pi for UART

- Pi Camera v2.1 (with cable)
  NEEDS:
  - Camera Case
  - Mount or stand to place on RVR


## July 11, 2021

Received a new Sphero RVR and Raspberry Pi Model 4 with 4GB RAM. Charged the battery over night. This is the journey of set-up ...

1. Charge RVR battery (takes several hours)
2. Update the firmware on the RVR via iPhone app.
  On iPhone:
  - installed Sphero EDU app
  - Home User
  - Unable to login to app using my Sphero account (created and logged into Sphero online using lars1050@umn.edu, mns). Proceeded without login.
  - Chose "Drive" option and connected to RV-D55B. Firmware update.
3. Etch Raspberry Pi OS onto SD card (destroys all content on the card).
  - Raspberry Pi Imager https://www.raspberrypi.org/software/
  - SD card reader in PC, open Pi Imager, choose Raspberry Pi OS (32-bit) recommended OS, choose the SD card, write. The OS is a modified version of Debian (linux), sometimes referred to as Raspian.

### SD Card loaded with OS. Getting it set up...

> When it started, stated that it was resizing and rebooted. Then it rebootted and opened with a setup screen.

- Setting location
- Asking for a new password. I typed in the default "raspberry" password.
- Showing a black border (yes).
- Choose the WiFi. Typing in password.
- Checking for software updates. Downloading updates. Installing updates. Restart.

```
sudo apt update
sudo apt dist-upgrade
sudo apt clean
sudo reboot
```

> At sudo apt dist-upgrade, "The following package was automatically installed and is no longer required: python-colorzero. Use 'sudo apt auto remove' to remove it."

<hr>

## Starting to Install Sphero SDK

https://github.com/sphero-inc/sphero-sdk-raspberrypi-python

- Cloning github into pi (home) directory
- Renamed repo to sphero (we will see if this is a good idea or not)

> Note that need to use python versus python3 to get versions 2.7.16 versus 3.7.3. AND pip v18.1 for python2.7; pip3 v18.1 for python3

- `cd sphero`
- **Edit first-time-setup.sh so that it uses python3 and pip3, not python**.
- Run script with `./first-time-setup.sh`. Installing all the packages. DID NOT LIKE pip3 -- changing back and running again. That worked. Restart.
  > Gives a message that the path is not set, but it really is. You can confirm with echo $PATH.

After reboot.
- `pipenv --python /usr/bin/python3.7` (Successfully created virtual environment)
- `pipenv install` (_Creating Pipfile.lock. Taking a very long time - spinning on "Locking". Installing dependencies - taking a long time._)

"AN ERROR OCCURRED: cryptography==3.4.7; python_version >= '3.6' then --hash with a lot of numbers (repeated)! Will try again." Then it kept going. Saved the error message in errormessage.txt.

- Fixing cryptography error. Looking at: https://cryptography.io/en/latest/installation/.
  - pip install --upgrade pip (successfully installed v20.3.4) EXCEPT I think I just updated pip. Try again with pip3
  - pip3 install --upgrade pip (that seemed to work)
  - pip3 install cryptogrphy (but states it is already installed??)

Shutting down to connect Pi to RVR

<hr>

## Ready for Pi + rvr

1. Set up SSH with `sudo raspi-config`. Enable SSH (under "Interface Options") and you can enable VNC and the camera while you are at it.
2. Got IP address with `hostname -I`. Checked ssh and all good.

```
cd sphero
pipenv shell
```
NOW IN VIRTUAL ENVIRONMENT (notice the "(sphero)" in front of the prompt)

3. `cd gettingstarted/observer/driving`
4. `sudo python3 drive_raw_motors.py`

Now begins the issue with things not installed. First note is 'aiohttp' even though it is in the Pipfile listed as a dependency. I think this is where we get into trouble because everything is installed without sudo, but now I am trying with sudo to gain access to the port.

Back in raspi-config under SSH. NO to console, YES to enable SSH.
Reboot.

- `pip3 install aiohttp`
- 'pip3 install serial_asyncio' (no version)
- 'pip3 install pySerial_asyncio'

Darn it! I wasn't in the pipenv shell. Try this again ...

- `pip3 install aiohttp`
- 'pip3 install pySerial_asyncio' (bunch of error msgs about connecting, but then was successful)

New problem -- "Checking RVR firmware versions ..." then nothing.

Stopped there. Shut everything down. When I returned, it was all working! Yay!

<hr>

## Installing OpenCV: https://www.jeremymorgan.com/tutorials/raspberry-pi/how-to-install-opencv-raspberry-pi/

1. Per instructions, expand file system (to ensure card is being fully used). Reboot.

(as an aside, I checked in with ssh to see if it was still working. All of this could be done through ssh)

```
df -h     // to show disk is fully available -- i see 29G on a 32G card
cd sphero
pipenv shell
```

```
# these update commands done with sphero install, so did not do anything really
sudo apt-get update
sudo apt-get upgrade
sudo pip3 install opencv-contrib-python
```

BIG FAIL on that one. Put the error messages in installcverror.txt.
After the fact, I noticed that I had put that "sudo" in front of the pip3 install -- I do not think that is right.

It is having problems installing wheels (I have seen this before).

Trying this: https://github.com/opencv/opencv/issues/18359
```
pip3 install --upgrade pip setuptools wheel
pip3 install opencv-contrib-python
```

BIG FAIL again. error on cmake installation again. Okay, let's try sudo again.

```
sudo pip3 install opencv-contrib-python   // FAIL
sudo pip3 install --upgrade pip setuptools wheel
```

Interesting on the pip upgrade -- I noticed that it states pip v18.1, but I had upgraded pip to v20.3.4. We will see.

```
pip3 install opencv-contrib-python    // (just "killed", nothing else)
sudo pip3 install opencv-contrib-python (just "killed".)
```

Now I am really stuck!!
Moved outside the pipenv shell `exit`. Trying `pip3 install opencv-contrib-python` outside the environment.

Error Message: "Defaulting to user installation because normal site-packages is not writable." Then a lot of red about the wheel and cmake, yet it is proceeding.

Here's a post about this error: https://stackoverflow.com/questions/59997065/pip-python-normal-site-packages-is-not-writeable/65290638
I think all these problems have to do with installing with different versions of python. Can I run RVR outside of virtual environment??

opencv installed just fine outside of pipenv!! Arg.

Gonna do a reboot, just in case.

Checking python versions inside the pipenv shell...
"python" in the shell is 3.7.3 !
"pip" in the shell is 21.1.3

```
pip install opencv-contrib-python   FAIL (killed)
sudo pip install opencv-contrib-python  FAIL (killed)
```

You can see error messages from the kernal in _/var/log/messages_

Get a list of packages installed: `pip list` BUT if you `sudo pip list`, it is a different list.

Exited shell. Again with `python -m pip install pipenv` NOTICE used _python_, not _python3_. Proceeded with install -- did not indicate this was already done. Back in to `pipenv shell`.

`pip install opencv-contrib-python`

(giving me error msgs about Python 2.7 deprecation ???)

Failed to build wheel (again) but keeps going ...
"using cached opencv-contrib-python-4.5.1.48.tar.gz"

SUCCESS (I THINK!!)

```
python
>>> import cv2
```

ERROR: libhdf5_serial.so cannot open shared object file.
https://stackoverflow.com/questions/62433716/how-to-solve-importerror-libhdf5-serial-so-103-cannot-open-shared-object-file
`pip install h5py`

successfully installed but it did not fix the problem.
trying `pipenv install h5py`
trying `sudo apt-get install python3-h5py`

I think that last one worked!!!

In python, `>>>import cv2` ERROR: "libcblas.so no file"
https://stackoverflow.com/questions/53347759/importerror-libcblas-so-3-cannot-open-shared-object-file-no-such-file-or-dire

Trying `sudo apt-get install libcblas-dev` ERROR: "not available, but replaced with libatlas-base-dev"

`sudo apt-get install libatlas-base-dev`

SUCCESS!!!!!!!!!!!!!
