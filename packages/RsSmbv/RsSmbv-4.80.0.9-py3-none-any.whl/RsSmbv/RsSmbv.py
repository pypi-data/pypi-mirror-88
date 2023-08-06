from .Internal.Core import Core
from .Internal.InstrumentErrors import RsInstrException
from .Internal.CommandsGroup import CommandsGroup
from . import repcap
from .Internal.RepeatedCapability import RepeatedCapability


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsSmbv:
	"""8891 total commands, 26 Sub-groups, 0 group commands"""
	driver_options = "SupportedInstrModels = SMW/SMBV, SupportedIdnPatterns = SMW/SMBV, SimulationIdnString = 'Rohde&Schwarz,SMBV100B,100001,4.80.0.0009'"

	def __init__(self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
		"""Initializes new RsSmbv session. \n
		Parameter options tokens examples:
			- 'Simulate=True' - starts the session in simulation mode. Default: False
			- 'SelectVisa=socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			- 'SelectVisa=rs' - forces usage of RohdeSchwarz Visa
			- 'SelectVisa=ni' - forces usage of National Instruments Visa
			- 'QueryInstrumentStatus = False' - same as driver.utilities.instrument_status_checking = False
			- 'DriverSetup=(WriteDelay = 20, ReadDelay = 5)' - Introduces delay of 20ms before each write and 5ms before each read
			- 'DriverSetup=(OpcWaitMode = OpcQuery)' - mode for all the opc-synchronised write/reads. Other modes: StbPolling, StbPollingSlow, StbPollingSuperSlow
			- 'DriverSetup=(AddTermCharToWriteBinBLock = True)' - Adds one additional LF to the end of the binary data (some instruments require that)
			- 'DriverSetup=(AssureWriteWithTermChar = True)' - Makes sure each command/query is terminated with termination character. Default: Interface dependent
			- 'DriverSetup=(TerminationCharacter = '\n')' - Sets the termination character for reading. Default: '\n' (LineFeed)
			- 'DriverSetup=(IoSegmentSize = 10E3)' - Maximum size of one write/read segment. If transferred data is bigger, it is split to more segments
			- 'DriverSetup=(OpcTimeout = 10000)' - same as driver.utilities.opc_timeout = 10000
			- 'DriverSetup=(VisaTimeout = 5000)' - same as driver.utilities.visa_timeout = 5000
			- 'DriverSetup=(ViClearExeMode = 255)' - Binary combination where 1 means performing viClear() on a certain interface as the very first command in init
			- 'DriverSetup=(OpcQueryAfterWrite = True)' - same as driver.utilities.opc_query_after_write = True
		:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
		:param id_query: if True: the instrument's model name is verified against the models supported by the driver and eventually throws an exception.
		:param reset: Resets the instrument (sends *RST command) and clears its status sybsystem
		:param options: string tokens alternating the driver settings.
		:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session."""
		self._core = Core(resource_name, id_query, reset, RsSmbv.driver_options, options, direct_session)
		self._core.driver_version = '4.80.0.0009'
		self._options = options
		self._add_all_global_repcaps()
		self._custom_properties_init()
		# noinspection PyTypeChecker
		self._base = CommandsGroup("ROOT", self._core, None)

	@classmethod
	def from_existing_session(cls, session: object, options: str = None) -> 'RsSmbv':
		"""Creates a new RsCmwBluetoothSig object with the entered 'session' reused. \n
		:param session: can be an another driver or a direct pyvisa session.
		:param options: string tokens alternating the driver settings."""
		# noinspection PyTypeChecker
		return cls(None, False, False, options, session)

	def __str__(self) -> str:
		if self._core.io:
			return f"RsSmbv session '{self._core.io.resource_name}'"
		else:
			return f"RsSmbv with session closed"

	@staticmethod
	def assert_minimum_version(min_version: str) -> None:
		"""Asserts that the driver version fulfills the minimum required version you have entered.
		This way you make sure your installed driver is of the entered version or newer."""
		min_version_list = min_version.split('.')
		curr_version_list = '4.80.0.0009'.split('.')
		count_min = len(min_version_list)
		count_curr = len(curr_version_list)
		count = count_min if count_min < count_curr else count_curr
		for i in range(count):
			minimum = int(min_version_list[i])
			curr = int(curr_version_list[i])
			if curr > minimum:
				break
			if curr < minimum:
				raise RsInstrException(f"Assertion for minimum RsSmbv version failed. Current version: '4.80.0.0009', minimum required version: '{min_version}'")

	def close(self) -> None:
		"""Closes the active RsSmbv session."""
		self._core.io.close()

	def get_session_handle(self) -> object:
		"""Returns the underlying pyvisa session."""
		return self._core.get_session_handle()

	def _add_all_global_repcaps(self) -> None:
		"""Adds all the repcaps defined as global to the instrument's global repcaps dictionary."""
		self._core.io.add_global_repcap('<HwInstance>', RepeatedCapability("ROOT", 'repcap_hwInstance_get', 'repcap_hwInstance_set', repcap.HwInstance.Inst0))

	def repcap_hwInstance_get(self) -> repcap.HwInstance:
		"""Returns Global Repeated capability HwInstance"""
		return self._core.io.get_global_repcap_value('<HwInstance>')

	def repcap_hwInstance_set(self, value: repcap.HwInstance) -> None:
		"""Sets Global Repeated capability HwInstance
		Default value after init: HwInstance.Inst0"""
		self._core.io.set_global_repcap_value('<HwInstance>', value)

	def clone(self) -> 'RsSmbv':
		"""Creates a deep copy of the RsSmbv object. Also copies:
			- All the existing Global repeated capability values
			- All the default group repeated capabilities setting \n
		After cloning, you can set all the repeated capabilities settings independentely from the original group.
		Calling close() on the new object does not close the original VISA session"""
		cloned = RsSmbv.from_existing_session(self.get_session_handle(), self._options)
		self._base.synchronize_repcaps(cloned)
		cloned.repcap_hwInstance_set(self.repcap_hwInstance_get())
		return cloned

	def restore_all_repcaps_to_default(self) -> None:
		"""Sets all the Group and Global repcaps to their initial values"""
		self._base.restore_repcaps()
		self.repcap_hwInstance_set(repcap.HwInstance.Inst0)

	def _custom_properties_init(self):
		"""Adds all the interfaces that are custom for the driver."""
		from .CustomFiles.utilities import Utilities
		self.utilities = Utilities(self._core)
		from .CustomFiles.events import Events
		self.events = Events(self._core)
		from .CustomFiles.arb_files import ArbFiles
		self.arb_files = ArbFiles(self._core)

	@property
	def bert(self):
		"""bert commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_bert'):
			from .Implementations.Bert import Bert
			self._bert = Bert(self._core, self._base)
		return self._bert

	@property
	def bler(self):
		"""bler commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_bler'):
			from .Implementations.Bler import Bler
			self._bler = Bler(self._core, self._base)
		return self._bler

	@property
	def calibration(self):
		"""calibration commands group. 11 Sub-classes, 2 commands."""
		if not hasattr(self, '_calibration'):
			from .Implementations.Calibration import Calibration
			self._calibration = Calibration(self._core, self._base)
		return self._calibration

	@property
	def clock(self):
		"""clock commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_clock'):
			from .Implementations.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def device(self):
		"""device commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Implementations.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	@property
	def diagnostic(self):
		"""diagnostic commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_diagnostic'):
			from .Implementations.Diagnostic import Diagnostic
			self._diagnostic = Diagnostic(self._core, self._base)
		return self._diagnostic

	@property
	def display(self):
		"""display commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_display'):
			from .Implementations.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_formatPy'):
			from .Implementations.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy

	@property
	def hardCopy(self):
		"""hardCopy commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_hardCopy'):
			from .Implementations.HardCopy import HardCopy
			self._hardCopy = HardCopy(self._core, self._base)
		return self._hardCopy

	@property
	def initiate(self):
		"""initiate commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_initiate'):
			from .Implementations.Initiate import Initiate
			self._initiate = Initiate(self._core, self._base)
		return self._initiate

	@property
	def kboard(self):
		"""kboard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kboard'):
			from .Implementations.Kboard import Kboard
			self._kboard = Kboard(self._core, self._base)
		return self._kboard

	@property
	def memory(self):
		"""memory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_memory'):
			from .Implementations.Memory import Memory
			self._memory = Memory(self._core, self._base)
		return self._memory

	@property
	def massMemory(self):
		"""massMemory commands group. 4 Sub-classes, 8 commands."""
		if not hasattr(self, '_massMemory'):
			from .Implementations.MassMemory import MassMemory
			self._massMemory = MassMemory(self._core, self._base)
		return self._massMemory

	@property
	def output(self):
		"""output commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_output'):
			from .Implementations.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def read(self):
		"""read commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_read'):
			from .Implementations.Read import Read
			self._read = Read(self._core, self._base)
		return self._read

	@property
	def sconfiguration(self):
		"""sconfiguration commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_sconfiguration'):
			from .Implementations.Sconfiguration import Sconfiguration
			self._sconfiguration = Sconfiguration(self._core, self._base)
		return self._sconfiguration

	@property
	def sense(self):
		"""sense commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sense'):
			from .Implementations.Sense import Sense
			self._sense = Sense(self._core, self._base)
		return self._sense

	@property
	def slist(self):
		"""slist commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_slist'):
			from .Implementations.Slist import Slist
			self._slist = Slist(self._core, self._base)
		return self._slist

	@property
	def source(self):
		"""source commands group. 32 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Implementations.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def status(self):
		"""status commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_status'):
			from .Implementations.Status import Status
			self._status = Status(self._core, self._base)
		return self._status

	@property
	def sweep(self):
		"""sweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sweep'):
			from .Implementations.Sweep import Sweep
			self._sweep = Sweep(self._core, self._base)
		return self._sweep

	@property
	def system(self):
		"""system commands group. 37 Sub-classes, 30 commands."""
		if not hasattr(self, '_system'):
			from .Implementations.System import System
			self._system = System(self._core, self._base)
		return self._system

	@property
	def test(self):
		"""test commands group. 10 Sub-classes, 6 commands."""
		if not hasattr(self, '_test'):
			from .Implementations.Test import Test
			self._test = Test(self._core, self._base)
		return self._test

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .Implementations.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def unit(self):
		"""unit commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_unit'):
			from .Implementations.Unit import Unit
			self._unit = Unit(self._core, self._base)
		return self._unit

	@property
	def xfer(self):
		"""xfer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xfer'):
			from .Implementations.Xfer import Xfer
			self._xfer = Xfer(self._core, self._base)
		return self._xfer
