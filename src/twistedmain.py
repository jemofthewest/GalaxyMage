from twisted.internet import reactor, defer
from twisted.spread import pb
from twisted.python import util, failure
from twisted.cred import checkers, portal, credentials
from zope import interface

import gui.MainWindow
import gui.ScenarioGUI
import logging
import Resources
import Main

serverLog = logging.getLogger('gsrv')
clientLog = logging.getLogger('gcli')

import engine.netsupport

############################ COMMON

# Each Avatar can call some methods on the server. A GameCreator can
# call all methods, a GamePlayer can call most methods (everything
# needed to actually play in a game), and a GameObserver has the least
# access (they can only watch.)
class Access(object):
    CREATOR = "Creator"
    PLAYER = "Player"
    OBSERVER = "Observer"

class GameObserver(pb.Avatar):
    def __init__(self, server, clientRef, name):
        self.clientRef = clientRef
        self.accessLevel = Access.OBSERVER
        self.server = server
        self.gameState = server.state
        self.name = name
        self.faction = None

    def perspective_info(self, version):
        if Main.__version__ != version:
            err = ("Your version of GalaxyMage (%s) does not match the server's (%s)." %
                   (version, Main.__version__))
            raise Exception(err)
        return self.name, self.accessLevel, self.faction

    def perspective_chat(self, message):
        self.server.remoteAll('chat', self.name, message)

    def perspective_readyForGame(self):
        self.server.clients[self.clientRef].readyForGame = True

    def perspective_readyToDisplay(self):
        self.server.clients[self.clientRef].readyToDisplay = True

class GamePlayer(GameObserver):
    def __init__(self, server, clientRef, name):
        GameObserver.__init__(self, server, clientRef, name)
        self.accessLevel = Access.PLAYER

    def perspective_unitMove(self, x, y):
        return self.gameState.unitMove(self, int(x), int(y))

    def perspective_unitAct(self, abilityID, x, y):
        return self.gameState.unitAct(self, int(abilityID), int(x), int(y))

    def perspective_unitFacing(self, facing):
        return self.gameState.unitFacing(self, int(facing))
        
class GameCreator(GamePlayer):
    def __init__(self, server, clientRef, name):
        GamePlayer.__init__(self, server, clientRef, name)
        self.accessLevel = Access.CREATOR
            
    def perspective_setScenario(self, campaign, scenario):
        clientLog.debug("Set campaign and scenario to %s/%s" %
                        (campaign, scenario))
        return self.server.state.setScenario(campaign, scenario)

############################ CLIENT

class GameClient(pb.Referenceable):
    """Client interface. Handles talking to the server but doesn't
    take any real actions or start any GUI."""
    def __init__(self, server, serverPort, username):
        self.server = server
        self.serverPort = serverPort
        self.username = username
        self.perspective = None
        self.accessLevel = Access.OBSERVER
        self.name = None
        self.faction = None
        self.scenario = None
        self.start()
        self.unit = None # FIXME: remove

    def start(self):
        # Start connection to the PB server
        factory = pb.PBClientFactory()
        reactor.connectTCP(self.server,
                           self.serverPort,
                           factory)
        # log in with username and blank password
        c = credentials.UsernamePassword(self.username, "")
        df = factory.login(c, self)
        df.addCallback(self.gotPerspective)
        df.addErrback(lambda e: self.error(e, "logging in to %s" %
                                           self.server))

    # Methods starting with remote_ can be called by the server.
    def remote_startGame(self, scenario):
        self.scenario = scenario
        for u in scenario.units():
            scenario.map().squares[u.x()][u.y()].unit = u

    def remote_chat(self, username, message):
        pass

    def remote_serverMessage(self, message):
        pass

    def remote_unitBeginTurn(self, unitID):
        self.unit = self.scenario.unitFromID(unitID)

    def remote_unitUpdate(self, unitID, newUnit):
        unit = self.scenario.unitFromID(unitID)
        unit.update(newUnit)
        if not unit.alive():
            self.scenario.map().squares[unit.x()][unit.y()].unit = None

    # FIXME: for sanity's sake, need to send unitIDs with all of these
    # so that the right unit is guaranteed to be affected even if
    # lagmonster happens - I think this is fixed now, 2006-Mar-25
    def remote_unitMoveActCancel(self, move, act, cancel):
        pass

    def remote_unitMoved(self, x, y):
        # Actually move the unit on our map
        m = self.scenario.map()
        m.squares[self.unit.x()][self.unit.y()].unit = None
        m.squares[x][y].unit = self.unit
        # FIXME: we should set the unit posn here but that screws up
        # the GUI

    def remote_unitSetFacing(self, facing):
        self.unit.setFacing(facing)

    def remote_actionResults(self, actionResults):
        pass

    def remote_actionPerformed(self, abilityID):
        pass

    # Utility function for calling a remote method on the server. Adds
    # a sensible errback.
    def remote(self, methodName, *args):
        df = self.perspective.callRemote(methodName, *args)
        op = "%s%s" % (methodName, str(args))
        df.addErrback(self.error, op)
        return df

    def error(self, failure, op=""):
        clientLog.error('Error in %s: %s' %
                        (op, str(failure.getErrorMessage())))
        if reactor.running:
            reactor.stop()

    def gotPerspective(self, perspective):
        """Called after a successful login to the server."""
        self.perspective = perspective
        df = self.remote('info', Main.__version__)
        df.addCallback(self.gotInfo)

    def gotInfo(self, (name, accessLevel, faction)):
        self.name = name
        self.faction = faction
        self.accessLevel = accessLevel
        self.remote('readyForGame')

