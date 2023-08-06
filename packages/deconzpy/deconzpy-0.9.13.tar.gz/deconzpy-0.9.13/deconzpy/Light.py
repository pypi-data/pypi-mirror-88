#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from .BaseElement import DeconzBaseElement

import logging
logger = logging.getLogger(__name__)


class Light(DeconzBaseElement):
    """ Repraesentation eines Lichts """
    class State:
        """ ein Status eines Lichts """
        brightness = None
        colorTemperatur = 0
        hue = -1
        on = None
        sat = -1
        xy = [0, 0]
        alert = None

        def __init__(self, prevState=None):
            pass

        # 	if prevState != None:
        # 		self.brightness = prevState.brightness
        # 		self.colormode = prevState.colormode
        # 		self.colorTemperatur = prevState.colorTemperatur
        # 		self.hue = prevState.hue
        # 		self.on = prevState.on
        # 		self.sat = prevState.sat
        # 		self.xy = prevState.xy

    def __init__(self, id, arr, urlRoot):
        DeconzBaseElement.__init__(self, id, arr, urlRoot)
        self.stateStack = {0: Light.State()}
        #set defaults
        if self.getAttribute("state_bri") != None:
            self.stateStack[0].brightness = 0 
        if self.getAttribute("state_on") != None:
            self.stateStack[0].on = False
        self.highestStateId = 0  # highest state id

    def __getOrAddState(self, prio):
        state = None
        if prio not in self.stateStack:
            # if adding a new higher state
            if prio > self.highestStateId:
                self.highestStateId = prio
            state = Light.State()
            self.stateStack[prio] = state
        return self.stateStack[prio]

    def getName(self):
        return self.getAttribute("name")

    def getManufacturer(self):
        return self.getAttribute("manufacturername")

    def getType(self):
        return self.getAttribute("type")

    def isOn(self):
        return self.getAttribute("state_on")

    def isReachable(self):
        return self.getAttribute("state_reachable")

    def setBrightness(self, value, statePrio=10, transitiontime=10):
        newState = self.__getOrAddState(statePrio)
        newState.brightness = value
        if statePrio >= self.highestStateId:
            logger.info(
                "new high prio last: %s new: %s", str(
                    self.highestStateId), str(statePrio))
            self.__setSate(newState)

    def getBrightness(self):
        return self.getAttribute("state_bri")

    def setColorTemperatur(self, value, statePrio=10, transitiontime=10):
        newState = self.__getOrAddState(statePrio)
        if ( value is not None
             and value >= 153
             and value <= 500 ):
            logger.info("ct max %s ct min %s", self.getAttribute("ctmax"), self.getAttribute("ctmin"))
            # check for light specific min max and adapt
            if (self.getAttribute("ctmax") is not None
                and value > self.getAttribute("ctmax")):
                newState.colorTemperatur = self.getAttribute("ctmax")
            elif (self.getAttribute("ctmin") is not None
                and value < self.getAttribute("ctmin")):
                newState.colorTemperatur = self.getAttribute("ctmin")
            else:
                newState.colorTemperatur = int(value)
        else:
            logger.warn("Color Temperatur out of range")
        if statePrio >= self.highestStateId:
            logger.info(
                "new high prio last: %s new: %s", str(
                    self.highestStateId), str(statePrio))
            self.__setSate(newState)

    def getColorTemeratur(self):
        return self.getAttribute("state_ct")

    def actionOn(self, statePrio=10, transitiontime=10, brightness=None, colorTemperatur=None):
        newState = self.__getOrAddState(statePrio)
        newState.on = True
        if brightness is not None:
            if brightness >= 0 and brightness <= 255:
                newState.brightness = int(brightness)
            else:
                newState.brightness = 255

        #dublicating code her is not pretty, but i dont see any simple beautifull solution
        if ( colorTemperatur is not None
             and colorTemperatur >= 153
             and colorTemperatur <= 500 ):
            # check for light specific min max and adapt
            if (self.getAttribute("ctmax") is not None
                and colorTemperatur > self.getAttribute("ctmax")):
                newState.colorTemperatur = self.getAttribute("ctmax")
            elif (self.getAttribute("ctmin") is not None
                and colorTemperatur < self.getAttribute("ctmin")):
                newState.colorTemperatur = self.getAttribute("ctmin")
            else:
                newState.colorTemperatur = int(colorTemperatur)

        if statePrio >= self.highestStateId:
            logger.info(
                "new high prio last: %s new: %s", str(
                    self.highestStateId), str(statePrio))
            self.__setSate(newState)

    # switch light off and flush stack
    def actionOff(self):
        newState = self.__getOrAddState(0)
        newState.on = False
        self.__setSate(newState)
        # clean up stack
        for key in list(self.stateStack.keys()):
            if key != 0:
                del self.stateStack[key]
        # reset highest state
        self.highestStateId = 0

    def setAlert(self, statePrio=10, alert="select"):
        logger.info("LIGHT %s set alert", self.getName())
        newState = self.__getOrAddState(statePrio)
        newState.alert = alert
        self.__setSate(newState)

    def stopAlert(self, statePrio=10):
        self.setAlert(statePrio=statePrio, alert="none")

    def __setSate(self, state):
        jsonObj = {}
        if state.alert != None: #self.stateStack[self.highestStateId].alert:
            jsonObj["alert"] = state.alert
            logger.info("LIGHT %s update state - %s/%s/state - %s", str(self.getId()), self.getUrlRoot(), self.getId(), str(jsonObj))
            r = requests.put(self.getUrlRoot() + "/" + self.getId() + "/state",json=jsonObj,timeout=3 )
            if not r:
                logger.warn("Some Error in update state: %s",r.text)
        # todo check if different from current setting
        jsonObj = {}  # {"transitiontime": 10}
        if ( state.colorTemperatur >= 153
             and state.colorTemperatur <= 500
             and self.getColorTemeratur() != state.colorTemperatur ):
            jsonObj["ct"] = state.colorTemperatur

        if state.hue >= 0 and state.hue <= 65535:
            jsonObj["hue"] = state.hue
        if state.sat >= 0 and state.sat <= 255:
            jsonObj["sat"] = state.sat
        if jsonObj != {}:  # {"transitiontime": 10}:
            if "IKEA" in self.getManufacturer() or "dresden" in self.getManufacturer():
                if state.on != self.isOn():
                    jsonObj["on"] = state.on 
                logger.info("LIGHT %s update state - %s/%s/state - %s", str(self.getId()), self.getUrlRoot(), self.getId(), str(jsonObj))
                r = requests.put(self.getUrlRoot() + "/" + self.getId() + "/state",json=jsonObj,timeout=3 )
                if not r:
                    logger.warn("Some Error in update state: %s",r.text)
        jsonObj = {}  # {"transitiontime": 10}
        if (state.brightness != None and state.brightness >= 0 and state.brightness <= 255 and self.getBrightness() != state.brightness):
            jsonObj["bri"] = state.brightness
        if state.on != None and state.on != self.isOn():
            jsonObj["on"] = state.on
        if state.brightness != None and state.brightness == 0:
            jsonObj["on"] = False
            state.on = False
        if jsonObj != {}:  # {"transitiontime": 10}:
            logger.info("LIGHT %s update state - %s/%s/state - %s", str(self.getId()), self.getUrlRoot(), self.getId(), str(jsonObj))
            r = requests.put(self.getUrlRoot() + "/" + self.getId() + "/state",json=jsonObj,timeout=3 )
            if not r:
                logger.warn("LIGHT %s Some Error in update state: %s", self.getName(), r.text)

    def hasState(self, prio):  # check weather prio is still in stack
        return prio in self.stateStack

    def revokeState(self, prio):
        logger.info("%s revoke State: %s", self.getName(), str(prio))
        if prio == 0:
            # wont revoke this
            return
        if prio in self.stateStack:
            del self.stateStack[prio]
        # find highest prio
        hId = None
        for prio, state in self.stateStack.items():
            if hId is None or prio > hId:
                hId = prio
        # wenn neuer aktueller status dann setzten
        if self.highestStateId != hId:
            logger.info("%s revoke set new State: %s", self.getName(), str(hId))
            self.highestStateId = hId
            self.__setSate(self.stateStack[hId])

    def println(self):
        color = int(self.getId()) % 7
        print("\x1b[1;3" +
              str(color +
                  1) +
              ";40m" +
              "{:2d} : ".format(int(self.getId())) +
              " {:7.7s} - {:30s}".format(self.getManufacturer(), self.getName()), " - " +
              self.getType() +
              "\x1b[0m", )
