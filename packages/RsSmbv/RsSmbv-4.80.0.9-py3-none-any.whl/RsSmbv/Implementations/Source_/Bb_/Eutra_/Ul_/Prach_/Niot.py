from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 6 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("niot", core, parent)

	def clone(self) -> 'Niot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Niot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cfg(self):
		"""cfg commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cfg'):
			from .Niot_.Cfg import Cfg
			self._cfg = Cfg(self._core, self._base)
		return self._cfg

	# noinspection PyTypeChecker
	def get_pfmt(self) -> enums.EutraPracNbiotPreambleFormat:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:PFMT \n
		Select the preamble format. \n
			:return: preamble_format: F0| F1 | 0| 1 | F2| F0A| F1A 0|1 backward compatibility; use F0|F1 instead.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:PFMT?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPracNbiotPreambleFormat)

	def set_pfmt(self, preamble_format: enums.EutraPracNbiotPreambleFormat) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:PFMT \n
		Select the preamble format. \n
			:param preamble_format: F0| F1 | 0| 1 | F2| F0A| F1A 0|1 backward compatibility; use F0|F1 instead.
		"""
		param = Conversions.enum_scalar_to_str(preamble_format, enums.EutraPracNbiotPreambleFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:PFMT {param}')