class InteractiveClient(GameClient):
    """Interactive client -- the normal player GUI."""
    def __init__(self, server, serverPort, username, scenario, aiPlayers,
                 window):
        self.window = window
        self.scenarioGUI = None
        self.scenarioName = scenario
        self.aiPlayers = aiPlayers
        GameClient.__init__(self, server, serverPort, username)

    def gotInfo(self, (name, accessLevel, faction)):
        GameClient.gotInfo(self, (name, accessLevel, faction))
        clientLog.debug("Access level set to %s" % self.accessLevel)
        if self.accessLevel == Access.CREATOR:        
            # FIXME: set scenario name from in-game, not command-line only
            df = self.remote('setScenario',
                             'demo', # FIXME: allow setting campaign
                             self.scenarioName)
            for i in xrange(0, self.aiPlayers):
                ai = AIClient(self.server, self.serverPort)

    def gotPerspective(self, perspective):
        GameClient.gotPerspective(self, perspective)

    def remote_startGame(self, scenario):
        GameClient.remote_startGame(self, scenario)
        self.scenarioGUI = gui.ScenarioGUI.ScenarioGUI(self,
                                                       scenario,
                                                       self.faction)
        self.window.setDelegate(self.scenarioGUI)

    def remote_chat(self, username, message):
        self.scenarioGUI.showMessage("<%s> %s" % (username, message))

    def remote_serverMessage(self, message):
        if self.scenarioGUI != None:
            self.scenarioGUI.showMessage("*** %s" % message)

    def remote_unitBeginTurn(self, unitID):
        GameClient.remote_unitBeginTurn(self, unitID)
        self.scenarioGUI.activateUnit(self.unit)

    def remote_unitMoveActCancel(self, move, act, cancel):
        self.scenarioGUI.moveActCancel(move, act, cancel)   

    def remote_unitMoved(self, x, y):
        GameClient.remote_unitMoved(self, x, y)
        self.scenarioGUI.moveUnit(x, y)
        
    def remote_unitSetFacing(self, facing):
        GameClient.remote_unitSetFacing(self, facing)
        reactor.callLater(1.0, self.remote, 'readyToDisplay')
        
    def remote_actionResults(self, actionResults):
        for unitID, results in actionResults.items():
            self.scenarioGUI.showActionResults(unitID, results)
        reactor.callLater(1.0, self.remote, 'readyToDisplay')
        
    def remote_actionPerformed(self, abilityID):
        self.scenarioGUI.showActionPerformed(abilityID)

### AI Client
import ai.UnitAI
import FSM
import engine.Battle
from twisted.internet import threads
        
