# 1. Install Package ( windows / Linux / Mac )
### 1.1. requirements
> - Python 3.x
> - jupyter notebook or anaconda env
>   _pip install jupyter_ <br>
>   or <br>
>   _python -m pip install --user jupyter_ <br>
>
>   _pip3 install jupyter_  <br>
>   or <br>
>   _python3 -m pip install --user jupyter_ <br>

### 1.2. Install Visual Python package
> **[pip / conda]**
> _pip install visualpython_

### 1.3. Optional package
* jupyter_contrib_nbextensions<br>
* Install to manage nbtextensions visually.
>> **[pip]**<br>
>>  _pip install jupyter_contrib_nbextensions <br>_
   _jupyter contrib nbextension install --user_
>> **[conda - anaconda env]**
> _conda install -c conda-forge jupyter_contrib_nbextensions_ <br>
   _jupyter contrib nbextension install --user_

# 2.Package controller for Linux/Mac/Windows
### 2.1. Visual Python contoller info

> **usage: _visualpy [option]_** <br>

```
  optional arguments:
   -h,   help       - show this help message and exit
   -e,   enable     - enable Visual Python
   -d,   disable    - disable Visual Python
   -i,   install    - install Visual Python extensions
   -un,  uninstall  - uninstall Visual Python packages
   -up,  upgrade    - upgrade Visual Python Package
   -v,   version    - show Visual Python current version
```

### 2.2. Activate Visual Python
> _visualpy install_ <br>
> or <br>
> _visualpy -i_

### 2.3. Disable Visual Python
> _visualpy disable_ <br>
> or
> _visualpy -d_

### 2.4. Enable Visual Python extension
> _visualpy enable_ <br>
> or <br>
> _visualpy -e_

### 2.5. Upgrade Visual Python package version
> _visualpy upgrade_ <br>
> or <br>
> _visualpy -up_

### 2.6. Uninstall Visual Python package
> _visualpy uninstall_ <br>
> or <br>
> _visualpy -un_

