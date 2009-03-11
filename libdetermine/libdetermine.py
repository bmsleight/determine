# -*- coding: utf-8 -*-
#
#   determine - generate traffic signal timing diagrams to determine green running time. 
#   Copyright (C) Brendan M. Sleight, et al. <determine@barwap.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from optparse import OptionParser
import amara
import copy


class phaseTypeClass:
    def __init__(self, name="Traffic", preGreenName="Red-Amber", preGreenTime=2, preGreenTimeConfigurable=False, greenName="Green", 
                 greenConfigurable=True, greenMin=7,
                 postGreenName="Amber", postGreenTime=3, postGreenConfigurable=False, redName="Red"):
        self.name = str(unicode(name))
        self.preGreenName = str(unicode(preGreenName)) 
        self.preGreenTime = int(unicode(preGreenTime)) 
        if str(unicode(preGreenTimeConfigurable)) == "False":
            self.preGreenTimeConfigurable = False
        else:
            self.preGreenTimeConfigurable = True
        self.greenName = str(unicode(greenName))
        if str(unicode(greenConfigurable)) == "False":
            self.greenConfigurable = False
        else:
            self.greenConfigurable = True
        self.greenMin = int(unicode(greenMin))
        self.postGreenName = str(unicode(postGreenName))
        self.postGreenTime = int(unicode(postGreenTime))
        if str(unicode(postGreenConfigurable)) == "False":
            self.postGreenConfigurable = False
        else:
            self.postGreenConfigurable = True
        self.redName = str(unicode(redName))

class phaseTypeArrayClass:
    def __init__(self):
        self.phases = []
    def phaseType(self, name):
        phaseTypeFound = False
        for phaseType in self.phases:
            if phaseType.name == str(unicode(name)):
                phaseTypeFound = True
                returnPhaseType = phaseType
        if phaseTypeFound == False:
            returnPhaseType = self.phases[0]
        return returnPhaseType
    def listNames(self):
        namesList = []        
        for phaseType in self.phases:
            namesList.append(phaseType.name)
        return namesList

