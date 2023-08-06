from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Psdu:
	"""Psdu commands group definition. 30 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psdu", core, parent)

	def clone(self) -> 'Psdu':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Psdu(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bspreading(self):
		"""bspreading commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bspreading'):
			from .Psdu_.Bspreading import Bspreading
			self._bspreading = Bspreading(self._core, self._base)
		return self._bspreading

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_data'):
			from .Psdu_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def mac(self):
		"""mac commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_mac'):
			from .Psdu_.Mac import Mac
			self._mac = Mac(self._core, self._base)
		return self._mac

	def get_brate(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:PSDU:BRATe \n
		No command help available \n
			:return: brate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:BRATe?')
		return Conversions.str_to_float(response)

	def set_brate(self, brate: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:PSDU:BRATe \n
		No command help available \n
			:param brate: No help available
		"""
		param = Conversions.decimal_value_to_str(brate)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:BRATe {param}')

	def get_dlength(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:PSDU:DLENgth \n
		No command help available \n
			:return: dlength: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:DLENgth?')
		return Conversions.str_to_float(response)

	def set_dlength(self, dlength: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:PSDU:DLENgth \n
		No command help available \n
			:param dlength: No help available
		"""
		param = Conversions.decimal_value_to_str(dlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:DLENgth {param}')

	# noinspection PyTypeChecker
	def get_modulation(self) -> enums.ModulationE:
		"""[SOURce<HW>]:BB:WLAN:PSDU:MODulation \n
		No command help available \n
			:return: modulation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationE)

	def get_scount(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:PSDU:SCOunt \n
		No command help available \n
			:return: scount: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:SCOunt?')
		return Conversions.str_to_float(response)

	def set_scount(self, scount: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:PSDU:SCOunt \n
		No command help available \n
			:param scount: No help available
		"""
		param = Conversions.decimal_value_to_str(scount)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:SCOunt {param}')
