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
import curses

import libdetermine



class signalTimerClass:
    def __init__(self, interval = 1):
        self.interval = interval
        self.lastTime = time.time()
    def pause(self):
        finish = self.lastTime + self.interval - time.time()
        if finish > 0:
            time.sleep(finish)
            self.lastTime = self.lastTime + self.interval
        else:
            raise Exception, "Running too slow."
        

def printStatus(myscreen, currentState):
    y = 0
    myscreen.clear()
    for phase in currentState.diagramPhases:
        myscreen.addstr(y, 0, phase.letter )
        myscreen.addstr(y, 4, phase.state )
        y = y +1
    myscreen.refresh()
    # diagramPhases
        #self.letter = letter
     #   self.state = state


def startingAllRed(site):
    startingtime = libdetermine.diagramTimeClass(-1)
    for phase in site.phases.phases:
        diagramPhase = libdetermine.diagramPhaseClass(phase.letter, state=phase.phaseType.redName)
        startingtime.diagramPhases.append(diagramPhase)
    # Start from stage 0
    startingtime.diagramStage.running = str(0)
    return startingtime


def switchOn(countryConfig, site):
    timeSeconds = 0
    currentState = startingAllRed(site)
    signalTimer = signalTimerClass()
    myscreen = curses.initscr()
    curses.curs_set(0)
    
    while True:
        # Prepare the next second. Load sateg movement and phase and stage configs
        nextSecond = libdetermine.diagramTimeClass(timeSeconds)
        nextSecond.movements = site.methodOfControl.getMovements()
        nextSecond.diagramPhases = libdetermine.copyLastSecondPhases(currentState.diagramPhases)
        nextSecond.diagramStage = libdetermine.copyLastSecondStage(currentState.diagramStage)

        # Have we done all the Phase changed needed ? - If so load any queued moves
        if currentState.allPhaseMovesComplete():
            nextSecond.diagramStage.moveComplete()
            nextSecond.primeAnyStageMovementsWaiting(site, currentState)
        nextSecond.decrementPhaseDelay()
        nextSecond.decrementIntergreens(site, currentState)
        nextSecond.decrementMinTime()
        
        # If some phases did change - are we at the end of a stage
        if nextSecond.stateChanges(site, currentState):
            nextSecond.diagramStage.stageEnded()
        nextSecond.terminatedByOthers(site, nextSecond)
        
        # After all that may (AGAIN) be at the end of phase changes.
        if nextSecond.allPhaseMovesComplete():
            nextSecond.diagramStage.moveComplete()
            nextSecond.primeAnyStageMovementsWaiting(site, nextSecond)

        # AGAIN If some phases did change - are we at the end of a stage            
        if nextSecond.stateChanges(site, currentState):
            nextSecond.diagramStage.stageEnded()
        nextSecond.progressTimeSinceGreen(site)

        # Everything ready just wait until the right time to change the signals.
        signalTimer.pause()
        currentState = nextSecond          
        
        printStatus(myscreen, currentState)

#        xmlPretty = amara.parse(nextSecond.xml())
#        print xmlPretty.xml(indent=u"yes")


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

    countryConfig = libdetermine.parseCountryConfig(options.country)
    site = libdetermine.parseSiteConfig(options.site, countryConfig)
    switchOn(countryConfig, site)
    #    test_phases()

if __name__ == "__main__":
    main()
