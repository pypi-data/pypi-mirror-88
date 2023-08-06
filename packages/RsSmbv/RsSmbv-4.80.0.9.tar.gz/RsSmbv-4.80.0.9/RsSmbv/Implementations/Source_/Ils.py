from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ils:
	"""Ils commands group definition. 27 total commands, 7 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ils", core, parent)

	def clone(self) -> 'Ils':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ils(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Ils_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def gs(self):
		"""gs commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_gs'):
			from .Ils_.Gs import Gs
			self._gs = Gs(self._core, self._base)
		return self._gs

	@property
	def gslope(self):
		"""gslope commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_gslope'):
			from .Ils_.Gslope import Gslope
			self._gslope = Gslope(self._core, self._base)
		return self._gslope

	@property
	def localizer(self):
		"""localizer commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_localizer'):
			from .Ils_.Localizer import Localizer
			self._localizer = Localizer(self._core, self._base)
		return self._localizer

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Ils_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Ils_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def mbeacon(self):
		"""mbeacon commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_mbeacon'):
			from .Ils_.Mbeacon import Mbeacon
			self._mbeacon = Mbeacon(self._core, self._base)
		return self._mbeacon

	def preset(self) -> None:
		"""[SOURce<HW>]:ILS:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:ILS:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:ILS:STATe \n
		Activates/deactivates the avionic standard. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:ILS:STATe \n
		Activates/deactivates the avionic standard. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:STATe {param}')
