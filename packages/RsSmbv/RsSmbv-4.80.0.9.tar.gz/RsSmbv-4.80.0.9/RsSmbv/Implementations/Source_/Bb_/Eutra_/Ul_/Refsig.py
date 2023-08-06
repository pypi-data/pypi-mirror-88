from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Refsig:
	"""Refsig commands group definition. 18 total commands, 2 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("refsig", core, parent)

	def clone(self) -> 'Refsig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Refsig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def drs(self):
		"""drs commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_drs'):
			from .Refsig_.Drs import Drs
			self._drs = Drs(self._core, self._base)
		return self._drs

	@property
	def srs(self):
		"""srs commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_srs'):
			from .Refsig_.Srs import Srs
			self._srs = Srs(self._core, self._base)
		return self._srs

	def get_dmrs(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:DMRS \n
		Sets the part of the demodulation reference signal (DMRS) index which is broadcasted and therefore valid for the whole
		cell. This index applies when multiple shifts within a cell are used and is used by the calculation of the DMRS sequence. \n
			:return: drs_dmrs: integer Range: 0 to 11
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:DMRS?')
		return Conversions.str_to_int(response)

	def set_dmrs(self, drs_dmrs: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:DMRS \n
		Sets the part of the demodulation reference signal (DMRS) index which is broadcasted and therefore valid for the whole
		cell. This index applies when multiple shifts within a cell are used and is used by the calculation of the DMRS sequence. \n
			:param drs_dmrs: integer Range: 0 to 11
		"""
		param = Conversions.decimal_value_to_str(drs_dmrs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:DMRS {param}')

	def get_ds_shift(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:DSSHift \n
		Sets the delta sequence shift for PUSCH needed for the calculation of the group hopping pattern. \n
			:return: delta_seq_shift: integer Range: 0 to 29
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:DSSHift?')
		return Conversions.str_to_int(response)

	def set_ds_shift(self, delta_seq_shift: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:DSSHift \n
		Sets the delta sequence shift for PUSCH needed for the calculation of the group hopping pattern. \n
			:param delta_seq_shift: integer Range: 0 to 29
		"""
		param = Conversions.decimal_value_to_str(delta_seq_shift)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:DSSHift {param}')

	def get_grp_hopping(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:GRPHopping \n
		Enables/disables group hopping for the uplink reference signals demodulation reference signal (DRS) and sounding
		reference signal (SRS) . \n
			:return: group_hopping: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:GRPHopping?')
		return Conversions.str_to_bool(response)

	def set_grp_hopping(self, group_hopping: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:GRPHopping \n
		Enables/disables group hopping for the uplink reference signals demodulation reference signal (DRS) and sounding
		reference signal (SRS) . \n
			:param group_hopping: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(group_hopping)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:GRPHopping {param}')

	def get_seq_hopping(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:SEQHopping \n
		Enables/disables sequence hopping for the uplink reference signals demodulation reference signal (DRS) and sounding
		reference signal (SRS) . \n
			:return: sequence_hopping: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SEQHopping?')
		return Conversions.str_to_bool(response)

	def set_seq_hopping(self, sequence_hopping: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:REFSig:SEQHopping \n
		Enables/disables sequence hopping for the uplink reference signals demodulation reference signal (DRS) and sounding
		reference signal (SRS) . \n
			:param sequence_hopping: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(sequence_hopping)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:REFSig:SEQHopping {param}')
