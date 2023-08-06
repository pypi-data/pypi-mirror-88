from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stereo:
	"""Stereo commands group definition. 91 total commands, 7 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stereo", core, parent)

	def clone(self) -> 'Stereo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Stereo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def audio(self):
		"""audio commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_audio'):
			from .Stereo_.Audio import Audio
			self._audio = Audio(self._core, self._base)
		return self._audio

	@property
	def ds(self):
		"""ds commands group. 0 Sub-classes, 9 commands."""
		if not hasattr(self, '_ds'):
			from .Stereo_.Ds import Ds
			self._ds = Ds(self._core, self._base)
		return self._ds

	@property
	def ghex(self):
		"""ghex commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_ghex'):
			from .Stereo_.Ghex import Ghex
			self._ghex = Ghex(self._core, self._base)
		return self._ghex

	@property
	def grps(self):
		"""grps commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_grps'):
			from .Stereo_.Grps import Grps
			self._grps = Grps(self._core, self._base)
		return self._grps

	@property
	def pilot(self):
		"""pilot commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_pilot'):
			from .Stereo_.Pilot import Pilot
			self._pilot = Pilot(self._core, self._base)
		return self._pilot

	@property
	def setting(self):
		"""setting commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_setting'):
			from .Stereo_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_trigger'):
			from .Stereo_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_deviation(self) -> int:
		"""[SOURce<HW>]:BB:STEReo:DEViation \n
		No command help available \n
			:return: deviation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:DEViation?')
		return Conversions.str_to_int(response)

	def set_deviation(self, deviation: int) -> None:
		"""[SOURce<HW>]:BB:STEReo:DEViation \n
		No command help available \n
			:param deviation: No help available
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:DEViation {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:STEReo:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:STEReo:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:STEReo:PRESet')

	def get_puws_int(self) -> bool:
		"""[SOURce<HW>]:BB:STEReo:PUWSint \n
		No command help available \n
			:return: puws: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:PUWSint?')
		return Conversions.str_to_bool(response)

	def set_puws_int(self, puws: bool) -> None:
		"""[SOURce<HW>]:BB:STEReo:PUWSint \n
		No command help available \n
			:param puws: No help available
		"""
		param = Conversions.bool_to_str(puws)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:PUWSint {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.FmStereoAudSrc:
		"""[SOURce<HW>]:BB:STEReo:SOURce \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.FmStereoAudSrc)

	def set_source(self, source: enums.FmStereoAudSrc) -> None:
		"""[SOURce<HW>]:BB:STEReo:SOURce \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.FmStereoAudSrc)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:SOURce {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:STEReo:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:STEReo:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:STATe {param}')
