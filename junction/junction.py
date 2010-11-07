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
import time

import libdetermine

    

def startingAllRed(site):
    startingtime = libdetermine.diagramTimeClass(-1)
    for phase in site.phases.phases:
        diagramPhase = libdetermine.diagramPhaseClass(phase.letter, state=phase.phaseType.redName)
        startingtime.diagramPhases.append(diagramPhase)
    startingtime.diagramStage.running = str(0)
    return startingtime

def getMovements(methodOfControl):
    movements = []
    methodOfControl.currentMoC.tick()    
    for movement in methodOfControl.currentMoC.getMovements():
        newMovement = libdetermine.diagramMovementClass(movement.toStageName)
        movements.append(newMovement)
    return movements



def switchOn(countryConfig, site):
    timeSeconds = 0
    currentState = startingAllRed(site)
    
    print currentState.xml()
    
    for loop in range(0, 120):
        nextSecond = libdetermine.diagramTimeClass(timeSeconds)
        nextSecond.movements = getMovements(site.methodOfControl)
        nextSecond.diagramPhases = libdetermine.copyLastSecondPhases(currentState.diagramPhases)
        nextSecond.diagramStage = libdetermine.copyLastSecondStage(currentState.diagramStage)

        if currentState.allPhaseMovesComplete():
            nextSecond.diagramStage.moveComplete()
            nextSecond.primeAnyStageMovementsWaiting(site, currentState)
        nextSecond.decrementPhaseDelay()
        nextSecond.decrementIntergreens(site, currentState)
        nextSecond.decrementMinTime()


        if nextSecond.stateChanges(site, currentState):
            nextSecond.diagramStage.stageEnded()
        nextSecond.terminatedByOthers(site, nextSecond)
        if nextSecond.allPhaseMovesComplete():
            nextSecond.diagramStage.moveComplete()
            nextSecond.primeAnyStageMovementsWaiting(site, nextSecond)
        if nextSecond.stateChanges(site, currentState):
            nextSecond.diagramStage.stageEnded()
        nextSecond.progressTimeSinceGreen(site)

        xmlPretty = amara.parse(nextSecond.xml())
        print xmlPretty.xml(indent=u"yes")


        currentState = copy.deepcopy(nextSecond)
        
#        print currentState.xml()
        time.sleep(1)



def main():
    usage = "usage: %prog [options] --type=COUNTRY.XML --site=SITE.XML \n       %prog --help for all options"
    parser = OptionParser(usage, version="%prog ")
    parser.add_option("-t", "--type", dest="country",
                      help="use type of signals as definined in the xml template")
    parser.add_option("-s", "--site", dest="site",
                      help="Use site.xml as the input site")
    (options, args) = parser.parse_args() 
    if not options.country or not options.site:
        parser.error("Must set country, site and output")
#    countryConfig = amara.parse(options.country)
    print "Hello World"
    countryConfig = libdetermine.parseCountryConfig(options.country)
    site = libdetermine.parseSiteConfig(options.site, countryConfig)
    switchOn(countryConfig, site)
    #    test_phases()

if __name__ == "__main__":
    main()
