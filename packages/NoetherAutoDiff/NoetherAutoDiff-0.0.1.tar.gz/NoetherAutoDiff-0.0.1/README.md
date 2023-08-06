## First, Acknowledgment
In case you're wondering, our project's name is chosen because we wanted to highlight a brilliant mathematician, [Emmy Noether][EmmyNoetherWiki]. In the late 19th to early 20th centry, she contributed a lot to the field of mathematics, including [Noether's Theorm][noethers_theorm], and with very little recoginition while she was alive. 

## Installing the NoetherAutoDiff python library

#### Option 1: ###
- Use pip install to install directory from PyPI (TODO)  
    ```
    pip install NoetherAutoDiff
    ```

#### Option 2:
- Download the NoetherAutoDiff python module along with the C++ `.so` shared object from our [github repo][py_source_files]. The package is contained inside the [*/py/bin*][py_dir_link] subdirectory in our repo. Inside it has a few *.py files and NoetherAutoDiff.so C/C++ shared library. You don't need anything else.  

- Then find out what environement path Python checks on your machine. To do this follow this steps:  
```$ python```   

    Next, import the sys module:

    ``` >>> import sys```

    Then have Python print out the system path:

    ```>>> print(sys.path)```

    From the output on your python interpreter, look for something like this:   

    ```
    '/usr/.../.../lib/python3.5/site-packages'
    ```

- Next, move the folder you downloaded into this location. All the files should stay inside the NoetherAD sub directory except for the NoetherAD.py file. Put the NoetherAD.py file at the same level as the NoetherAutoDiff directory. It should look like below:

    ```
    /usr/.../python3.6/site-packages/NoetherAutoDiff     <--- everthing else inside the folder
    /usr/...python3.6/site-packages/NoetherAD.py         <--- the file that contains all *import* statements
    ```

## Basic Usage (Tutorial)
Once installed using either *Option 1* or *Option 2* mentioned above, you can type  `import NoetherAutoDiff` from the `$ python` command line as follows:
```
>>> import NoetherAutoDiff as nad
```
Then you can instantiate any of these classes `NoetherAutoDiff`, `NoetherAutoDiff_Vector`, `NoetherAutoDiff_V`, `NoetherAutoDiff_V_Vector` by providing the correct input arguments at instantiation. Here are a few examples on how to find the directional or none directional derivatives the Auto Differentiation algorithm.  

The `NoetherAutoDiff` class take four inputs. They have the following types:
- `input` - a **string** representing the function to be evaluated
- `mode` - the integer **0**  for (for forward mode), or a **1** (for reverse mode) evaluation of auto diff
- `inits` - are key (`char`) and value (`double`) pair of the variables' representation (the point where the derivative will be evaluated at)
- `seeds` - represents the seed vector (the direction of the vector for directional derivatives)  

Now, let's try an ugle looking function from the python interpreter line:
```
>>> function = "sin(x)^cos(x-5/3+4^x*y/z)/tan(3*x)+exp(3*x-1)"
>>> mode = 0
>>> inits = {'x': 1.4, 'y': 2.4, 'z': 3.4}
>>> seeds =  {'x': 1, 'y': 1, 'z': 1}
>>> n = nad.NoetherAutoDiff(function, mode, inits, seeds) 
```
We now have our `NoetherAutoDiff` object. Here is how we can access the value of the function:
```
>>> n.val
25.095548918554428
```
Here is how we can get the derivaties with respect to all variables:
```
>>> n.deriv
{'x': 69.57424922848773, 'y': -0.016870006832635686, 'z': 0.0119082401171546}
```
or we can pretty print all the inputs and outputs using `.print()` as follows:
```
>>> n.print()
Input function:
  f = sin(x)^cos(x-5/3+4^x*y/z)/tan(3*x)+exp(3*x-1)
Evaluated at:
  x=1.4
  y=2.4
  z=3.4
Numeric Value:
  f = 25.095548918554428
Derivates:
  df/dx = 69.57424922848773
  df/dy = -0.016870006832635686
  df/dz = 0.0119082401171546
```

Comparison operations are suppoerted. To check weather or not two `NoetherAutoDiff` objects are the same, do this:
```
>>> n == n
True
```

The main difference between the `NoetherAutoDiff` and `NoetherAutoDiff_Vector` classes is that the latter takes vector positional inputs as opposed to key/value dictionary as `inits` and `seeds`. For that to work, the variables in the input function have to be provided as `x0, x1, ...` as below:
```
>>> function = "sin(x0)^cos(x0-5/3+4^x0*x1/x2)/tan(3*x0)+exp(3*x0-1)"
>>> inits_v = [1.0, 2.0, 3.0]
>>> seeds_v = [1, 1, 1]
>>> n_v = nad.NoetherAutoDiff_Vector(function, mode, inits_v, seeds_v) 
>>> n_v.val
-0.14862974395913575
>>> n_v.deriv
[-143.23486622993053, -1.577367720808487, 1.0515784805389914]
```
We can again pretty print the input and outputs as follows.
```
>>> n_v.print()
Input function:
  f = sin(x0)^cos(x0-5/3+4^x0*x1/x2)/tan(3*x0)+exp(3*x0-1)
Evaluated at:
  x0=1.0
  x1=2.0
  x2=3.0
Numeric Value:
  f = -0.14862974395913575
Derivates:
  df/dx0 = -143.23486622993053
  df/dx1 = -1.577367720808487
  df/dx2 = 1.0515784805389914
```

Let's try comparions `n` and `n_v`:
```
>>> n == n_v
False
```
Aha! Notice the init values are not the same. Otherwise the above would print `True`.

The other two classes we haven't talked about yet have similar behavior except that these take a number of function (a system of equations). The `NoetherAutoDiff_V` take a python list of string each representing a function, and key/value `inits` and `seeds`, same as `NoetherAutoDiff`. The `NoetherAutoDiff_V_Vector` class takes in a list of equation strings (with variables represented as `x0, x1, ...) and a python list of positional values for `inits` and `seeds`.


### Todos

 - Add more features (like printing trace and graph)
 - Write more tests
 - Add more tutorial, and demo use cases that demonstrate the value of **AutoDiff**
 - Support complex numbers?

License
----

MIT


**Free Software, Hell Yeah!**

[noethers_theorm]: <https://en.wikipedia.org/wiki/Noether%27s_theorem>
[EmmyNoetherWiki]: <https://en.wikipedia.org/wiki/Noether%27s_theorem>
[py_source_files]: <https://github.com/cs107-noether/cs107-FinalProject/archive/v0.1.tar.gz>
[py_dir_link]: <https://github.com/cs107-noether/cs107-FinalProject/tree/dev/py>
