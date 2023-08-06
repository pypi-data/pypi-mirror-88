from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Calibration:
	"""Calibration commands group definition. 34 total commands, 11 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("calibration", core, parent)

	def clone(self) -> 'Calibration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Calibration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def all(self):
		"""all commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_all'):
			from .Calibration_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def bbin(self):
		"""bbin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbin'):
			from .Calibration_.Bbin import Bbin
			self._bbin = Bbin(self._core, self._base)
		return self._bbin

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Calibration_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def fmOffset(self):
		"""fmOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmOffset'):
			from .Calibration_.FmOffset import FmOffset
			self._fmOffset = FmOffset(self._core, self._base)
		return self._fmOffset

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Calibration_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def iqModulator(self):
		"""iqModulator commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_iqModulator'):
			from .Calibration_.IqModulator import IqModulator
			self._iqModulator = IqModulator(self._core, self._base)
		return self._iqModulator

	@property
	def level(self):
		"""level commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_level'):
			from .Calibration_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def lfOutput(self):
		"""lfOutput commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lfOutput'):
			from .Calibration_.LfOutput import LfOutput
			self._lfOutput = LfOutput(self._core, self._base)
		return self._lfOutput

	@property
	def roscillator(self):
		"""roscillator commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_roscillator'):
			from .Calibration_.Roscillator import Roscillator
			self._roscillator = Roscillator(self._core, self._base)
		return self._roscillator

	@property
	def tselected(self):
		"""tselected commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_tselected'):
			from .Calibration_.Tselected import Tselected
			self._tselected = Tselected(self._core, self._base)
		return self._tselected

	@property
	def vco(self):
		"""vco commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vco'):
			from .Calibration_.Vco import Vco
			self._vco = Vco(self._core, self._base)
		return self._vco

	def get_continue_on_error(self) -> bool:
		"""CALibration<HW>:CONTinueonerror \n
		Continues the calibration even though an error was detected. By default adjustments are aborted on error. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:CONTinueonerror?')
		return Conversions.str_to_bool(response)

	def set_continue_on_error(self, state: bool) -> None:
		"""CALibration<HW>:CONTinueonerror \n
		Continues the calibration even though an error was detected. By default adjustments are aborted on error. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CALibration<HwInstance>:CONTinueonerror {param}')

	def set_debug(self, state: bool) -> None:
		"""CALibration<HW>:DEBug \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CALibration<HwInstance>:DEBug {param}')