class phaseClass:
    def __init__(self, letter, phaseType, greenMin, preGreenTime=-1, postGreenTime=-1, description=None):
        self.letter = str(unicode(letter))
        self.phaseType = phaseType
        self.preGreenTimeConfigurable = phaseType.preGreenTimeConfigurable
        self.greenConfigurable = phaseType.greenConfigurable
        self.postGreenConfigurable = phaseType.postGreenConfigurable

        if greenMin==-1 or not self.greenConfigurable:
            self.greenMin = phaseType.greenMin
        else:
            self.greenMin = int(unicode(greenMin))
        if preGreenTime==-1 or not self.preGreenTimeConfigurable:
            self.preGreenTime = phaseType.preGreenTime
        else:
            self.preGreenTime = int(unicode(preGreenTime))
        if postGreenTime==-1 or not self.postGreenConfigurable:
            self.postGreenTime = int(unicode(phaseType.postGreenTime))
        else:
            self.postGreenTime = postGreenTime

        self.preGreenName = phaseType.preGreenName 
        self.greenName = phaseType.greenName
        self.postGreenName = phaseType.postGreenName
        self.redName = phaseType.redName
        self.intergreensFromLetter = []
        self.intergreensFromTime = []
        self.phaseDelayFrom = []
        self.phaseDelayTo = []
        self.phaseDelayTime = []
        self.description = description
    def setIntergreenFrom(self, FromPhaseLetter, FromTime):
        try:
            i = self.intergreensFromLetter.index(FromPhaseLetter)
            self.intergreensFromTime[i] = FromTime
        except:
            self.intergreensFromLetter.append(FromPhaseLetter)
            self.intergreensFromTime.append(int(unicode(FromTime)))
    def intergreenFrom(self, FromPhaseLetter):
        try:
            i = self.intergreensFromLetter.index(FromPhaseLetter)
            fromTime = self.intergreensFromTime[i]
        except:
            fromTime = 0
        return fromTime
    def setPhaseDelay(self, phaseDelayFrom, phaseDelayTo, phaseDelayTime):
        self.phaseDelayFrom.append(str(unicode(phaseDelayFrom)))
        self.phaseDelayTo.append(str(unicode(phaseDelayTo)))
        self.phaseDelayTime.append(int(unicode(phaseDelayTime)))
    def phaseDelay(self, phaseDelayFrom, phaseDelayTo):
        returnPhaseDelay = 0
        l = len(self.phaseDelayFrom)
        for i in range(0, l):
            if phaseDelayFrom == self.phaseDelayFrom[i] and phaseDelayTo == self.phaseDelayTo[i]:
                returnPhaseDelay = self.phaseDelayTime[i]
        return returnPhaseDelay
    def eachPhaseDelayText(self, i):
        phaseText = self.letter + " on a move from " + str(self.phaseDelayFrom[i]) + \
                       " to " + str(self.phaseDelayTo[i]) + " is delayed by " + str(self.phaseDelayTime[i]) + "\n"  
        return phaseText
    def phaseDelayDelete(self, phaseDelayText):
        delLetter = phaseDelayText.split()[0]
        delFrom = phaseDelayText.split()[5]
        delTo = phaseDelayText.split()[7]
        delTime = phaseDelayText.split()[11]
        l = len(self.phaseDelayFrom)
        foundIndex = -1
        for i in range(0, l):
            if self.phaseDelayFrom[i] == delFrom and \
            self.phaseDelayTo[i] == delTo and \
            str(self.phaseDelayTime[i]) == delTime:
                foundIndex = i
        if foundIndex !=-1:
            del self.phaseDelayFrom[foundIndex]
            del self.phaseDelayTo[foundIndex]
            del self.phaseDelayTime[foundIndex]
    def phaseDelayText(self):
        text = ""
        l = len(self.phaseDelayFrom)
        if l:
            for i in range(0, l):
                text = text + self.eachPhaseDelayText(i)
        return text
    def phaseDelayList(self):
        delayList = []
        l = len(self.phaseDelayFrom)
        for i in range(0, l):
            delayList.append(self.eachPhaseDelayText(i))
        return delayList
    def xmlPhase(self):
        xml = "<phase>"
        xml = xml + "<letter>"
        xml = xml + self.letter
        xml = xml + "</letter>"
        if self.description:
            xml = xml + "<description>"    
            xml = xml + self.description    
            xml = xml + "</description>"    
        xml = xml + "<signal_type>"
        xml = xml + str(self.phaseType.name)
        xml = xml + "</signal_type>"
        xml = xml + "<mintime>"
        xml = xml + str(self.greenMin)
        xml = xml + "</mintime>"
        if self.postGreenTime != self.phaseType.postGreenTime:
            xml = xml + "<post_green_time>"
            xml = xml + str(self.postGreenTime)
            xml = xml + "</post_green_time>"
        xml = xml + "</phase>"
        return xml
    def xmlPhaseDelay(self):
        if len(self.phaseDelayFrom) == 0:
            return ""
        else:
            xml = "<phase_delay>"
            for index in range(len(self.phaseDelayFrom)):
                xml = xml + "<phase>"
                xml = xml + str(self.letter)
                xml = xml + "</phase>"
                xml = xml + "<from>"
                xml = xml + str(self.phaseDelayFrom[index])
                xml = xml + "</from>"            
                xml = xml + "<to>"
                xml = xml + str(self.phaseDelayTo[index])
                xml = xml + "</to>"            
                xml = xml + "<length>"
                xml = xml + str(self.phaseDelayTime[index])
                xml = xml + "</length>"            
            xml = xml + "</phase_delay>"
            return xml
    def xmlIntergreens(self):
        if len(self.intergreensFromLetter) == 0:
            return ""
        else:
            xml = ""
#            print self.letter
#            print "self.intergreensFromLetter: ", len(self.intergreensFromLetter), self.intergreensFromLetter
#            for phase in self.intergreensFromLetter:
#                print str(phase)
#            print "self.intergreensFromTime: ", len(self.intergreensFromTime), self.intergreensFromTime
            for index in range(len(self.intergreensFromLetter)):
                xml = xml + "<intergreen>"
                xml = xml + "<from>"
                xml = xml + str(self.intergreensFromLetter[index])
                xml = xml + "</from>"            
                xml = xml + "<to>"
                xml = xml + str(self.letter)
                xml = xml + "</to>"
                xml = xml + "<length>"
                xml = xml + str(self.intergreensFromTime[index])
                xml = xml + "</length>"            
                xml = xml + "</intergreen>"
            return xml


