from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phase:
	"""Phase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phase", core, parent)

	def set(self, phase: float, channel=repcap.Channel.Default, txIx=repcap.TxIx.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:ANTenna:TCHain<CH>:TX<DIR>:PHASe \n
		Sets the phase when cylindrical mapping coordinates are selected. \n
			:param phase: float Range: 0 to 359.99
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tchain')
			:param txIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')"""
		param = Conversions.decimal_value_to_str(phase)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		txIx_cmd_val = self._base.get_repcap_cmd_value(txIx, repcap.TxIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:ANTenna:TCHain{channel_cmd_val}:TX{txIx_cmd_val}:PHASe {param}')

	def get(self, channel=repcap.Channel.Default, txIx=repcap.TxIx.Default) -> float:
		"""[SOURce<HW>]:BB:WLNN:ANTenna:TCHain<CH>:TX<DIR>:PHASe \n
		Sets the phase when cylindrical mapping coordinates are selected. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tchain')
			:param txIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tx')
			:return: phase: float Range: 0 to 359.99"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		txIx_cmd_val = self._base.get_repcap_cmd_value(txIx, repcap.TxIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:ANTenna:TCHain{channel_cmd_val}:TX{txIx_cmd_val}:PHASe?')
		return Conversions.str_to_float(response)
