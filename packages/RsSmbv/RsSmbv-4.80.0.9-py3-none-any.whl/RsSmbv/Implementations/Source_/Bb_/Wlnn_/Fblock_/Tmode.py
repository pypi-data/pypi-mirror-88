from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmode", core, parent)

	def set(self, tm_ode: enums.WlannFbTxMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TMODe \n
		Sets the Tx mode. The available Tx modes are dependent on the physical mode. \n
			:param tm_ode: L20| LDUP| LUP| LLOW| HT20| HT40| HTDup| HTUP| HTLow| CCK| PBCC| V20| V40| V80| V160| V8080| L10| S1| S2| S4| S16| HE20| HE40| HE80| HE8080| HE160| EHT320 | L20| LDUP| LUP| LLOW| HT20| HT40| HTDup| HTUP| HTLow| CCK| PBCC| V20| V40| V80| V160| V8080| L10| S1| S2| S4| S16| HE20| HE40| HE80| HE8080| HE160
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(tm_ode, enums.WlannFbTxMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TMODe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbTxMode:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:TMODe \n
		Sets the Tx mode. The available Tx modes are dependent on the physical mode. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: tm_ode: L20| LDUP| LUP| LLOW| HT20| HT40| HTDup| HTUP| HTLow| CCK| PBCC| V20| V40| V80| V160| V8080| L10| S1| S2| S4| S16| HE20| HE40| HE80| HE8080| HE160| EHT320 | L20| LDUP| LUP| LLOW| HT20| HT40| HTDup| HTUP| HTLow| CCK| PBCC| V20| V40| V80| V160| V8080| L10| S1| S2| S4| S16| HE20| HE40| HE80| HE8080| HE160"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbTxMode)
