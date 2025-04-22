# flutterWindNode

An Autodesk Maya Field Node that helps to achieve a flutter wind effect to any nucleus-based simulation.  
By applying a sine wave to the field, it generates the desired flutter motion.  
While still in its experimental stages, this technique has been successfully used in multiple production shots.  
I recommend using it in conjuntion with other winds.


**How to use it:**  
Create a flutterWindNode.  
Connect it to the nCloth or nHair object. You can use mel or python to do that.  
```python
connectDynamic -f flutterWindNode nClothObject;   
cmds.connectDynamic("flutterWindNode", "nClothObject", f=True) 
```

**Basic example, with no other wind applied:**  

https://github.com/user-attachments/assets/8e3979cf-05a1-4047-910e-1cf37181258a
