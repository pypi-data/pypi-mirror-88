from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ciq:
	"""Ciq commands group definition. 4 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ciq", core, parent)

	def clone(self) -> 'Ciq':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ciq(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def create(self):
		"""create commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_create'):
			from .Ciq_.Create import Create
			self._create = Create(self._core, self._base)
		return self._create

	def get_icomponent(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:CIQ:I \n
		Sets the value for the I and Q component of the test signal \n
			:return: ipart: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:CIQ:I?')
		return Conversions.str_to_float(response)

	def set_icomponent(self, ipart: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:CIQ:I \n
		Sets the value for the I and Q component of the test signal \n
			:param ipart: float Range: -1 to 1, Unit: FS
		"""
		param = Conversions.decimal_value_to_str(ipart)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:CIQ:I {param}')

	def get_qcomponent(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:CIQ:Q \n
		Sets the value for the I and Q component of the test signal \n
			:return: tsig: float Range: -1 to 1, Unit: FS
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:CIQ:Q?')
		return Conversions.str_to_float(response)

	def set_qcomponent(self, tsig: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:CIQ:Q \n
		Sets the value for the I and Q component of the test signal \n
			:param tsig: float Range: -1 to 1, Unit: FS
		"""
		param = Conversions.decimal_value_to_str(tsig)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:CIQ:Q {param}')
