import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import sys
import math


class FlutterWindField(OpenMayaMPx.MPxFieldNode):
    kPluginNodeName = "flutterWindField"
    kPluginNodeId = OpenMaya.MTypeId(0x000494f7)

    def __init__(self):
        OpenMayaMPx.MPxFieldNode.__init__(self)

    def compute(self, plug, dataBlock):
        if not (plug==self.mOutputForce):
            return False

        try:
            # get the logical index of the element this plug refers to
            multiIndex = plug.logicalIndex()

            # Get input data handle, use outputArrayValue since we do not
            # want to evaluate both inputs, only the one related to the
            # requested multiIndex. Evaluating both inputs at once would cause
            # a dependency graph loop.

            hInputArray = dataBlock.inputArrayValue(self.mInputData)
            hInputArray.jumpToElement(multiIndex)

            # get children of aInputData
            hCompond = hInputArray.inputValue()

            hPosition = hCompond.child(self.mInputPositions)
            dPosition = hPosition.data()
            fnPosition = OpenMaya.MFnVectorArrayData(dPosition)
            points = fnPosition.array()

            forceArray = self.applySineWave(dataBlock, points)

            # get output data handle
            hOutArray = dataBlock.outputArrayValue(self.mOutputForce)
            bOutArray = hOutArray.builder()

            # get output force array from block
            hOut = bOutArray.addElement(multiIndex)
            fnOutputForce = OpenMaya.MFnVectorArrayData()
            dOutputForce = fnOutputForce.create(forceArray)

            # update data block with new output force data
            hOut.setMObject(dOutputForce)
            dataBlock.setClean(plug)
        except:
            #Ignoring the logical index error
            pass

        return True


    def applySineWave(self, block, points):
        time = OpenMayaAnim.MAnimControl.currentTime()
        currentFrame = time.value()

        if (not points.length()):
            return False
        
        outputForce = OpenMaya.MVectorArray()

        windDirectionValue = block.inputValue(self.windDirection).asFloatVector()
        windMagnitudeValue = block.inputValue(self.windMagnitude).asDouble()
        windSpeedValue = block.inputValue(self.windSpeed).asDouble()
        windFreqValue = block.inputValue(self.windFreq).asDouble()
        windTimeOffsetValue = block.inputValue(self.windTimeOffset).asDouble()
        windDirectionOffsetValue = block.inputValue (self.windDirectionOffset).asFloatVector()
        windRandomAmpValue = block.inputValue(self.windRandomAmp).asDouble()
        windRandomFreqValue = block.inputValue(self.windRandomFreq).asDouble()
        windRandomSpeedValue = block.inputValue(self.windRandomSpeed).asDouble()

        windDirection = OpenMaya.MVector(windDirectionValue)
        windDirection0ffset = OpenMaya.MVector(windDirectionOffsetValue)
        windNoise = OpenMaya.MVector()
        windRand = OpenMaya.MVector()

        wind = OpenMaya.MVector(0, 0, 0)

        for idx_point in range(points.length()):
            if (windRandomAmpValue != 0.0 or windRandomFreqValue != 0.0 or windRandomSpeedValue != 0.0):
                windDirectionValue.normalize()
                wind = OpenMaya.MVector(-1.0 * windDirectionOffset.x * (currentFrame + windTimeOffsetValue) +
                            points[idx_point].x * windRandomFreqValue -
                            windRandomspeedValue * (currentFrame + windTineOffsetValue) * windDirection.x,
                            -1.0 * windDirectionOffset.y * (currentFrame + windTimeOffsetValue) +
                            point[idx_point].y * windRandomFreqValue -
                            windRandomSpeedValue * (currentFrame + windTimeOffsetValue) * windDirection.y,
                            -1.0 * windDirectionOffset.z * (currentFrame + windTimeOffsetValue) +
                            point[idx_point].z * windRandomFreqValue -
                            windRandomSpeedValue * (currentFrame + windTimeOffsetValue) * windDirection.z)

            #outputForce. append (wind"windRandomAmpValue)
            wind = OpenMaya.MVector(math.sin((currentFrame + points[idx_point].x) * windDirection.x),
                                    math.sin((currentFrame + points[idx_point].x) * windDirection.y),
                                    math.sin((currentFrame + points[idx_point].x) * windDirection.z))

            wind = OpenMaya.MVector(0, (windMagnitudeValue*math.sin((currentFrame*windSpeedValue) + points[idx_point].x*windFreqValue)), 0)
            
            outputForce.append(wind*windMagnitudeValue)
        return outputForce
        


