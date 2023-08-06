from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gap:
	"""Gap commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gap", core, parent)

	def clone(self) -> 'Gap':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gap(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Gap_.Config import Config
			self._config = Config(self._core, self._base)
		return self._config

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Gap_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	# noinspection PyTypeChecker
	def get_periodicity(self) -> enums.EutraNbiotGapPeriodicity:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:GAP:PERiodicity \n
		Sets the number of subframes after that the configured gap is repeated. \n
			:return: gap_periodicity: 64| 128| 256| 512
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:GAP:PERiodicity?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotGapPeriodicity)

	def set_periodicity(self, gap_periodicity: enums.EutraNbiotGapPeriodicity) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:GAP:PERiodicity \n
		Sets the number of subframes after that the configured gap is repeated. \n
			:param gap_periodicity: 64| 128| 256| 512
		"""
		param = Conversions.enum_scalar_to_str(gap_periodicity, enums.EutraNbiotGapPeriodicity)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:GAP:PERiodicity {param}')

	# noinspection PyTypeChecker
	def get_threshold(self) -> enums.EutraNbiotGapThreshold:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:GAP:THReshold \n
		Sets the gap threshold. \n
			:return: gap_threshold: 32| 64| 128| 256
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:GAP:THReshold?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotGapThreshold)

	def set_threshold(self, gap_threshold: enums.EutraNbiotGapThreshold) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:GAP:THReshold \n
		Sets the gap threshold. \n
			:param gap_threshold: 32| 64| 128| 256
		"""
		param = Conversions.enum_scalar_to_str(gap_threshold, enums.EutraNbiotGapThreshold)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:GAP:THReshold {param}')
