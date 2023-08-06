from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 21 total commands, 4 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alevel(self):
		"""alevel commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_alevel'):
			from .User_.Alevel import Alevel
			self._alevel = Alevel(self._core, self._base)
		return self._alevel

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .User_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def flist(self):
		"""flist commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_flist'):
			from .User_.Flist import Flist
			self._flist = Flist(self._core, self._base)
		return self._flist

	@property
	def slist(self):
		"""slist commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_slist'):
			from .User_.Slist import Slist
			self._slist = Slist(self._core, self._base)
		return self._slist

	def get_load(self) -> str:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.freqresp. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:return: freq_resp_rf_rcl: 'filename' Filename or complete file path; file extension can be omitted
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:LOAD?')
		return trim_str_response(response)

	def set_load(self, freq_resp_rf_rcl: str) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.freqresp. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param freq_resp_rf_rcl: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(freq_resp_rf_rcl)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:LOAD {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:PRESet \n
		Sets the option's parameters to their default values (*RST values specified for the commands) . Not affected is the state
		set with the command CORRection:FRESponse:RF. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:PRESet \n
		Sets the option's parameters to their default values (*RST values specified for the commands) . Not affected is the state
		set with the command CORRection:FRESponse:RF. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:PRESet')

	def get_store(self) -> str:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:STORe \n
		Saves the current settings into the selected file; the file extension (*.freqresp) is assigned automatically. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:return: freq_resp_rf_save: 'filename' Filename or complete file path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:STORe?')
		return trim_str_response(response)

	def set_store(self, freq_resp_rf_save: str) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:STORe \n
		Saves the current settings into the selected file; the file extension (*.freqresp) is assigned automatically. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param freq_resp_rf_save: 'filename' Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(freq_resp_rf_save)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:STORe {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:[STATe] \n
		Enables/disables the frequency response correction. \n
			:return: freq_resp_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, freq_resp_state: bool) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:[STATe] \n
		Enables/disables the frequency response correction. \n
			:param freq_resp_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(freq_resp_state)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:STATe {param}')
