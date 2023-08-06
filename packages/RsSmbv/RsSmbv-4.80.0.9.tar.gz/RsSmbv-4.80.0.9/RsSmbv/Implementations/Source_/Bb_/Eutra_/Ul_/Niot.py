from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

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
	def valid(self):
		"""valid commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_valid'):
			from .Niot_.Valid import Valid
			self._valid = Valid(self._core, self._base)
		return self._valid

	# noinspection PyTypeChecker
	def get_sub_config(self) -> enums.EutraNbiotInbandBitmapSfAll:
		"""[SOURce<HW>]:BB:EUTRa:UL:NIOT:SUBConfig \n
		Sets the number of subframes in the bitmap. \n
			:return: sf_config: N10| N40
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:NIOT:SUBConfig?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotInbandBitmapSfAll)

	def set_sub_config(self, sf_config: enums.EutraNbiotInbandBitmapSfAll) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:NIOT:SUBConfig \n
		Sets the number of subframes in the bitmap. \n
			:param sf_config: N10| N40
		"""
		param = Conversions.enum_scalar_to_str(sf_config, enums.EutraNbiotInbandBitmapSfAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:NIOT:SUBConfig {param}')
