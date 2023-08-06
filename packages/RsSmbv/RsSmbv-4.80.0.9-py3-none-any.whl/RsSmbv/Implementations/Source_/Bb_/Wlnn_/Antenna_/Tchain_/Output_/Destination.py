from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Destination:
	"""Destination commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("destination", core, parent)

	def set(self, destination: enums.WlannTxOutpDest, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:ANTenna:TCHain<CH>:OUTPut:DESTination \n
		Selects the destination of the calculated IQ chains. \n
			:param destination: OFF| BB| BB_B| FILE OFF No mapping takes place. BB The IQ chain is output to the baseband A. Exactly one output stream can be mapped as 'Baseband A'. FILE The IQ chain is saved in a file.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tchain')"""
		param = Conversions.enum_scalar_to_str(destination, enums.WlannTxOutpDest)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:ANTenna:TCHain{channel_cmd_val}:OUTPut:DESTination {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannTxOutpDest:
		"""[SOURce<HW>]:BB:WLNN:ANTenna:TCHain<CH>:OUTPut:DESTination \n
		Selects the destination of the calculated IQ chains. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tchain')
			:return: destination: OFF| BB| BB_B| FILE OFF No mapping takes place. BB The IQ chain is output to the baseband A. Exactly one output stream can be mapped as 'Baseband A'. FILE The IQ chain is saved in a file."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:ANTenna:TCHain{channel_cmd_val}:OUTPut:DESTination?')
		return Conversions.str_to_scalar_enum(response, enums.WlannTxOutpDest)
