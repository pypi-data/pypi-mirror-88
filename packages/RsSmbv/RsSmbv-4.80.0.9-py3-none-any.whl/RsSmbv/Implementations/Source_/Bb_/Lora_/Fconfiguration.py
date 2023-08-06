from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fconfiguration:
	"""Fconfiguration commands group definition. 16 total commands, 9 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fconfiguration", core, parent)

	def clone(self) -> 'Fconfiguration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fconfiguration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bmode(self):
		"""bmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmode'):
			from .Fconfiguration_.Bmode import Bmode
			self._bmode = Bmode(self._core, self._base)
		return self._bmode

	@property
	def cmode(self):
		"""cmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmode'):
			from .Fconfiguration_.Cmode import Cmode
			self._cmode = Cmode(self._core, self._base)
		return self._cmode

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_data'):
			from .Fconfiguration_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def eactive(self):
		"""eactive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eactive'):
			from .Fconfiguration_.Eactive import Eactive
			self._eactive = Eactive(self._core, self._base)
		return self._eactive

	@property
	def hactive(self):
		"""hactive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hactive'):
			from .Fconfiguration_.Hactive import Hactive
			self._hactive = Hactive(self._core, self._base)
		return self._hactive

	@property
	def iactive(self):
		"""iactive commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iactive'):
			from .Fconfiguration_.Iactive import Iactive
			self._iactive = Iactive(self._core, self._base)
		return self._iactive

	@property
	def pcrc(self):
		"""pcrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcrc'):
			from .Fconfiguration_.Pcrc import Pcrc
			self._pcrc = Pcrc(self._core, self._base)
		return self._pcrc

	@property
	def prcMode(self):
		"""prcMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prcMode'):
			from .Fconfiguration_.PrcMode import PrcMode
			self._prcMode = PrcMode(self._core, self._base)
		return self._prcMode

	@property
	def rbit(self):
		"""rbit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbit'):
			from .Fconfiguration_.Rbit import Rbit
			self._rbit = Rbit(self._core, self._base)
		return self._rbit

	# noinspection PyTypeChecker
	def get_crate(self) -> enums.LoRaCodRate:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:CRATe \n
		Sets the coding rate. \n
			:return: crate: CR0| CR1| CR2| CR3| CR4 CRx = 0 to 4 The coding rate RCoding is calculated as follows: RCoding = 4 / (4 + CRx) 'CR0' corresponds to no coding, i.e. RCoding = 1.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:CRATe?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaCodRate)

	def set_crate(self, crate: enums.LoRaCodRate) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:CRATe \n
		Sets the coding rate. \n
			:param crate: CR0| CR1| CR2| CR3| CR4 CRx = 0 to 4 The coding rate RCoding is calculated as follows: RCoding = 4 / (4 + CRx) 'CR0' corresponds to no coding, i.e. RCoding = 1.
		"""
		param = Conversions.enum_scalar_to_str(crate, enums.LoRaCodRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:CRATe {param}')

	def get_dlength(self) -> int:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DLENgth \n
		Sets the data length of the payload in the frame. \n
			:return: dlength: integer Range: 1 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:DLENgth?')
		return Conversions.str_to_int(response)

	def set_dlength(self, dlength: int) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:DLENgth \n
		Sets the data length of the payload in the frame. \n
			:param dlength: integer Range: 1 to 255
		"""
		param = Conversions.decimal_value_to_str(dlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:DLENgth {param}')

	# noinspection PyTypeChecker
	def get_sfactor(self) -> enums.LoRaSf:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:SFACtor \n
		Sets the spreading factor for the modulation. \n
			:return: sf: SF6| SF7| SF8| SF9| SF10| SF11| SF12
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:SFACtor?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaSf)

	def set_sfactor(self, sf: enums.LoRaSf) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:SFACtor \n
		Sets the spreading factor for the modulation. \n
			:param sf: SF6| SF7| SF8| SF9| SF10| SF11| SF12
		"""
		param = Conversions.enum_scalar_to_str(sf, enums.LoRaSf)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:SFACtor {param}')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.LoRaSyncMode:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:SMODe \n
		Sets the synchronization mode of the preamble. \n
			:return: sm_ode: PRIVate| PUBLic PRIVate A preamble with a public sync word is generated. PUBLic A preamble with a private sync word is generated.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaSyncMode)

	def set_smode(self, sm_ode: enums.LoRaSyncMode) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:SMODe \n
		Sets the synchronization mode of the preamble. \n
			:param sm_ode: PRIVate| PUBLic PRIVate A preamble with a public sync word is generated. PUBLic A preamble with a private sync word is generated.
		"""
		param = Conversions.enum_scalar_to_str(sm_ode, enums.LoRaSyncMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:SMODe {param}')

	def get_up_length(self) -> int:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:UPLength \n
		Sets the unmodulated preamble length. \n
			:return: plength: integer Range: 6 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:FCONfiguration:UPLength?')
		return Conversions.str_to_int(response)

	def set_up_length(self, plength: int) -> None:
		"""[SOURce<HW>]:BB:LORA:FCONfiguration:UPLength \n
		Sets the unmodulated preamble length. \n
			:param plength: integer Range: 6 to 8
		"""
		param = Conversions.decimal_value_to_str(plength)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:FCONfiguration:UPLength {param}')