class phaseArrayClass:
    def __init__(self):
        self.phases = []
    def newPhase(self, letter, phaseType, greenMin, preGreenTime=-1, postGreenTime=-1, description=None):
        phase = phaseClass(letter, phaseType, greenMin, preGreenTime, postGreenTime, description)
        self.phases.append(phase)
    def phase(self, letter):
        phaseFound = False
        for phase in self.phases:
            if phase.letter == str(unicode(letter)):
                phaseFound = True
                returnPhase = phase
        if phaseFound == False:
            returnPhase = self.phases[0]
        return returnPhase
    def phaseListLetters(self):
        listLetters = []
        for phase in self.phases:
            listLetters.append(phase.letter)
        return listLetters
    def phaseDelayText(self):
        text = ""
        for phase in self.phases:
            text = text + phase.phaseDelayText()
        return text
    def xml(self):
        xml = "<phases>"
        for phase in self.phases:
            xml = xml + str(phase.xmlPhase())
        xml = xml + "</phases>"
        return xml
    def xmlPhaseDelay(self):
        xml = "<phase_delays>"
        for phase in self.phases:
            xml = xml + str(phase.xmlPhaseDelay())
        xml = xml + "</phase_delays>"
        return xml
    def xmlIntergreens(self):
        xml = "<intergreens>"
        for phase in self.phases:
            xml = xml + str(phase.xmlIntergreens())
        xml = xml + "</intergreens>"
        return xml


class stageClass:
    def __init__(self, stageName):
        self.phases = []
        self.stageName = str(unicode(stageName))
    def doesContainPhase(self, phaseLetter):
        phaseFound = False
        for phase in self.phases:
            if phase.letter == phaseLetter:
                phaseFound = True
        return phaseFound
    def printAllPhases(self):
        for phase in self.phases:
            print "Stage", self.stageName, "Contains", phase.letter
    def text(self):
        text = "Stage " + self.stageName + ":"
        for phase in self.phases:
            text = text + " " + str(phase.letter) 
        return text
    def xml(self):
        xml = "<stage>" 
        xml = xml + "<stage_number>"
        xml = xml + self.stageName
        xml = xml + "</stage_number>"
        xml = xml + "<phases>" 
        for phase in self.phases:
            xml = xml + "<phase>"
            xml = xml + str(phase.letter)
            xml = xml + "</phase>"
        xml = xml + "</phases>" 
        xml = xml + "</stage>"
        return xml


class stageArrayClass:
    def __init__(self):
        self.stages = []
    def newStage(self, stageName):
        stage = stageClass(stageName)
        self.stages.append(stage)
    def stage(self, stageName):
        stageFound = False
        for stage in self.stages:
            if stage.stageName == str(unicode(stageName)):
                stageFound = True
                returnStage = stage
        if stageFound == False:
            returnStage = False
        return returnStage
    def text(self):
        text = "" 
        for stage in self.stages:
            text = text + stage.text()
            text = text + " \n"
        return text
    def listStageNames(self):
        listStageNames = []
        for stage in self.stages:
            listStageNames.append(str(unicode(stage.stageName)))
        return listStageNames  
    def xml(self):
        xml = "<stages>" 
        for stage in self.stages:
            xml = xml + stage.xml()
        xml = xml + "</stages>"
        return xml

