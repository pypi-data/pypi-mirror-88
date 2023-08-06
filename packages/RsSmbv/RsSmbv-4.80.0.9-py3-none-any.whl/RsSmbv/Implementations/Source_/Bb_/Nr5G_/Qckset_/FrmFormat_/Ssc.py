from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssc:
	"""Ssc commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssc", core, parent)

	def clone(self) -> 'Ssc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ssc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ussIdx(self):
		"""ussIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ussIdx'):
			from .Ssc_.UssIdx import UssIdx
			self._ussIdx = UssIdx(self._core, self._base)
		return self._ussIdx

	def get_ndl_symbols(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:NDLSymbols \n
		Queries the number of DL symbols. \n
			:return: qck_set_slot_dl_sym: integer Range: 0 to 14
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:NDLSymbols?')
		return Conversions.str_to_int(response)

	def get_ng_symbols(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:NGSYmbols \n
		Queries the number of guard symbols. \n
			:return: qck_set_sguard_sym: integer Range: 0 to 14
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:NGSYmbols?')
		return Conversions.str_to_int(response)

	def get_nul_symbols(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:NULSymbols \n
		Queries the number of UL symbols. \n
			:return: qck_set_sul_slots: integer Range: 0 to 14
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:NULSymbols?')
		return Conversions.str_to_int(response)

	def get_slfmt(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:SLFMt \n
		Sets the special slot format index. \n
			:return: qck_set_slot_fmt: integer Range: 0 to 45
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:SLFMt?')
		return Conversions.str_to_int(response)

	def set_slfmt(self, qck_set_slot_fmt: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SSC:SLFMt \n
		Sets the special slot format index. \n
			:param qck_set_slot_fmt: integer Range: 0 to 45
		"""
		param = Conversions.decimal_value_to_str(qck_set_slot_fmt)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SSC:SLFMt {param}')
