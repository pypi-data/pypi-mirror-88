from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slist:
	"""Slist commands group definition. 7 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slist", core, parent)

	def clone(self) -> 'Slist':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Slist(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ports(self):
		"""ports commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ports'):
			from .Slist_.Ports import Ports
			self._ports = Ports(self._core, self._base)
		return self._ports

	@property
	def select(self):
		"""select commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_select'):
			from .Slist_.Select import Select
			self._select = Select(self._core, self._base)
		return self._select

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Slist_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def get_catalog(self) -> str:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt:CATalog?')
		return trim_str_response(response)

	def clear(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt:CLEar \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt:CLEar')

	def clear_with_opc(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt:CLEar \n
		No command help available \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt:CLEar')

	def get_size(self) -> int:
		"""[SOURce<HW>]:CORRection:FRESponse:IQ:USER:SLISt:SIZE \n
		No command help available \n
			:return: freq_resp_iq_sli_si: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:IQ:USER:SLISt:SIZE?')
		return Conversions.str_to_int(response)
