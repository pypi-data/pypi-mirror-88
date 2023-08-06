from Pluginable.Event import *
from Pluginable.Logger import *
from Pluginable.Exceptions import *
from Pluginable.Settings import Settings
import Pluginable.MultiHandler as mh
from time import sleep

class ProgramState:
  allowRunning = False
  def __init__(self, program):
    Note(program, f'Program state changed to {self.__class__.__name__}')
  def setCustomSettings(self, program, data):
    Warn(program, 'Can not change settings now')
  def setProgramSettings(self, program, data):
    Warn(program, 'Can not change settings now')
  def setPluginSettings(self, program, pluginKey, data):
    Warn(program, 'Can not configure plugins now')
  def initialize(self, program):
    Warn(program, 'Can not initialize now')
  def run(self, program):
    Warn(program, 'Can not run the program now')
  def stopProgram(self, program):
    Error(program, f'stopProgram was not defined for state {self.__class__.__name__}')
    exit()
  def onCriticalError(self, program, pluginKey):
    Error(program, f'onCriticalError was not defined for state {self.__class__.__name__}')
    exit()
  def disallowRunning(self):
    self.allowRunning = False


class StatePreInit(ProgramState):
  def setCustomSettings(self, program, data):
    Note(program, 'Setting custom settings')
  def setProgramSettings(self, program, data):
    Note(program, 'Changing program settings')
  def stopProgram(self, program):
    program.cleanup()
  def onCriticalError(self, program, pluginKey):
    program.cleanup()

  def initialize(self, program):
    Note(program, 'Initializing')
    self.applySettingsChanges(program)
    program.tpsMon.setTarget(Settings.Kernel.MaxProgramTicksPerSec)
    try: program.compiler.compile()
    except (CompilerError, PluginStartupError) as exc:
      program.onCriticalError(KernelExcEvent(True, exc))
      exit()
    program._state = StatePostInit(program)

  def applySettingsChanges(self, program):
    Warn(program, 'Applying settings changes')
    for key, val in program.settings.items():
      if type(val) == str: val = f'"{val}"'
      elif type(val) == datetime:
        val = f"datetime.strptime('{val}', '%Y-%m-%d %H:%M:%S.%f')"
      exec(f'Settings.{key} = {val}')


class StatePostInit(ProgramState):
  def setPluginSettings(self, program, pluginKey, data):
    Note(program, f'Configuring plugin {pluginKey}')
  def run(self, program):
    Note(program, 'Starting the program')
    program._state = StateRunning(program)
    program.run()
  def stopProgram(self, program):
    program.cleanup()
  def onCriticalError(self, program, pluginKey):
    program.cleanup()


class StateRunning(ProgramState):
  allowRunning = True
  def run(self, program):
    try: program.compiler.load()
    except Exception as exc: program.onErrorEvent(KernelExcEvent(True, exc))
    Note(program, 'Starting program')
    while program._state.allowRunning:
      try:
        program.handleAllAwaitingEvents()
        program.tpsMon.tick()
      except KeyboardInterrupt: break
    self.stopProgram(program)

  def callPluginsQuitMethod(self, program, omit=None):
    for key, plugin in program.plugins.items():
      if key == omit: continue
      mh.set(plugin.quitStatus, 1)
      mh.push(plugin.queue, KernelEvent('Quit'))

  def joinPluginProcesses(self, program):
    for key, plugin in program.plugins.items():
      if not plugin.loaded: continue
      plugin.proc.join()

  def stopProgram(self, program):
    self.callPluginsQuitMethod(program)
    sleep(Settings.Kernel.MaxPluginCleanupDuration)
    self.joinPluginProcesses(program)
    program.cleanup()

  def onCriticalError(self, program, omitPlugin):
    self.disallowRunning()
    self.callPluginsQuitMethod(program, omit=omitPlugin)
    sleep(Settings.Kernel.MaxPluginCleanupDuration)
    self.joinPluginProcesses(program)
    program.cleanup()