class AIFSM(FSM.FSM):
    def __init__(self, aiClient):
        FSM.FSM.__init__(self, ['disabled', 'begin', 'calc'])
        for s in self.states:
            self.addEntryHook(s, getattr(self, "enter_" + s, self.doNothing))
        self.aiClient = aiClient
        self.unit = None
        self.turn = None
        
    def enter_begin(self, oldState, unitID):
        self.unit = self.aiClient.scenario.unitFromID(unitID)

    def enter_calc(self, oldState, (move, act, cancel)):
        self.unit.setMoveActCancel(move, act, cancel)
        unitAI = ai.UnitAI.Exhaustive(self.unit)
        df = threads.deferToThread(unitAI.calc,
                                   self.aiClient.scenario.battle())
        df.addCallback(self.executeTurn)

    def executeTurn(self, turn):
        self.turn = turn
        if turn.turnOrder() == engine.Battle.UnitTurn.MOVE_FIRST:
            if turn.moveTarget() != None:
                self.aiClient.remote('unitMove',
                                     *turn.moveTarget())
            if turn.action() != None:
                self.aiClient.remote('unitAct',
                                     turn.action().abilityID,
                                     *turn.actionTarget())
            self.aiClient.remote('unitFacing', turn.facing())
        else:
            raise NotImplemented("AI turn order = act-first")

    def doNothing(self, *args):
        pass

# FIXME: clean up AIclient, don't need AIFSM class
class AIClient(GameClient):
    """AI client -- just sends moves to the server when needed."""
    def __init__(self, server, serverPort):
        GameClient.__init__(self, server, serverPort, "AI")
        self.fsm = AIFSM(self)
    
    def remote_unitBeginTurn(self, unitID):
        GameClient.remote_unitBeginTurn(self, unitID)
        self.fsm.trans('begin', unitID)
    
    def remote_unitMoveActCancel(self, move, act, cancel):
        if self.fsm.state == 'begin':
            self.fsm.trans('calc', (move, act, cancel))

    def remote_unitMoved(self, x, y):
        GameClient.remote_unitMoved(self, x, y)
        self.unit.setPosn(x, y, self.scenario.map().squares[x][y].z)
        self.remote('readyToDisplay')

    def remote_unitSetFacing(self, facing):
        GameClient.remote_unitSetFacing(self, facing)
        self.remote('readyToDisplay')

    def remote_actionResults(self, *args):
        GameClient.remote_actionResults(self, *args)
        self.remote('readyToDisplay')

########################### SERVER

class UnitState(object):
    def __init__(self, unit, controller):
        self.unit = unit
        self.controller = controller
        self.originalPosn = unit.posn()

    def moveActCancel(self):
        return self.unit.hasMove(), self.unit.hasAct(), self.unit.hasCancel()