class diagramPhaseClass:
    def __init__(self, letter, state="Red", minRemaining=0, timeSinceGreen=180, move=None):
        self.letter = letter
        self.state = state
        self.minRemaining = minRemaining
        self.timeSinceGreen = timeSinceGreen
        self.move = move
        self.intergreens = [] 
        self.phaseDelayTime = 0
        self.comments = ""
    def largestIntergreen(self):
        largest = 0
        for intergreen in self.intergreens:
            if intergreen.remaining > largest:
                largest = intergreen.remaining
        return largest
    def decrementIntergreens(self, site, lastSecondDiagram):
        for intergreen in self.intergreens:
            if lastSecondDiagram.diagramPhase(intergreen.fromLetter).state != site.phases.phase(intergreen.fromLetter).phaseType.greenName:
                intergreen.remaining = intergreen.remaining - 1
                if intergreen.remaining == 0:
                    self.intergreens.remove(intergreen)
    def decrementMinTime(self):
        if self.minRemaining > 0:
            self.minRemaining = self.minRemaining -1
    def decrementPhaseDelay(self):
        if self.phaseDelayTime > 0:
            self.phaseDelayTime = self.phaseDelayTime - 1
    def incrementTimeSinceGreen(self, site):
        if self.state != site.phases.phase(self.letter).phaseType.greenName:
                self.timeSinceGreen = self.timeSinceGreen + 1 
    def stateChanges(self, site):
        oldState = self.state
        if self.move != None:
            # Phase changing colour
            if self.move == site.phases.phase(self.letter).phaseType.redName:
                # To Red
                if self.minRemaining > 0 or self.phaseDelayTime > 0:
                    # Min Times!
                    # Hold on Phase delay or say leaving amber.
                    pass
                else:
                    # Going to Red, current on postGreen, but with phase delay 0 and minRemaing = 0
                    #  So time to go Red, go red, go red .... 
                    if self.state == site.phases.phase(self.letter).phaseType.postGreenName:
                        # if currentState = postGreen then move to red as already done for example leaving amber
                        self.state = site.phases.phase(self.letter).phaseType.redName
                        self.move = None
                    else:
                        if site.phases.phase(self.letter).postGreenTime == 0:
                            # Going to Red, with postGreen = 0
                            self.state = site.phases.phase(self.letter).phaseType.redName
                            self.move = None
                        else:
                            # Going to Red, with postRed > 0 e.g. Leaving Amber
                            self.state = site.phases.phase(self.letter).phaseType.postGreenName
                            # We have already run it for one second, it we set it here.
                            self.minRemaining = site.phases.phase(self.letter).postGreenTime
            else:
            # Moving to Green
                if self.minRemaining > 0 or self.phaseDelayTime > 0:
                # Min Times!
                    pass
                else:
                    preGreenTime = site.phases.phase(self.letter).preGreenTime
                    largestIntergreen = self.largestIntergreen()
                    # If (preGreen has run or preGreen is zero) and largestIntergreen = 0
                    #     then start Green and set timeSinceGreen = 0
                    if largestIntergreen == 0:
                        if preGreenTime == 0 or self.state == site.phases.phase(self.letter).phaseType.preGreenName:
                                self.state = site.phases.phase(self.letter).phaseType.greenName
                                self.move = None
                                self.timeSinceGreen = 0
                                self.minRemaining = site.phases.phase(self.letter).greenMin
                    # Start the preGreen (e.g.Red-Amber)
                    if preGreenTime > 0 and self.state == site.phases.phase(self.letter).phaseType.redName \
                    and largestIntergreen <= preGreenTime:
                        # Need to run the preGreen
                        self.state = site.phases.phase(self.letter).phaseType.preGreenName
                        # We have already run it for one second, it we set it here.
                        self.minRemaining = site.phases.phase(self.letter).preGreenTime 
        if oldState != self.state:
            changedState = True
        else:
            changedState = False
        return changedState
    def xml(self):
        xml = "<phase>"
        xml = xml + "<letter>" + self.letter + "</letter>"
        xml = xml + "<state>" + self.state + "</state>"
        xml = xml + "<min_remaining>" + str(self.minRemaining) + "</min_remaining>"
        xml = xml + "<time_since_green>" + str(self.timeSinceGreen) + "</time_since_green>"
        xml = xml + "<move>" + str(self.move) + "</move>"
        xml = xml + "<intergreens>" 
        for intergreen in self.intergreens:
            xml = xml + intergreen.xml()
        xml = xml + "</intergreens>"
        xml = xml + "<phase_delay>" + str(self.phaseDelayTime) + "</phase_delay>"
        xml = xml + "<comments>" + str(self.comments) + "</comments>"
        xml = xml + "</phase>"
        return xml

class digramIntergreenClass:
    def __init__(self, fromLetter, remaining):
        self.fromLetter = fromLetter
        self.remaining = remaining
    def xml(self):
        xml = "<intergreen>"
        xml = xml + "<from>" + self.fromLetter + "</from>"
        xml = xml + "<remaining>" + str(self.remaining) + "</remaining>"
        xml = xml + "</intergreen>"
        return xml

class diagramMovementClass:
    def __init__(self, moveTo):
        self.moveTo = str(unicode(moveTo))
    def xml(self):
        xml = "<move>"
        xml = xml + "<to>" + self.moveTo + "</to>"
        xml = xml + "</move>"
        return xml

class diagramStageClass:
    def __init__(self):
        self.running = ""
        self.movingFrom = ""
        self.movingTo = ""
    def moveComplete(self):
        if self.movingTo:
            self.running = self.movingTo
            self.movingTo = ""
            self.movingFrom = ""
    def moveStart(self, movingTo):
        self.movingFrom = self.running
