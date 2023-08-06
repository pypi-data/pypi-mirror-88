# SDFUtils
Gazebo SDF utils.  Write smaller and simpler xacro and get richer and complex SDF files.
## basic usage: 
python3 xacro2sdf.xacro2sdf input_xacro_file output_sdf_file 
## XACRO
- properties
- macro
- include
- pure python

## properties
- declare variable to use by other sdf section


##### source sdf with xacro tags
```xml
<sdf xmlns:xacro="http://xacro">
    <xacro:property name="width" value=".2" />
    <xacro:property name="bodylen" value=".6" />
    <xacro:property name="x" value="1" />
    <xacro:property name="y" value="2" />
    <xacro:property name="z" value="3" />
    <link name="base_link">
        <pose>${x} ${y} ${z} 0 0 0</pose>
        <visual>
            <geometry>
                <cylinder radius="${2*width}" length="${bodylen}" />
            </geometry>
        </visual>
    </link>
</sdf>
```
##### output sdf
```xml
<sdf >
    <link name="base_link">
        <pose>1.0 2.0 3.0 0 0 0</pose>
        <visual>
            <geometry>
                <cylinder radius="0.4" length="0.6"/>
            </geometry>
        </visual>
    </link>
</sdf>
```

## include
include other `xacro` files to use

- `file://` : load files relative to sdf/xacro file
- `package://` : load files from `helper` folder under script source folder

```xml
<xacro:include uri="file://data.xacro" />
<xacro:include uri="package://common.xacro" />
<xacro:include uri="package://color.xacro" />
```

- `data.xacro`: custom file hold data properties for example
- `common.xacro`: common macro's like inertia and basic geometry
- `color.xacro`: color and texture macro's

## pure python
- use python inside your models, ident the same as in python (starting from column 0)!
- store your needed variables in "return_values" dictionary and use them later in the model by the given keys.   

```xml
    <xacro:python>
    <![CDATA[
import numpy as np 
def foo(): 
    if 2 > 5: 
        return 5,4,3,2,1
    global np
    b = np.array([0,1])
    x = 3433
    y = 324
    z = 3
    m = 1
    return x,y,z,m,b
temp = foo()
return_values = {'x': temp[0], 'y': temp[1], 'z': temp[2], 'm': temp[3], 'b': temp[4]}
]]>
    </xacro:python> 
```


### common 
#### macros
- inertia_box
- inertia_sphere
- inertia_cylinder
- geometry_cylinder
- geometry_box
- geometry_sphere

### color
#### macro
- color
