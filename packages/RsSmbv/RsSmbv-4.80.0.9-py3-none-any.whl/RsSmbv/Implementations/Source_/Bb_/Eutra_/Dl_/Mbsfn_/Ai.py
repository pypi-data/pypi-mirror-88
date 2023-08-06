from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ai:
	"""Ai commands group definition. 18 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ai", core, parent)

	def clone(self) -> 'Ai':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ai(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mcch(self):
		"""mcch commands group. 3 Sub-classes, 12 commands."""
		if not hasattr(self, '_mcch'):
			from .Ai_.Mcch import Mcch
			self._mcch = Mcch(self._core, self._base)
		return self._mcch

	def get_id(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:ID \n
		Defines the MBSFN area ID, parameter NidMBSFN. \n
			:return: area_id: integer Range: 0 to 255
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:ID?')
		return Conversions.str_to_int(response)

	def set_id(self, area_id: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:ID \n
		Defines the MBSFN area ID, parameter NidMBSFN. \n
			:param area_id: integer Range: 0 to 255
		"""
		param = Conversions.decimal_value_to_str(area_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:ID {param}')

	def get_nind(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:NIND \n
		Defines which PDCCH bit is used to notify the UE about change of the MCCH applicable for this MBSFN area. \n
			:return: notif_indicator: integer Range: 0 to 7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:NIND?')
		return Conversions.str_to_int(response)

	def set_nind(self, notif_indicator: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:NIND \n
		Defines which PDCCH bit is used to notify the UE about change of the MCCH applicable for this MBSFN area. \n
			:param notif_indicator: integer Range: 0 to 7
		"""
		param = Conversions.decimal_value_to_str(notif_indicator)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:NIND {param}')

	def get_nmrl(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:NMRL \n
		Defines how many symbols from the beginning of the subframe constitute the non-MBSFN region. \n
			:return: region_length: integer Range: 1 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:NMRL?')
		return Conversions.str_to_int(response)

	def set_nmrl(self, region_length: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:NMRL \n
		Defines how many symbols from the beginning of the subframe constitute the non-MBSFN region. \n
			:param region_length: integer Range: 1 to 2
		"""
		param = Conversions.decimal_value_to_str(region_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:NMRL {param}')
