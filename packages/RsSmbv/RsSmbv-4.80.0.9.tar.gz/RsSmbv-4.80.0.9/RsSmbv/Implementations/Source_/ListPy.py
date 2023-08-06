from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 34 total commands, 8 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	def clone(self) -> 'ListPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ListPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dexchange(self):
		"""dexchange commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_dexchange'):
			from .ListPy_.Dexchange import Dexchange
			self._dexchange = Dexchange(self._core, self._base)
		return self._dexchange

	@property
	def dwell(self):
		"""dwell commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_dwell'):
			from .ListPy_.Dwell import Dwell
			self._dwell = Dwell(self._core, self._base)
		return self._dwell

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .ListPy_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_index'):
			from .ListPy_.Index import Index
			self._index = Index(self._core, self._base)
		return self._index

	@property
	def learn(self):
		"""learn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_learn'):
			from .ListPy_.Learn import Learn
			self._learn = Learn(self._core, self._base)
		return self._learn

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mode'):
			from .ListPy_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_power'):
			from .ListPy_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def trigger(self):
		"""trigger commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_trigger'):
			from .ListPy_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:LIST:CATalog \n
		Queries the available list files in the specified directory. \n
			:return: catalog: string List of list filenames, separated by commas
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:LIST:DELete \n
		Deletes the specified list. Refer to 'Accessing Files in the Default or in a Specified Directory' for general information
		on file handling in the default and in a specific directory. \n
			:param filename: string Filename or complete file path; file extension is optional.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:LIST:DELete {param}')

	def delete_all(self) -> None:
		"""[SOURce<HW>]:LIST:DELete:ALL \n
		Deletes all lists in the set directory.
			INTRO_CMD_HELP: This command can only be executed, if: \n
			- No list file is selected.
			- List mode is disabled. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:LIST:DELete:ALL')

	def delete_all_with_opc(self) -> None:
		"""[SOURce<HW>]:LIST:DELete:ALL \n
		Deletes all lists in the set directory.
			INTRO_CMD_HELP: This command can only be executed, if: \n
			- No list file is selected.
			- List mode is disabled. \n
		Same as delete_all, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:LIST:DELete:ALL')

	def get_free(self) -> int:
		"""[SOURce<HW>]:LIST:FREE \n
		Queries the amount of free memory (in bytes) for list mode lists. \n
			:return: free: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:FREE?')
		return Conversions.str_to_int(response)

	def reset(self) -> None:
		"""[SOURce<HW>]:LIST:RESet \n
		Jumps to the beginning of the list. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:LIST:RESet')

	def reset_with_opc(self) -> None:
		"""[SOURce<HW>]:LIST:RESet \n
		Jumps to the beginning of the list. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:LIST:RESet')

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.LmodRunMode:
		"""[SOURce<HW>]:LIST:RMODe \n
		No command help available \n
			:return: rm_ode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.LmodRunMode)

	def set_rmode(self, rm_ode: enums.LmodRunMode) -> None:
		"""[SOURce<HW>]:LIST:RMODe \n
		No command help available \n
			:param rm_ode: No help available
		"""
		param = Conversions.enum_scalar_to_str(rm_ode, enums.LmodRunMode)
		self._core.io.write(f'SOURce<HwInstance>:LIST:RMODe {param}')

	def get_running(self) -> bool:
		"""[SOURce<HW>]:LIST:RUNNing \n
		Queries the current state of the list mode. \n
			:return: state: 0| 1| OFF| ON 1 Signal generation based on the list mode is active.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:RUNNing?')
		return Conversions.str_to_bool(response)

	def get_select(self) -> str:
		"""[SOURce<HW>]:LIST:SELect \n
		Selects or creates a data list in list mode. If the list with the selected name does not exist, a new list is created. \n
			:return: filename: string Filename or complete file path; file extension can be omitted.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""[SOURce<HW>]:LIST:SELect \n
		Selects or creates a data list in list mode. If the list with the selected name does not exist, a new list is created. \n
			:param filename: string Filename or complete file path; file extension can be omitted.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:LIST:SELect {param}')
