from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

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
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Data_.Dselect import Dselect
			self._dselect = Dselect(self._core, self._base)
		return self._dselect

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Data_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	def set(self, data: enums.DataSour, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:CHANnel<CH>:DPDCh:DATA \n
		The command determines the data source for the selected DPDCH. For the enhanced channels of user equipment 1 (UE1) , this
		entry is valid when channel coding is deactivated. When channel coding is active, data sources are selected for the
		transport channels with the commands BB:W3GPp:MST:CHANnel:DPDCh:DCCH:DATA and BB:W3GPp:MST:ENHanced:TCHannel:DATA. \n
			:param data: PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| ZERO | ONE| PATTern PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Channel.Dpdch.Data.Dselect.set. ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Channel.Dpdch.Data.Pattern.set.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSour)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DPDCh:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.DataSour:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:CHANnel<CH>:DPDCh:DATA \n
		The command determines the data source for the selected DPDCH. For the enhanced channels of user equipment 1 (UE1) , this
		entry is valid when channel coding is deactivated. When channel coding is active, data sources are selected for the
		transport channels with the commands BB:W3GPp:MST:CHANnel:DPDCh:DCCH:DATA and BB:W3GPp:MST:ENHanced:TCHannel:DATA. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: data: PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| ZERO | ONE| PATTern PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Channel.Dpdch.Data.Dselect.set. ZERO | ONE Internal 0 and 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Channel.Dpdch.Data.Pattern.set."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DPDCh:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)
