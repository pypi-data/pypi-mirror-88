from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Umotion:
	"""Umotion commands group definition. 24 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("umotion", core, parent)

	def clone(self) -> 'Umotion':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Umotion(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Umotion_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_step'):
			from .Umotion_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def csv(self):
		"""csv commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_csv'):
			from .Umotion_.Csv import Csv
			self._csv = Csv(self._core, self._base)
		return self._csv

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.LogFmtSat:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:UMOTion:FORMat \n
		Sets the file format in that the logged data is stored. \n
			:return: format_py: CSV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:UMOTion:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.LogFmtSat)
