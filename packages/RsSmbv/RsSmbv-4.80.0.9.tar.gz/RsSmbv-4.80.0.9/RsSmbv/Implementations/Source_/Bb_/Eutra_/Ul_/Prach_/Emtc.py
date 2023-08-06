from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Emtc:
	"""Emtc commands group definition. 7 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("emtc", core, parent)

	def clone(self) -> 'Emtc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Emtc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def celv(self):
		"""celv commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_celv'):
			from .Emtc_.Celv import Celv
			self._celv = Celv(self._core, self._base)
		return self._celv

	def get_hoff(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:HOFF \n
		Sets a PRACH hopping offset as number of resource blocks (RB) . \n
			:return: hopping_offset: integer Range: 1 to 110
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:HOFF?')
		return Conversions.str_to_int(response)

	def set_hoff(self, hopping_offset: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:HOFF \n
		Sets a PRACH hopping offset as number of resource blocks (RB) . \n
			:param hopping_offset: integer Range: 1 to 110
		"""
		param = Conversions.decimal_value_to_str(hopping_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:HOFF {param}')

	# noinspection PyTypeChecker
	def get_rset(self) -> enums.EutraPrachPreambleSet:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:RSET \n
		Enables using the restricted set. \n
			:return: restricted_set: URES| ARES| BRES| OFF| ON URES|OFF Unrestricted preamble set. ARES|ON Restricted set type A. BRES Restricted set type B.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:RSET?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPrachPreambleSet)

	def set_rset(self, restricted_set: enums.EutraPrachPreambleSet) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:RSET \n
		Enables using the restricted set. \n
			:param restricted_set: URES| ARES| BRES| OFF| ON URES|OFF Unrestricted preamble set. ARES|ON Restricted set type A. BRES Restricted set type B.
		"""
		param = Conversions.enum_scalar_to_str(restricted_set, enums.EutraPrachPreambleSet)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:RSET {param}')
