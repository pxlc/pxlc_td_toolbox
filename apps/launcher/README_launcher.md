# Pixelcurio Launcher Application example

This is a simple example of an animation/VFX studio "Launcher Application" written using the [Qt shim](https://github.com/mottosso/Qt.py), created by [Marcus Ottosson](https://github.com/mottosso), with interface design using Qt Designer provided with PySide 1.2.2 for Python 2.7.x.

## Qt Designer to Qt-shim compatible `.py` interface file

The Qt shim is a wrapper around various modules providing access to Qt UI functionality (PySide 1.2.x, PySide 2.x, Qt4, and Qt5), but abstracting modules so that code can be used across environments with varying Qt module availability.

The Qt shim mimics PySide2, so using the Qt Designer and the `pyside-uic` converter for PySide 1.2.x, will generate a python module file that isn't fully compatible with the Qt shim.

In the `bin` folder of this applicatin example is a python script that will take the output of a PySide 1.2.x `pyside-uic` conversion and revise it to make it compatible with the Qt shim.

### Here is the workflow:

**( 1 )** Run PySide UI Designer, likely found at **`C:\Python27\Lib\site-packages\PySide\designer.exe`** (on Windows) ... then create UI, and save out to a **`.ui`** file, say `pxlc_launcher_interface.ui`

**( 2 )** Then convert the `.ui` file to a `.py` module file, using:

```bash
> C:\Python27\python.exe C:\Python27\Lib\site-packages\PySide\scripts\uic.py -o pxlc_launcher_UI.py pxlc_launcher_interface.ui
```

**( 3 )** Then run the provided post-process script in the bin directory to make the converted `.py` module usable with the Qt shim:

```bash
> C:\Python27\python.exe .\bin\post_process_converted_ui_file.py pxlc_launcer_UI.py pxlc_launcher_UI_for_Qt_shim.py
```

**( 4 )** In the Qt-shim based main python script of your application, import the class object name from the `pxlc_launcher_UI_for_Qt_shim` module


## LICENSE

MIT License

Copyright (c) 2018 pxlc@github

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


<br/>

**[end]**