class GameState(object):
    WAITING_FOR_PLAYERS = 0
    PLAYING = 1
    DONE = 2
    
    def __init__(self, server):
        self.server = server
        self.scenario = None
        self.state = GameState.WAITING_FOR_PLAYERS
        self.unitState = None
        self.factions = {}
        self.clientCommandQueue = []
        
    def setScenario(self, campaign, scenario):
        # FIXME SECURITY: scenarios and campaigns should only be a
        # simple string; for security reasons we need to make sure
        # they don't contain weird characters like "..", "/", or "."
        Resources.setCampaign(campaign)
        self.scenario = Resources.scenario(scenario)
        self.scenario.numPlayers = 2 # FIXME: should be defined by the scenario

    def update(self):
        self._update()
        reactor.callLater(0.1, self.update)

    def _update(self):
        # If we've collected enough players, start the game
        if self.state == GameState.WAITING_FOR_PLAYERS:
            if not self.scenario:
                return
            readyPlayers = 0
            for c in self.server.clients.values():
                if c.readyForGame:
                    readyPlayers += 1
            if readyPlayers == self.scenario.numPlayers:
                self.startGame()
            return
        # If we need a new unit, pick one
        if self.state == GameState.PLAYING and self.clientsReadyToDisplay():
            b = self.scenario.battle()
            if b.status() != -1:
                self.clientCommandQueue.append(('battleStatus', (b.status(),)))
            if b.activeUnit == None:
                unit = b.pickNextUnit()
                controller = self.factions[unit.faction()]
                self.unitState = UnitState(unit, controller)
                self.server.remoteAll('unitBeginTurn', unit.unitID)
                self.server.remote(controller.ref, 'unitMoveActCancel',
                                   *self.unitState.moveActCancel())
            if self.clientCommandQueue:
                commandName, args = self.clientCommandQueue.pop(0)
                self.setClientsReadyToDisplay(False)
                if commandName == 'unitMove':
                    self.sendUnitMove(*args)
                elif commandName == 'unitAct':
                    self.sendUnitAct(*args)
                elif commandName == 'unitFacing':
                    self.sendUnitFacing(*args)
                elif commandName == 'battleStatus':
                    self.sendBattleStatus(*args)
                
    def startGame(self):
        self.factions = {}
        self.state = GameState.PLAYING
        self.server.remoteAll('startGame', self.scenario)
        for c in self.server.clients.values():
            self.factions[c.faction] = c
        self.setClientsReadyToDisplay(True)

    def clientsReadyToDisplay(self):
        for c in self.server.clients.values():
            if not c.readyToDisplay:
                return False
        return True

    def setClientsReadyToDisplay(self, ready):
        for c in self.server.clients.values():
            c.readyToDisplay = ready       

    def unitController(self, client):
        return client.faction == self.unitState.unit.faction()

    def unitMove(self, client, x, y):
        if not self.unitController(client):
            return False
        result = self.scenario.battle().unitMoved(x, y)
        if not result:
            return False
        self.clientCommandQueue.append(('unitMove', (client, x, y)))
        return True

    def sendBattleStatus(self, winner):
        for c in self.server.clients.values():
            if c.faction == winner:
                self.server.remote(c.ref,
                                   'serverMessage', 'You win!')
            else:
                self.server.remote(c.ref,
                                   'serverMessage', 'You lose!')
        self.state = GameState.DONE
        reactor.callLater(10, reactor.stop)

    def sendUnitMove(self, client, x, y):
        self.server.remote(client, 'unitMoveActCancel',
                           *self.unitState.moveActCancel())
        self.server.remoteAll('unitMoved', x, y)

    def unitAct(self, client, abilityID, x, y):
        if not self.unitController(client):
            return False
        ability = engine.Ability.Ability.get[abilityID]
        result = self.scenario.battle().unitActed(ability, x, y)
        if not result:
            return False
        affectedUnits, allEffectResults = result
        self.clientCommandQueue.append(('unitAct',
                                        (client, abilityID, affectedUnits,
                                         allEffectResults)))
        return True

    def sendUnitAct(self, client, abilityID, affectedUnits, allEffectResults):
        # FIXME: put actionPerformed and actionResults into one
        # message
        self.server.remoteAll('actionPerformed', abilityID)
        self.server.remoteAll('actionResults', allEffectResults)
        for u in affectedUnits:
            self.server.remoteAll('unitUpdate', u.unitID, u)
        self.server.remote(client, 'unitMoveActCancel',
                           *self.unitState.moveActCancel())


    def unitFacing(self, client, facing):
        if not self.unitController(client):
            return False
        result = self.scenario.battle().unitSetFacing(facing)
        if not result:
            return False
        self.clientCommandQueue.append(('unitFacing', (facing,)))
        return True
    
    def sendUnitFacing(self, facing):
        self.server.remoteAll('unitSetFacing', facing)
        self.scenario.battle().unitDone()

class ClientInfo(object):
    nextFaction = 0
    
    def __init__(self, ref, name, address, accessLevel):
        self.ref = ref
        self.address = address
        self.accessLevel = accessLevel
        self.name = name
        self.faction = ClientInfo.nextFaction
        self.readyForGame = False
        self.readyToDisplay = True
        ClientInfo.nextFaction += 1

    def __str__(self):
        return "%s (%s:%s)" % (self.name, self.address.host, self.address.port)

class UsernameChecker(object):
    interface.implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def __init__(self):
        self.users = {}

    def requestAvatarId(self, credentials):
        name = credentials.username
        i = 2
        while name in self.users:
            name = credentials.username + str(i)
            i += 1
        self.users[name] = True
        return defer.succeed(name)

