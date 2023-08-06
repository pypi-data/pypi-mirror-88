from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Index:
	"""Index commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("index", core, parent)

	def set(self, index: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:MAC:INDex \n
		Sets the MAC Index used for the selected user. MAC Index has to be different for the different users. However, in case
		that two users are using the same value for MAC Index, the lower priority user is disabled, or be unable to enable. The
		values for the MAC Indexes for the other users (see method RsSmbv.Source.Bb.Evdo.Anetwork.ouCount) are assigned from a
		pool of valid MAC Indexes. \n
			:param index: integer Range: 5 to 63 for physical layer subtype 0&1, 6 to 127 for physical layer subtype 2, 4 to 383 for physical layer subtype 3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(index)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:MAC:INDex {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:MAC:INDex \n
		Sets the MAC Index used for the selected user. MAC Index has to be different for the different users. However, in case
		that two users are using the same value for MAC Index, the lower priority user is disabled, or be unable to enable. The
		values for the MAC Indexes for the other users (see method RsSmbv.Source.Bb.Evdo.Anetwork.ouCount) are assigned from a
		pool of valid MAC Indexes. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: index: integer Range: 5 to 63 for physical layer subtype 0&1, 6 to 127 for physical layer subtype 2, 4 to 383 for physical layer subtype 3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:MAC:INDex?')
		return Conversions.str_to_int(response)
