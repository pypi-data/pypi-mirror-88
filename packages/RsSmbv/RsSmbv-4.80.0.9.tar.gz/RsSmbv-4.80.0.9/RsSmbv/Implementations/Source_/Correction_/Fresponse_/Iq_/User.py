from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 21 total commands, 4 Sub-groups, 4 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

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
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:LOAD \n
		No command help available \n
			:return: freq_resp_iq_rcl: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:LOAD?')
		return trim_str_response(response)

	def set_load(self, freq_resp_iq_rcl: str) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:LOAD \n
		No command help available \n
			:param freq_resp_iq_rcl: No help available
		"""
		param = Conversions.value_to_quoted_str(freq_resp_iq_rcl)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:LOAD {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:PRESet')

	def get_store(self) -> str:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:STORe \n
		No command help available \n
			:return: freq_resp_iq_save: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:STORe?')
		return trim_str_response(response)

	def set_store(self, freq_resp_iq_save: str) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:STORe \n
		No command help available \n
			:param freq_resp_iq_save: No help available
		"""
		param = Conversions.value_to_quoted_str(freq_resp_iq_save)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:STORe {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:[STATe] \n
		No command help available \n
			:return: freq_corr_iq_stat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, freq_corr_iq_stat: bool) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:[STATe] \n
		No command help available \n
			:param freq_corr_iq_stat: No help available
		"""
		param = Conversions.bool_to_str(freq_corr_iq_stat)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:STATe {param}')
