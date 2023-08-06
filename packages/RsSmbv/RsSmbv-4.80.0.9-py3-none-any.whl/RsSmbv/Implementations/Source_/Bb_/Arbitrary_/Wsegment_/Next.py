from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Next:
	"""Next commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("next", core, parent)

	def clone(self) -> 'Next':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Next(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Next_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	# noinspection PyTypeChecker
	def get_source(self) -> enums.ArbSegmNextSource:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:NEXT:SOURce \n
		Selects the next segment source. \n
			:return: source: INTernal| NSEGM1 | INTernal| NSEGM1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:NEXT:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.ArbSegmNextSource)

	def set_source(self, source: enums.ArbSegmNextSource) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:NEXT:SOURce \n
		Selects the next segment source. \n
			:param source: INTernal| NSEGM1 | INTernal| NSEGM1
		"""
		param = Conversions.enum_scalar_to_str(source, enums.ArbSegmNextSource)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:NEXT:SOURce {param}')

	def get_value(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:NEXT \n
		Selects the segment to be output. \n
			:return: next_py: integer Range: 0 to 1023
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:NEXT?')
		return Conversions.str_to_int(response)

	def set_value(self, next_py: int) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:NEXT \n
		Selects the segment to be output. \n
			:param next_py: integer Range: 0 to 1023
		"""
		param = Conversions.decimal_value_to_str(next_py)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:NEXT {param}')
