from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nr5G:
	"""Nr5G commands group definition. 984 total commands, 24 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nr5G", core, parent)

	def clone(self) -> 'Nr5G':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nr5G(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def analyzer(self):
		"""analyzer commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_analyzer'):
			from .Nr5G_.Analyzer import Analyzer
			self._analyzer = Analyzer(self._core, self._base)
		return self._analyzer

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Nr5G_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def feat(self):
		"""feat commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_feat'):
			from .Nr5G_.Feat import Feat
			self._feat = Feat(self._core, self._base)
		return self._feat

	@property
	def feature(self):
		"""feature commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_feature'):
			from .Nr5G_.Feature import Feature
			self._feature = Feature(self._core, self._base)
		return self._feature

	@property
	def fmode(self):
		"""fmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmode'):
			from .Nr5G_.Fmode import Fmode
			self._fmode = Fmode(self._core, self._base)
		return self._fmode

	@property
	def hfb(self):
		"""hfb commands group. 0 Sub-classes, 11 commands."""
		if not hasattr(self, '_hfb'):
			from .Nr5G_.Hfb import Hfb
			self._hfb = Hfb(self._core, self._base)
		return self._hfb

	@property
	def k145(self):
		"""k145 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_k145'):
			from .Nr5G_.K145 import K145
			self._k145 = K145(self._core, self._base)
		return self._k145

	@property
	def k148(self):
		"""k148 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_k148'):
			from .Nr5G_.K148 import K148
			self._k148 = K148(self._core, self._base)
		return self._k148

	@property
	def k548(self):
		"""k548 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_k548'):
			from .Nr5G_.K548 import K548
			self._k548 = K548(self._core, self._base)
		return self._k548

	@property
	def k81(self):
		"""k81 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_k81'):
			from .Nr5G_.K81 import K81
			self._k81 = K81(self._core, self._base)
		return self._k81

	@property
	def logGen(self):
		"""logGen commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_logGen'):
			from .Nr5G_.LogGen import LogGen
			self._logGen = LogGen(self._core, self._base)
		return self._logGen

	@property
	def node(self):
		"""node commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_node'):
			from .Nr5G_.Node import Node
			self._node = Node(self._core, self._base)
		return self._node

	@property
	def nsmod(self):
		"""nsmod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsmod'):
			from .Nr5G_.Nsmod import Nsmod
			self._nsmod = Nsmod(self._core, self._base)
		return self._nsmod

	@property
	def output(self):
		"""output commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_output'):
			from .Nr5G_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def qckset(self):
		"""qckset commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_qckset'):
			from .Nr5G_.Qckset import Qckset
			self._qckset = Qckset(self._core, self._base)
		return self._qckset

	@property
	def sanity(self):
		"""sanity commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sanity'):
			from .Nr5G_.Sanity import Sanity
			self._sanity = Sanity(self._core, self._base)
		return self._sanity

	@property
	def scheduling(self):
		"""scheduling commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_scheduling'):
			from .Nr5G_.Scheduling import Scheduling
			self._scheduling = Scheduling(self._core, self._base)
		return self._scheduling

	@property
	def setting(self):
		"""setting commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Nr5G_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Nr5G_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def tcw(self):
		"""tcw commands group. 8 Sub-classes, 13 commands."""
		if not hasattr(self, '_tcw'):
			from .Nr5G_.Tcw import Tcw
			self._tcw = Tcw(self._core, self._base)
		return self._tcw

	@property
	def tdWind(self):
		"""tdWind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdWind'):
			from .Nr5G_.TdWind import TdWind
			self._tdWind = TdWind(self._core, self._base)
		return self._tdWind

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Nr5G_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def ubwp(self):
		"""ubwp commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_ubwp'):
			from .Nr5G_.Ubwp import Ubwp
			self._ubwp = Ubwp(self._core, self._base)
		return self._ubwp

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Nr5G_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_link(self) -> enums.UpDownDirection:
		"""[SOURce<HW>]:BB:NR5G:LINK \n
		Selects the transmission direction. \n
			:return: link_dir: DOWN| UP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.UpDownDirection)

	def set_link(self, link_dir: enums.UpDownDirection) -> None:
		"""[SOURce<HW>]:BB:NR5G:LINK \n
		Selects the transmission direction. \n
			:param link_dir: DOWN| UP
		"""
		param = Conversions.enum_scalar_to_str(link_dir, enums.UpDownDirection)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:LINK {param}')

	# noinspection PyTypeChecker
	def get_map_coord(self) -> enums.CoordMapMode:
		"""[SOURce<HW>]:BB:NR5G:MAPCoord \n
		No command help available \n
			:return: coord_map_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:MAPCoord?')
		return Conversions.str_to_scalar_enum(response, enums.CoordMapMode)

	def set_map_coord(self, coord_map_mode: enums.CoordMapMode) -> None:
		"""[SOURce<HW>]:BB:NR5G:MAPCoord \n
		No command help available \n
			:param coord_map_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(coord_map_mode, enums.CoordMapMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:MAPCoord {param}')

	def get_pl_version(self) -> str:
		"""[SOURce]:BB:NR5G:PLVersion \n
		No command help available \n
			:return: plugin_version: No help available
		"""
		response = self._core.io.query_str('SOURce:BB:NR5G:PLVersion?')
		return trim_str_response(response)

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:NR5G:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Nr5G.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:NR5G:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Nr5G.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NR5G:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:STATe {param}')

	def get_version(self) -> str:
		"""[SOURce]:BB:NR5G:VERSion \n
		Queries the version of the 3GPP standard underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce:BB:NR5G:VERSion?')
		return trim_str_response(response)