#        self.running = ""
        self.movingTo = movingTo
    def stageEnded(self):
        self.running = ""
    def xml(self):
        xml = "<stage>"
        xml = xml + "<running>" + self.running + "</running>"
        xml = xml + "<moving_from>" + self.movingFrom + "</moving_from>"
        xml = xml + "<moving_to>" + self.movingTo + "</moving_to>"
        xml = xml + "</stage>"
        return xml

class diagramTimeClass:
    def __init__(self, timeSeconds):
        self.timeSeconds = timeSeconds
        self.diagramStage = diagramStageClass()
        self.diagramPhases = []
        self.movements = []
    def diagramPhase(self, letter):
        phaseFound = False
        for diagramPhase in self.diagramPhases:
            if diagramPhase.letter == letter:
                phaseFound = True
                returnPhase = diagramPhase
        if phaseFound == False:
            returnPhase = False
        return returnPhase
    def allPhaseMovesComplete(self):
        movesComplete = True
        for phase in self.diagramPhases:
            if phase.move != None:
                movesComplete = False
        return movesComplete
    def allStageMovesComplete(self):
        movesComplete = True
        for movement in self.movements:
            if phase.moveTo != None:
                movesComplete = False
        return movesComplete
#    def updateStageStatus(self):
#        if self.movements != []:
#            self.diagramStage.moveStart(self.movements[0].moveTo)
    def primeAnyStageMovementsWaiting(self, site, lastSecondDiagram):
        if self.movements != []:
            movement = self.movements[0]
            self.movements.remove(movement)
            self.diagramStage.moveStart(movement.moveTo)
            for diagramPhase in self.diagramPhases:
                if site.stages.stage(movement.moveTo).doesContainPhase(diagramPhase.letter):
                    if diagramPhase.state != site.phases.phase(diagramPhase.letter).phaseType.greenName:
                        diagramPhase.move = site.phases.phase(diagramPhase.letter).phaseType.greenName
                        # add intergreens
                        for phase in site.phases.phases:
                            # intergreen
                            intergreenLength = site.phases.phase(diagramPhase.letter).intergreenFrom(phase.letter)
                            timeSinceGreen = lastSecondDiagram.diagramPhase(phase.letter).timeSinceGreen
                            if intergreenLength > 0:
                                if intergreenLength > timeSinceGreen:
                                    intergreen = digramIntergreenClass(phase.letter, intergreenLength - timeSinceGreen)  
                                    diagramPhase.intergreens.append(intergreen)
                                else:
                                    diagramPhase.comments = diagramPhase.comments + "Intergreen from " +  phase.letter + \
                                                            " already statified, " + phase.letter + " has not been green for " + \
                                                            str(timeSinceGreen) + " seconds. "
                else:
                    if diagramPhase.state != site.phases.phase(diagramPhase.letter).phaseType.redName:
                        diagramPhase.move = site.phases.phase(diagramPhase.letter).phaseType.redName
                        # Add phase delay (Leaving)
                        diagramPhase.phaseDelayTime = site.phases.phase(diagramPhase.letter).phaseDelay(self.diagramStage.movingFrom, self.diagramStage.movingTo)
                        if diagramPhase.phaseDelayTime > 0:
                            # Because the very next action is to reduce by one. 
                            #  This is not a fudge... really!
                            diagramPhase.phaseDelayTime = diagramPhase.phaseDelayTime +1

    def decrementIntergreens(self, site, lastSecondDiagram):
        for diagramPhase in self.diagramPhases:
            diagramPhase.decrementIntergreens(site, lastSecondDiagram)
    def decrementMinTime(self):
        for diagramPhase in self.diagramPhases:
            diagramPhase.decrementMinTime()
    def decrementPhaseDelay(self):
        for diagramPhase in self.diagramPhases:
            diagramPhase.decrementPhaseDelay()
    def stateChanges(self,site):
        changedState = False
        for diagramPhase in self.diagramPhases:
            if diagramPhase.stateChanges(site):
                changedState = True
        return changedState
    def progressTimeSinceGreen(self, site):
        for diagramPhase in self.diagramPhases:
            diagramPhase.incrementTimeSinceGreen(site)
    def xml(self):
        xml = "<time>"
        xml = xml + "<t>" + str(self.timeSeconds) + "</t>"
        xml = xml + self.diagramStage.xml()
        xml = xml + "<phases>" 
        for diagramPhase in self.diagramPhases:
            xml = xml + str(diagramPhase.xml())
        xml = xml + "</phases>"
        xml = xml + "<movements>" 
        for movement in self.movements:
            xml = xml + movement.xml()
        xml = xml + "</movements>"
        xml = xml + "</time>"
        return xml