def flutterWindFieldCreator():
    """
    Used by Maya to initiate a new node.
    """
    return OpenMayaMPx.asMPxPtr(FlutterWindField())



def flutterWindFieldInitialize():
    """
    Node attributes.
    """
    matrixAttr = OpenMaya.MFnMatrixAttribute()
    unitAttr = OpenMaya.MFnUnitAttribute()
    compoundAttr = OpenMaya.MFnCompoundAttribute()
    numAttr = OpenMaya.MFnNumericAttribute()

    #INPUT
    FlutterWindField.windDirection = numAttr.createPoint('windDirection', 'wdir')
    numAttr.setDefault(1.0, 0.0, 0.0)
    FlutterWindField.addAttribute(FlutterWindField.windDirection)

    FlutterWindField.windMagnitude = numAttr.create('windMagnitude', 'wmag', OpenMaya.MFnNumericData.kDouble, 10)
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windMagnitude)

    FlutterWindField.windSpeed = numAttr.create('windSpeed', 'wsp', OpenMaya.MFnNumericData.kDouble, 0.5)
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windSpeed)

    FlutterWindField.windFreq = numAttr.create('windFreq', 'wfr', OpenMaya.MFnNumericData.kDouble, 0.01)
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windFreq)

    FlutterWindField.windTimeOffset = numAttr.create('windTimeOffset', 'wto', OpenMaya.MFnNumericData.kDouble, 0)
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windTimeOffset)

    FlutterWindField.windDirectionOffset = numAttr.createPoint('windDirectionOffset', 'wdiro')
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windDirectionOffset)

    FlutterWindField.windRandomAmp = numAttr.create('windRandomAmp', 'wra', OpenMaya.MFnNumericData.kDouble, 0)
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windRandomAmp)

    FlutterWindField.windRandomFreq = numAttr.create('windRandomFreq', 'wrfr', OpenMaya.MFnNumericData.kDouble, 0)
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windRandomFreq)

    FlutterWindField.windRandomSpeed = numAttr.create('windRandomSpeed', 'wrsp', OpenMaya.MFnNumericData.kDouble, 0)
    numAttr.setStorable(True)
    numAttr.setKeyable(True)
    numAttr.setHidden(False)
    FlutterWindField.addAttribute(FlutterWindField.windRandomSpeed)

    FlutterWindField.mOutputForce = OpenMayaMPx.cvar.MPxFieldNode_mOutputForce

    FlutterWindField.attributeAffects(FlutterWindField.windDirection, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windMagnitude, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windSpeed, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windFreq, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windTimeOffset, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windDirectionOffset, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windRandomAmp, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windRandomFreq, FlutterWindField.mOutputForce)
    FlutterWindField.attributeAffects(FlutterWindField.windRandomSpeed, FlutterWindField.mOutputForce)


def initializePlugin(mobject):
    """
    Called by Maya to load the plugin.
    """
    plugin = OpenMayaMPx.MFnPlugin(mobject, 'David De Juan')
    try:
        plugin.registerNode(FlutterWindField.kPluginNodeName, FlutterWindField.kPluginNodeId, flutterWindFieldCreator, flutterWindFieldInitialize, OpenMayaMPx.MPxNode.kFieldNode)
    except:
        sys.stderr.write("Failed to register node: %s" % FlutterWindField.kPluginNodeName)
        raise


def uninitializePlugin(mobject):
    """
    Called by Maya to unlock the plugin.
    """
    plugin = OpenMayaMPx.MFnPlugin(mobject, 'David De Juan')
    try:
        plugin.deregisterNode(FlutterWindField.kPluginNodeId)
    except:
        sys.stderr.write("Failed to deregister node: %s" % FlutterWindField.kPluginNodeName)
        raise