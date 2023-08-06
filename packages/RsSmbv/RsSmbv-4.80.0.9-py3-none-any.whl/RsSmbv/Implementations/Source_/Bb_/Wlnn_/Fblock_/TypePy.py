from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.WlannFbType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TYPE \n
		The command selects the PPDU type. \n
			:param type_py: DATA| SOUNding| BEACon| TRIGger DATA Only Data Long Training Fields are used to probe the channel. SOUNding Staggered preambles are used to probe additional dimension of the MIMO channel. Only Physical Layer Mode GREEN FIELD is available. BEACon Frame type 'Beacon' is used to probe the channel.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.WlannFbType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbType:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TYPE \n
		The command selects the PPDU type. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: type_py: DATA| SOUNding| BEACon| TRIGger DATA Only Data Long Training Fields are used to probe the channel. SOUNding Staggered preambles are used to probe additional dimension of the MIMO channel. Only Physical Layer Mode GREEN FIELD is available. BEACon Frame type 'Beacon' is used to probe the channel."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbType)
