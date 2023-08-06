from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrmFormat:
	"""FrmFormat commands group definition. 9 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frmFormat", core, parent)

	def clone(self) -> 'FrmFormat':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrmFormat(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ssc(self):
		"""ssc commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_ssc'):
			from .FrmFormat_.Ssc import Ssc
			self._ssc = Ssc(self._core, self._base)
		return self._ssc

	def get_ndl_slots(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NDLSlots \n
		Sets the number of DL slots in the frame. \n
			:return: qck_set_dl_slots: integer Range: 0 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NDLSlots?')
		return Conversions.str_to_int(response)

	def set_ndl_slots(self, qck_set_dl_slots: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NDLSlots \n
		Sets the number of DL slots in the frame. \n
			:param qck_set_dl_slots: integer Range: 0 to 10
		"""
		param = Conversions.decimal_value_to_str(qck_set_dl_slots)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NDLSlots {param}')

	def get_ns_slots(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NSSLots \n
		Queries the number of special slots in the frame. \n
			:return: qck_set_no_spl_slot: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NSSLots?')
		return Conversions.str_to_int(response)

	def get_nul_slots(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NULSlots \n
		Queries the number of UL slots in the frame. \n
			:return: qck_set_ul_slots: integer Range: 0 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NULSlots?')
		return Conversions.str_to_int(response)

	def set_nul_slots(self, qck_set_ul_slots: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:NULSlots \n
		Queries the number of UL slots in the frame. \n
			:param qck_set_ul_slots: integer Range: 0 to 10
		"""
		param = Conversions.decimal_value_to_str(qck_set_ul_slots)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:NULSlots {param}')

	# noinspection PyTypeChecker
	def get_slength(self) -> enums.QuickSetSlotLenAll:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SLENgth \n
		Sets the duration of the frame in slots. \n
			:return: qck_set_slot_len: S5| S10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SLENgth?')
		return Conversions.str_to_scalar_enum(response, enums.QuickSetSlotLenAll)

	def set_slength(self, qck_set_slot_len: enums.QuickSetSlotLenAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:FRMFormat:SLENgth \n
		Sets the duration of the frame in slots. \n
			:param qck_set_slot_len: S5| S10
		"""
		param = Conversions.enum_scalar_to_str(qck_set_slot_len, enums.QuickSetSlotLenAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:FRMFormat:SLENgth {param}')
