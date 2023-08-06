from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	def set(self, source: enums.DataSour, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MPDU<ST>:DATA:SOURce \n
		Selects the data source. \n
			:param source: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command BB:WLNN:FBLch:MPDUst:DATA:DSEL ZERO | ONE Internal 0 or 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command BB:WLNN:FBLch:MPDUst:DATA:PATT.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mpdu')"""
		param = Conversions.enum_scalar_to_str(source, enums.DataSour)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MPDU{stream_cmd_val}:DATA:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, availableUser=repcap.AvailableUser.Default, stream=repcap.Stream.Default) -> enums.DataSour:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:[USER<DI>]:MPDU<ST>:DATA:SOURce \n
		Selects the data source. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:param availableUser: optional repeated capability selector. Default value: Nr0 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mpdu')
			:return: source: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt PNxx The pseudo-random sequence generator is used as the data source. Different random sequence lengths can be selected. DLISt A data list is used. The data list is selected with the command BB:WLNN:FBLch:MPDUst:DATA:DSEL ZERO | ONE Internal 0 or 1 data is used. PATTern Internal data is used. The bit pattern for the data is defined by the command BB:WLNN:FBLch:MPDUst:DATA:PATT."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		availableUser_cmd_val = self._base.get_repcap_cmd_value(availableUser, repcap.AvailableUser)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:USER{availableUser_cmd_val}:MPDU{stream_cmd_val}:DATA:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.DataSour)
