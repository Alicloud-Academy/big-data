# MaxCompute UDF Python Functions: With Custom Libaries!

- Status: **OK**
- Notes: Code tested and working as of 2021-01-20 (YYYY-MM-DD)

## What

This is a quick how-to (and demo Python code) showing how you can implement a Python UDF function in a MaxCompute project which includes additional Python dependencies (external libraries) not provided by the default MaxCompute Python UDF runtime environment.

## How

### Create a DataWorks Workspace

First, you'll need to open up the [Alibaba Cloud Console](https://www.alibabacloud.com) by clicking on "Log In" on the upper right hand side of the Alibaba Cloud homepage. Then, you'll need to locate the DataWorks console and create a new Workspace:

![Open the product menu](images/01.png)

![Search for DataWorks](images/02.png)

![Choose region](images/03.png)

![Create workspace](images/04.png)

![Choose the compute engine](images/05.png)

![Give the MaxCompute project a name](images/06.png)

![Open DataWorks DataStudio](images/07.png)

### Set up some test tables

Create two tables, one to hold the radii of circles (input data), and another to hold their areas, which we will calculate using a 3rd party library (NumPy) added to a Python 3 UDF function (more on that later). 

First, set up a new Ad-hoc Query:

![Set up new Ad-hoc Query](images/08.png)

![Open DataWorks DataStudio](images/09.png)

Once the Ad-hoc Query window opens, paste in the following MaxCompute SQL code, then hit the "Run" button near the top of the Ad-hoc Query Window:

```sql
CREATE TABLE IF NOT EXISTS circle_data (
    id BIGINT COMMENT 'circle id number',
    radius DOUBLE COMMENT 'circle radius'
);

-- Result table containing the info from circle_data, plus calculated areas
CREATE TABLE IF NOT EXISTS circle_data_out (
    id BIGINT COMMENT 'circle id number',
    radius DOUBLE COMMENT 'circle radius',
    area DOUBLE COMMENT 'circle area'
);
```

Next, create an additional Ad-hoc Query window, which we'll use to insert some test data into the `circle_data` table:

![Create additional Ad-hoc Query](images/10.png)

The SQL code you should paste into the query window is:

```sql
INSERT INTO TABLE circle_data (id, radius) VALUES (0, 1.5);
INSERT INTO TABLE circle_data (id, radius) VALUES (1, 2.0);
INSERT INTO TABLE circle_data (id, radius) VALUES (2, 3.0);
INSERT INTO TABLE circle_data (id, radius) VALUES (3, 2.5);
INSERT INTO TABLE circle_data (id, radius) VALUES (4, 0.9);
```

![Run query](images/11.png)

### Create a new Workflow

We need to create a new DataWorks Workflow where we can upload our Python code and associated 3rd party libary code (NumPy). We can do this from the "Manually Triggered Workflows" area in the DataStudio console:

![Create new Workflow](images/12.png)

![Name new Workflow](images/13.png)

### Upload resources

Next, we need to upload our Python code. Right click on "Resources", then choose "Create -> Python":

![Create Python resource](images/14.png)

![Create Python resource](images/15.png)

A new dialog should open:

![New Python window](images/16.png)

Paste the following code into the dialog:

```python
from odps.udf import annotate
@annotate("double->double")
class area(object):
    def __init__(self):
        import sys
        sys.path.insert(0, 'work/numpy-1.19.5-cp37-cp37m-manylinux1_x86_64.zip') # Our NumPy package

    def evaluate(self, arg0):
       import numpy as np
       if arg0 is None:
           return None
       # Calculate area of the circle
       return np.pi * (arg0 * arg0)
```

### Add the NumPy library 

We want to include a NumPy package in our Python 3 UDF. The package we are using for this example is `numpy-1.19.5-cp37-cp37m-manylinux1_x86_64`. You can get a copy [here](https://pypi.org/project/numpy/#files). 

Note that it is **very important** to make sure the package name includes "cp37" since the package needs to be built using the same version of CPython used by MaxCompute. When you download this file, the extension will be `.whl` (it's a wheel file). Change the extension to `.zip`, then upload the file as a resource:

![Create new resource](images/17.png)

![Upload new resource](images/18.png)

Note that after you upload the NumPy .zip file but *before* you click "Create", you should see something like this:

![Upload new resource](images/19.png)

### Create and register a new UDF

Now we have our Python code and our NumPy library `.zip` file. It's time to register a UDF function! Right click on "Function" as shown in the image below, then click on "Create Solution"

![Create function](images/20.png)

This will open up the function creation dialog:

![Set function name](images/21.png)

After you've given the function a name, you need to tell MaxCompute which resources it depends on:

![Set function configuration](images/22.png)

We're almost ready to use the UDF, but before we do that you need to **submit** the function, the area.py file, and the NumPy `.zip` archive. Click on the tab corresponding to each of those resources in the DataStudio console, and click on the little up arrow (next to the save button). **This is a critically important step, all 3 of these resources must be submitted before you will be able to call your UDF function successfully**.

### Try out the new UDF function

Now that our UDF function is registered, we can create a new ODPS SQL node that uses this function:

![Create an ODPS SQL node](images/23.png)

Once the Ad-Hoc query is set up, copy-paste this code into the query window:

```sql
set odps.sql.python.version=cp37;
INSERT OVERWRITE TABLE circle_data_out 
SELECT id, radius, area(radius) FROM circle_data;
```

Note that the line `set odps.sql.python.version=cp37;` is **critical**, because MaxCompute runs Python UDFs using Python 2 by default. This line forces MaxCompute to run Python UDFs using the Python 3 runtime.

Once you've saved your code, click on Run to execute the code:

![Paste in code, then run](images/24.png)

If everything went well, after 10-15 seconds you should see a message like this in the MaxCompute logs:

![Paste in code, then run](images/25.png)

### Check our results

Switch back to the Ad-hoc Query view and create a new query called `check_results`:

![Create new query](images/26.png)

![Name new query](images/27.png)

Paste the following code into the query window:

```sql
SELECT * FROM circle_data;
SELECT * FROM circle_data_out;
```

![Run new query](images/28.png)

After clicking "Run", you'll be presented with a dialog which will indicate whether there are any errors in your SQL code, alongside a cost estimate:

![Confirm run](images/29.png)

If there are no errors, click "Run" to continue.

After the two `SELECT` statements execute, you should see the following output:

![Input table](images/30.png)

![Input table](images/31.png)

That's it! You've successfully created a Python 3 UDF that uses a 3rd party library, and have used it within your MaxCompute project!

### Cleaning Up

When you're done, just delete the DataWorks Workspace and that's it! All the related resources (MaxCompute project, tables, functions) will be automatically released.

## Issues

None yet! If you find one let us know. 

## Credits

I drew some inspiration from this [LabEx lab](https://labex.io/courses/use-maxcompute-studio-to-develop-python-udfs) on creating Python UDF functions, though I chose to use the DataWorks interface rather than IntelliJ. 

[This document](https://www.alibabacloud.com/help/doc-detail/189752.htm) on adding custom libraries to Python 3 UDFs was also referenced heavily as I wrote this tutorial.

