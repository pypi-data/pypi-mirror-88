from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:DCONflict:[STATe] \n
		The command queries whether there is (response 1) or is not (response 0) a conflict (overlap) in the
		hierarchically-structured channelization codes. The cause of a possible domain conflict can be ascertained by manual
		operation in the 'BS > Code Domain' dialog. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: state: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:DCONflict:STATe?')
		return Conversions.str_to_bool(response)
