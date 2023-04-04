from OMPython import OMCSessionZMQ
import json


def parseJson(jsonPath):
    jsonFile = open(jsonPath)
    data = json.load(jsonFile)
    name = ''
    componentsStr = ''
    equationsStr = ''
    for model in data:
        name = model
        for key in data[model]:
            # key = places, transitions, arcs
            for obj in data[model][key]:
                # obj is specific place, transition, arc
                currentObj = data[model][key][obj]
                if key != 'Arcs':
                    # add component type and name to string
                    # example : PNlib.Components.PD PD_0
                    componentsStr += '    PNlib.Components.' + \
                        obj.split('_')[0] + ' ' + obj + '('

                    # loop over properties and add to string
                    # example (startTokens=1,nIn=0,nOut=1);

                    for property in currentObj:
                        componentsStr += property + '=' + \
                            str(currentObj[property]) + ','
                    componentsStr = componentsStr[:-1] + ');\n'
                else:
                    # add arc to equation string
                    # assumes after place always transition and vice versa
                    # TODO arcs count out, intplaces
                    startName = currentObj['start'].split('.')[-1]
                    endName = currentObj['end'].split('.')[-1]
                    if 'Transition' in currentObj['start']:
                        # TODO outPlace number
                        startName += '.outPlaces[1]'

                    else:
                        # TODO outT number
                        startName += '.outTransition[1]'

                    if 'Transition' in currentObj['end']:
                        # TODO inPlace number
                        endName += '.inPlaces[1]'
                    else:
                        # TODO inT number
                        endName += '.inTransition[1]'

                    # add to equation string
                    # example connect(PD_0.outPlaces[1],T_0.inTransition[1]);
                    equationsStr += '        connect(' + \
                        startName + ',' + endName + ');\n'
    return name, componentsStr, equationsStr


def writeModelicaFile(name, components, equations):
    # create .mo file
    modelicaFile = open('models/'+name+'.mo', 'w')

    # build .mo file
    modelStr = 'model ' + name + '\n'\
        + components + \
        '    equation\n' + equations + \
        '    annotation(\n' +\
        '        uses(PNlib(version = "2.2"))\n' +\
        '    );\n' +\
        'end '+name+';'

    # writes modelica file
    modelicaFile.write(modelStr)
    return modelStr


def simulateInOM(modelName, startTime=0, stopTime=10, numberOfIntervals=500, plotVars=''):
    # start OpenModelica
    omc = OMCSessionZMQ()
    cmds = [
        # load PNlib
        'loadModel(PNlib)',

        # load model
        'loadFile("models/'+modelName+'.mo")',

        # simulate model
        'simulate('+modelName + \

        ', startTime = '+str(startTime) + \
        ', stopTime = '+str(stopTime) + \
        ', numberOfIntervals ='+str(numberOfIntervals)+')',
        # plot results
        "plot("+plotVars+")"
    ]

    # execute commands and print results
    for cmd in cmds:
        answer = omc.sendExpression(cmd)
        print("\n{}:\n{}".format(cmd, answer))


modelname, components, equations = parseJson('wfml_HPN.json')
print(writeModelicaFile(modelname, components, equations))
simulateInOM(modelname, 0, 10, 500, '{PD_0.t, PD_1.t, PC_0.t, PC_1.t}')