class GameServer(object):
    interface.implements(portal.IRealm)
    
    def __init__(self, port):
        self.port = port
        self.state = GameState(self)
        self.clients = {} # maps clientRef -> ClientInfo
        self.start()
        serverLog.info('Listening on port %d' % self.port)

    def start(self):
        p = portal.Portal(self)
        c = UsernameChecker()
        p.registerChecker(c)
        reactor.listenTCP(self.port, pb.PBServerFactory(p))
        self.state.update()

    def error(self, failure, op=""):
        if failure.type == pb.PBConnectionLost:
            return
        serverLog.warn('Error in %s: %s' %
                       (op, str(failure.getErrorMessage())))

    def requestAvatar(self, name, clientRef, *interfaces):
        """This is what gets called when a client logs in."""
        if pb.IPerspective not in interfaces:
            raise NotImplementedError
        perspectiveClass = None
        if len(self.clients) == 0:
            perspectiveClass = GameCreator
        else:
            perspectiveClass = GamePlayer
        address = clientRef.broker.transport.getPeer()
        perspective = perspectiveClass(self, clientRef, name)
        clientInfo = ClientInfo(clientRef, name, address,
                                perspective.accessLevel)
        perspective.faction = clientInfo.faction
        self.clients[clientRef] = clientInfo
        serverLog.debug('%s connected (total clients: %d)' %
                        (clientInfo, len(self.clients)))
        self.remoteAll('serverMessage', "%s connected (%d players total)" %
                       (name, len(self.clients)))
        return (perspectiveClass, perspective,
                lambda: self.handleDisconnect(clientRef))

    def handleDisconnect(self, client):
        clientInfo = self.clients[client]
        del self.clients[client]
        serverLog.debug('%s disconnected (total clients: %d)' %
                        (clientInfo, len(self.clients)))
        self.remoteAll('serverMessage', "%s disconnected (%d players total)" %
                       (clientInfo.name, len(self.clients)))


    def remote(self, client, methodName, *args):
        if isinstance(client, GameObserver):
            client = client.clientRef
        df = client.callRemote(methodName, *args)
        op = "%s%s" % (methodName, str(args))
        df.addErrback(self.error, op)
        return df

    def remoteAll(self, methodName, *args):
        dfs = [self.remote(c, methodName, *args) for c in self.clients]
        return dfs          

class GameServerException(Exception):
    pass

########################################### MAIN

import gui.ScenarioChooser

window = None
opts = None

def runMapEditor(main, mapName):
    """Run the map editor.

    Arguments:

        main - A MainWindow classobj, this is the main window context.
        mapName - A string containing the name of the map to edit.
    """
    import gui.MapEditorGUI
    import Resources

    Resources.map = Resources.MapLoader()
    if mapName != None:
#        try:
            m = Resources.map(mapName)
#        except Exception, e:
#            print 'Error loading map "%s":' % mapName
#            print e
#            sys.exit(1)
    else:
        m = Resources.map('random')

    # Start the map editor GUI
    mapEditorGUI = gui.MapEditorGUI.MapEditorGUI(m)
    main.setDelegate(mapEditorGUI)


def startGame(server, port=None, user=None, scenario=None,
              multiplayer=None):
    if port == None:
        port = options.port
    if user == None:
        user = options.user
    if multiplayer == None:
        multiplayer = options.multiplayer
        
    # Configure the server
    if server == None:
        server = '127.0.0.1'
        gameServer = GameServer(port)
    # Then configure the client
    aiPlayers = 1
    if multiplayer:
        aiPlayers = 0
    gameClient = InteractiveClient(server,
                                   port,
                                   user,
                                   scenario,
                                   aiPlayers,
                                   window)

def run(opts):
    global window, options
    options = opts
    window = gui.MainWindow.MainWindow(options.fullscreen,
                                       options.width)
    window.update()
    if options.edit_map:
        runMapEditor(window, options.edit_map)
    else:
        window.setDelegate(gui.ScenarioChooser.ScenarioChooser())
    try:        
        reactor.run()               
    except KeyboardInterrupt:
        if reactor.running:
            reactor.stop()