class diagramClass:
    def __init__(self, title):
        self.title = str(unicode(title))
        self.times = []
    def atTime(self, timeSeconds):
        timeFound = False
        for time_ in self.times:
            if time_.timeSeconds == timeSeconds:
                returnTime = time_
                timeFound = True
        if timeFound:
            return returnTime
        else:
            return False
    def xml(self):
        xml = "<diagram>"
        xml = xml + "<title>" + self.title + "</title>"
        xml = xml + "<times>" 
        for time_ in self.times:
            xml = xml + str(time_.xml())
        xml = xml + "</times>" 
        xml = xml + "</diagram>"
        return xml


class requiredDiagramMovementClass:
    def __init__(self, timeSeconds, toStageName):
        self.timeSeconds = int(unicode(timeSeconds))
        self.toStageName = str(unicode(toStageName))
    def text(self):
        text = "  At " + str(self.timeSeconds) + " move to Stage " + self.toStageName + "\n"
        return text
    def xml(self):
        xml = "<move>"
        xml = xml + "<time>" + str(self.timeSeconds) + "</time>"
        xml = xml + "<to>" + self.toStageName + "</to>"
        xml = xml + "</move>"
        return xml

class requiredDiagramClass:
    def __init__(self, title, cycleTime, startingStageName, loop):
        self.title = str(unicode(title))
        self.cycleTime = int(unicode(cycleTime))
        self.startingStageName = startingStageName 
        self.loop = int(unicode(loop))
        self.movements = []
    def movementsAtTime(self, timeSeconds):
        returnMovements = []
        noMovements = True
        for movement in self.movements:
            if movement.timeSeconds == timeSeconds:
                 returnMovements.append(movement)
                 noMovements = False
        if noMovements:
            return False
        else:
            return returnMovements
    def diagramsText(self):
        diagramText = self.title + "\n"  
        diagramText = diagramText + "Cycle time: " + str(self.cycleTime) + "\n"  
        diagramText = diagramText + "Starting from stage " + str(unicode(self.startingStageName)) + "\n"  
        diagramText = diagramText + "Complete " + str(self.loop)  + " loop(s) of these movements:\n"  
        for movement in self.movements:
            diagramText = diagramText + movement.text()
        diagramText = diagramText + "\n\n"  
        return diagramText
    def xml(self):
        xml = "<diagram>"
        xml = xml + "<title>" + self.title + "</title>"
        xml = xml + "<cycle>" + str(self.cycleTime) + "</cycle>"
        xml = xml + "<start>" + str(self.startingStageName) + "</start>"
        xml = xml + "<loop>" + str(self.loop) + "</loop>"
        for movement in self.movements:
            xml = xml + str(movement.xml())
        xml = xml + "</diagram>"
        return xml

class siteClass:
    def __init__(self):
        self.address = ""
        self.comment = ""
        self.phases = phaseArrayClass()
        self.stages = stageArrayClass()
        self.requiredDiagrams = []
    def listDiagrams(self):
        listDiagrams = []
        for requiredDiagram in self.requiredDiagrams:
            listDiagrams.append(requiredDiagram.title)
        return listDiagrams
    def diagramsText(self):
        text = ""
        for requiredDiagram in self.requiredDiagrams:
            text = text + requiredDiagram.diagramsText()
        return text
    def diagram(self, title):
        diagramFound = False
        for requiredDiagram in self.requiredDiagrams:
            if requiredDiagram.title == title:
                diagramFound = True
                returnDiagram = requiredDiagram
        if diagramFound == False:
            returnDiagram = self.requiredDiagrams[0]
        return returnDiagram

    def xml(self):
        xml = "<?xml-stylesheet type=\"text/xsl\" href=\"traffic_signals_site.xsl\"?>"
        xml = xml + "<traffic_signals>"
        xml = xml + "<site>"
        xml = xml + "<address>" + str(self.address) + "</address>" 
        xml = xml + self.phases.xml() 
        xml = xml + self.stages.xml()
        xml = xml + self.phases.xmlPhaseDelay()
        xml = xml + self.phases.xmlIntergreens()
        xml = xml + "</site>"
        for requiredDiagram in self.requiredDiagrams:
            xml = xml + requiredDiagram.xml()
        xml = xml + "</traffic_signals>"
        xmlPretty = amara.parse(xml)
        return xmlPretty.xml(indent=u"yes")


