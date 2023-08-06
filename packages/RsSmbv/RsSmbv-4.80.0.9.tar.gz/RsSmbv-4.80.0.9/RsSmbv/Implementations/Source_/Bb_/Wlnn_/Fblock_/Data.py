from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 5 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dcycle(self):
		"""dcycle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcycle'):
			from .Data_.Dcycle import Dcycle
			self._dcycle = Dcycle(self._core, self._base)
		return self._dcycle

	@property
	def dselection(self):
		"""dselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselection'):
			from .Data_.Dselection import Dselection
			self._dselection = Dselection(self._core, self._base)
		return self._dselection

	@property
	def fduration(self):
		"""fduration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fduration'):
			from .Data_.Fduration import Fduration
			self._fduration = Fduration(self._core, self._base)
		return self._fduration

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Data_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def set(self, data: enums.WlannDataSource, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA \n
		Selects the data source. \n
			:param data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| AMPDU PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command BB:WLNN:FBLocks:DATA:DSEL ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command BB:WLNN:FBLocks:DATA:PATTern. AMPDU Aggregated mac protocol data unit (A-MPDU) data is used as configured with the commands in 'MPDU Configuration'
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(data, enums.WlannDataSource)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannDataSource:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA \n
		Selects the data source. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| AMPDU PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command BB:WLNN:FBLocks:DATA:DSEL ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command BB:WLNN:FBLocks:DATA:PATTern. AMPDU Aggregated mac protocol data unit (A-MPDU) data is used as configured with the commands in 'MPDU Configuration'"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.WlannDataSource)
