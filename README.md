# wfml_PN_OMSimulation
0. install OMPython (https://github.com/OpenModelica/OMPython) only needed when simulating
1. Generate WMLF json with Model (names in model need to same as PNLib Components, e.g. TransitionWithDelay = TD), see wfml_HPN_model.txt
2. adjust json name and simulation parameters and what results should be ploted
3. run ```python wfmlToOMSimulation.py```