class reportClass:
    def __init__(self, site):
        self.site = site
        self.diagrams = []
    def xml(self):
        xml = "<?xml-stylesheet type=\"text/xsl\" href=\"traffic_signals_report.xsl\"?>"
        xml = xml + "<traffic_signals_report>"
        xml = xml + "<address>" + str(self.site.address) + "</address>" 
        xml = xml + "<diagrams>"
        for diagram in self.diagrams:
            xml = xml + diagram.xml()
        xml = xml + "</diagrams>"
        xml = xml + "</traffic_signals_report>"
        xmlPretty = amara.parse(xml)
        return xmlPretty.xml(indent=u"yes")


def parseCountryConfig(countryXML):
    countryAmaraXML = amara.parse(countryXML)
    countryConfig = phaseTypeArrayClass()
    for phaseType in countryAmaraXML.traffic_signal_types.types.phase:
        newPhaseType = phaseTypeClass(phaseType.signal_type, phaseType.pre_green.state, phaseType.pre_green.time, 
                                      phaseType.pre_green.time.configurable, phaseType.at_green.state, 
                                      phaseType.at_green.time.configurable, phaseType.at_green.time,
                                      phaseType.post_green.state, phaseType.post_green.time, 
                                      phaseType.post_green.time.configurable, phaseType.at_red.state)
#        print phaseType.signal_type, phaseType.post_green.time.configurable
        countryConfig.phases.append(newPhaseType)
    return countryConfig


def parseSiteConfig(siteXML, countryConfig):
    siteAmaraXML = amara.parse(siteXML)
    site = siteClass()
    site.address = str(unicode(siteAmaraXML.traffic_signals.site.address))
    try:
        for phase in siteAmaraXML.traffic_signals.site.phases.phase:
            try:
                postGreenTime = int(unicode(phase.post_green_time))
            except:
                postGreenTime = -1
            try:
                # in UK this is called a black-out for pedestrians.
                postGreenTime = int(unicode(phase.black_out))
            except:
                postGreenTime = -1
            try:
                description = str(unicode(phase.description))
            except:
                description = None
            site.phases.newPhase(phase.letter, countryConfig.phaseType(phase.signal_type), greenMin=phase.mintime, postGreenTime=postGreenTime,
                                 description=description)
    except:
        pass
    try:
        for stage in siteAmaraXML.traffic_signals.site.stages.stage:
            site.stages.newStage(stage.stage_number)
            for phase in stage.phases.phase:
                site.stages.stage(stage.stage_number).phases.append(site.phases.phase(phase))
    except:
        pass
    try:
        for intergreen in siteAmaraXML.traffic_signals.site.intergreens.intergreen:
            site.phases.phase(intergreen.to).setIntergreenFrom(intergreen.from_, intergreen.length)
#            print str(intergreen.to), str(intergreen.from_), str(intergreen.length)
    except:
        pass
    try:
        for phaseDelay in siteAmaraXML.traffic_signals.site.phase_delays.phase_delay:
            site.phases.phase(phaseDelay.phase).setPhaseDelay(phaseDelay.from_, phaseDelay.to, phaseDelay.length)
    except:
        pass
    try:
        for diagram in siteAmaraXML.traffic_signals.diagrams.diagram:
            requiredDiagram = requiredDiagramClass(diagram.title, diagram.cycle, diagram.start, diagram.loop)
            for movement in diagram.movements.move:
                requiredMovement = requiredDiagramMovementClass(movement.time, movement.to)
                requiredDiagram.movements.append(requiredMovement)
            site.requiredDiagrams.append(requiredDiagram)
    except:
        pass
    return site


def staringPoint(site, startingStageName):
    startingtime = diagramTimeClass(-1)
    for phase in site.phases.phases:
        if site.stages.stage(startingStageName).doesContainPhase(phase.letter):
            diagramPhase = diagramPhaseClass(phase.letter, state=phase.phaseType.greenName, timeSinceGreen=0)
        else:
            diagramPhase = diagramPhaseClass(phase.letter, state=phase.phaseType.redName)
        startingtime.diagramPhases.append(diagramPhase)
    startingtime.diagramStage.running = str(unicode(startingStageName))
    return startingtime

