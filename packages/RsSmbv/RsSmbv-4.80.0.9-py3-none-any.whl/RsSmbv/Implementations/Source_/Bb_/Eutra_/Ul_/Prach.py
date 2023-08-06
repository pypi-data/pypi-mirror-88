from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prach:
	"""Prach commands group definition. 16 total commands, 2 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prach", core, parent)

	def clone(self) -> 'Prach':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Prach(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def emtc(self):
		"""emtc commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_emtc'):
			from .Prach_.Emtc import Emtc
			self._emtc = Emtc(self._core, self._base)
		return self._emtc

	@property
	def niot(self):
		"""niot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_niot'):
			from .Prach_.Niot import Niot
			self._niot = Niot(self._core, self._base)
		return self._niot

	def get_configuration(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:CONFiguration \n
		Sets the PRACH configuration number. \n
			:return: configuration: integer Range: 0 to 63
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PRACh:CONFiguration?')
		return Conversions.str_to_int(response)

	def set_configuration(self, configuration: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:CONFiguration \n
		Sets the PRACH configuration number. \n
			:param configuration: integer Range: 0 to 63
		"""
		param = Conversions.decimal_value_to_str(configuration)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:CONFiguration {param}')

	def get_foffset(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:FOFFset \n
		Sets the prach-FrequencyOffset nRAPRBoffset \n
			:return: frequency_offset: integer Range: 0 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PRACh:FOFFset?')
		return Conversions.str_to_int(response)

	def set_foffset(self, frequency_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:FOFFset \n
		Sets the prach-FrequencyOffset nRAPRBoffset \n
			:param frequency_offset: integer Range: 0 to dynamic
		"""
		param = Conversions.decimal_value_to_str(frequency_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:FOFFset {param}')

	# noinspection PyTypeChecker
	def get_rset(self) -> enums.EutraPrachPreambleSet:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:RSET \n
		Enables/disables using of a restricted preamble set. \n
			:return: restricted_set: URES| ARES| BRES| OFF| ON URES|OFF Unrestricted preamble set. ARES|ON Restricted set type A. BRES Restricted set type B.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PRACh:RSET?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPrachPreambleSet)

	def set_rset(self, restricted_set: enums.EutraPrachPreambleSet) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:RSET \n
		Enables/disables using of a restricted preamble set. \n
			:param restricted_set: URES| ARES| BRES| OFF| ON URES|OFF Unrestricted preamble set. ARES|ON Restricted set type A. BRES Restricted set type B.
		"""
		param = Conversions.enum_scalar_to_str(restricted_set, enums.EutraPrachPreambleSet)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:RSET {param}')
