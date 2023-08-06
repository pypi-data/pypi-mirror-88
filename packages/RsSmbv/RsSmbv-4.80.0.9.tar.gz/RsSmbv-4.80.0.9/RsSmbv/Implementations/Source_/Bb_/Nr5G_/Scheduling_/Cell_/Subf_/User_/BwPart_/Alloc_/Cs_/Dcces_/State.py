from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, dummy_cce_state: enums.CoresetUnusedRes, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCCes:STATe \n
		Defines if unused CORSET resources (CCEs) are used for data transmission or not. \n
			:param dummy_cce_state: 0| 1| ALLowpdsch 0 Disables data transmission in the unused CCEs. 1 Fills unused CCEs with dummy data, as set with the command method RsSmbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.Cs.Dcces.Data.set. ALLowpdsch Allows PDSCH transmission in the unused CCEs.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(dummy_cce_state, enums.CoresetUnusedRes)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCCes:STATe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.CoresetUnusedRes:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCCes:STATe \n
		Defines if unused CORSET resources (CCEs) are used for data transmission or not. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: dummy_cce_state: 0| 1| ALLowpdsch 0 Disables data transmission in the unused CCEs. 1 Fills unused CCEs with dummy data, as set with the command method RsSmbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.Cs.Dcces.Data.set. ALLowpdsch Allows PDSCH transmission in the unused CCEs."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCCes:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.CoresetUnusedRes)