def nextSecondOfDiagram(countryConfig, site, diagramRequired, diagram, timeSeconds):
    nextSecond = copy.deepcopy(diagram.atTime(timeSeconds-1))
    nextSecond.timeSeconds = timeSeconds
    return nextSecond

def copyLastSecondPhases(lastSecondPhases):
    returnPhases = copy.deepcopy(lastSecondPhases)
    for diagramPhase in returnPhases:
        diagramPhase.comments =  ""
    return returnPhases
 
def copyLastSecondStage(lastSecondStage):
    return copy.deepcopy(lastSecondStage)


def nextSecondsStageMovements(lastSecondMovements, diagramRequired, cycleTime):
    movements = copy.deepcopy(lastSecondMovements)
    if diagramRequired.movementsAtTime(cycleTime):
        for movement in diagramRequired.movementsAtTime(cycleTime):
            newMovement = diagramMovementClass(movement.toStageName)
            movements.append(newMovement)
    return movements


def generateDigram(countryConfig, site, diagramRequired, gtk, progressbar):
    diagram = diagramClass(diagramRequired.title)
    diagram.times.append(staringPoint(site, diagramRequired.startingStageName))
    timeSeconds = 0
    for loop in range(0, diagramRequired.loop):
        for cycleTime in range(0, diagramRequired.cycleTime):
            nextSecond = diagramTimeClass(timeSeconds)
            nextSecond.movements = nextSecondsStageMovements(diagram.atTime(timeSeconds-1).movements, diagramRequired, cycleTime)
            nextSecond.diagramPhases = copyLastSecondPhases(diagram.atTime(timeSeconds-1).diagramPhases)
            nextSecond.diagramStage = copyLastSecondStage(diagram.atTime(timeSeconds-1).diagramStage)
            if diagram.atTime(timeSeconds-1).allPhaseMovesComplete():
                nextSecond.diagramStage.moveComplete()
                nextSecond.primeAnyStageMovementsWaiting(site, diagram.atTime(timeSeconds-1))
            nextSecond.decrementIntergreens(site, diagram.atTime(timeSeconds-1))
            nextSecond.decrementMinTime()
            nextSecond.decrementPhaseDelay()
            if nextSecond.stateChanges(site):
                nextSecond.diagramStage.stageEnded()
            if nextSecond.allPhaseMovesComplete():
                nextSecond.diagramStage.moveComplete()
                nextSecond.primeAnyStageMovementsWaiting(site, nextSecond)
            if nextSecond.stateChanges(site):
                nextSecond.diagramStage.stageEnded()
            nextSecond.progressTimeSinceGreen(site)

            diagram.times.append(nextSecond)
            timeSeconds = timeSeconds + 1

            # Update GTK if GTK passed ...
            if gtk != None:
                progressbar.pulse()
                while gtk.events_pending():
                    gtk.main_iteration_do(False)

    return diagram


def generateReport(countryConfig, site, gtk=None, progressbar=None):
    report = reportClass(site)
    for diagramRequired in site.requiredDiagrams:
        diagram = generateDigram(countryConfig, site, diagramRequired, gtk, progressbar)
        report.diagrams.append(diagram)
    return report

def writeReportToFile(report, output):
    f=open(output, 'w')
    f.write(report.xml())
    f.close()


def main():
    usage = "usage: %prog [options] --type=COUNTRY.XML --site=SITE.XML --output=OUTPUT.XML\n       %prog --help for all options"
    parser = OptionParser(usage, version="%prog ")
    parser.add_option("-t", "--type", dest="country",
                      help="use type of signals as definined in the xml template")
    parser.add_option("-o", "--output", dest="output",
                      help="Store the created image as filename OUTPUT")
    parser.add_option("-s", "--site", dest="site",
                      help="Use site.xml as the input site")
    (options, args) = parser.parse_args() 
    if not options.country or not options.site or not options.output:
        parser.error("Must set country, site and output")
#    countryConfig = amara.parse(options.country)
    countryConfig = parseCountryConfig(options.country)
    site = parseSiteConfig(options.site, countryConfig)
    report = generateReport(countryConfig, site)
    writeReportToFile(report, options.output)
    print site.xml()
#    test_phases()

if __name__ == "__main__":
    main()
