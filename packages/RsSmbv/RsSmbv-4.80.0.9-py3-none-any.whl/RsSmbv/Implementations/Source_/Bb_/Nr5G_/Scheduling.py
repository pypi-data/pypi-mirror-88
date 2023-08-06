from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scheduling:
	"""Scheduling commands group definition. 363 total commands, 2 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scheduling", core, parent)

	def clone(self) -> 'Scheduling':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scheduling(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cell(self):
		"""cell commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Scheduling_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def sfn(self):
		"""sfn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfn'):
			from .Scheduling_.Sfn import Sfn
			self._sfn = Sfn(self._core, self._base)
		return self._sfn

	def get_ncarrier(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:SCHed:NCARrier \n
		No command help available \n
			:return: num_sched_carrier: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SCHed:NCARrier?')
		return Conversions.str_to_int(response)

	def set_ncarrier(self, num_sched_carrier: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:NCARrier \n
		No command help available \n
			:param num_sched_carrier: No help available
		"""
		param = Conversions.decimal_value_to_str(num_sched_carrier)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:NCARrier {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AutoManualMode:
		"""[SOURce<HW>]:BB:NR5G:SCHeduling:MODE \n
		Defines how the scheduling and the content of the different PDSCH allocations is defined and performed. \n
			:return: scheduling_mode: MANual| AUTO MANual No cross-reference between the settings made for the CORESET DCIs and the PDSCHs settings. Configure the PDSCH allocations manually. AUTO Content and scheduling of the PDSCH according to the configuration of the CORESET DCIs.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SCHeduling:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_mode(self, scheduling_mode: enums.AutoManualMode) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHeduling:MODE \n
		Defines how the scheduling and the content of the different PDSCH allocations is defined and performed. \n
			:param scheduling_mode: MANual| AUTO MANual No cross-reference between the settings made for the CORESET DCIs and the PDSCHs settings. Configure the PDSCH allocations manually. AUTO Content and scheduling of the PDSCH according to the configuration of the CORESET DCIs.
		"""
		param = Conversions.enum_scalar_to_str(scheduling_mode, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHeduling:MODE {param}')

	def get_rs_space(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:SCHeduling:RSSPace \n
		If enabled, the CCE start index is selected automatically to be within the current search space. \n
			:return: restr_to_sspace: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SCHeduling:RSSPace?')
		return Conversions.str_to_bool(response)

	def set_rs_space(self, restr_to_sspace: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHeduling:RSSPace \n
		If enabled, the CCE start index is selected automatically to be within the current search space. \n
			:param restr_to_sspace: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(restr_to_sspace)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHeduling:RSSPace {param}')
