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
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt:CATalog \n
		Queries the S-parameter files included in the current S-paramters list. \n
			:return: catalog: filename1,filename2,...filename10 Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt:CATalog?')
		return trim_str_response(response)

	def clear(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt:CLEar \n
		Deletes all entries in the lists. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt:CLEar')

	def clear_with_opc(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt:CLEar \n
		Deletes all entries in the lists. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt:CLEar')

	def get_size(self) -> int:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:USER:SLISt:SIZE \n
		Queries the number of files in the list. \n
			:return: freq_resp_rfs_li_si: integer Range: 0 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:FRESponse:RF:USER:SLISt:SIZE?')
		return Conversions.str_to_int(response)
