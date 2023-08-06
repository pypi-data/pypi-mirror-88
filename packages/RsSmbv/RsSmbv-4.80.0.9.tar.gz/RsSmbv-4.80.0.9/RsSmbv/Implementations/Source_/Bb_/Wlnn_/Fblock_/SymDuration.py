from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymDuration:
	"""SymDuration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symDuration", core, parent)

	def set(self, he_ltf_sym_dur: enums.WlannFbPpduHeLtfSymbDuraion, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SYMDuration \n
		Selects the duration of the HE long training field (LTF) .The symbol duration value does not include the guard interval. \n
			:param he_ltf_sym_dur: SD32| SD64| SD128
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(he_ltf_sym_dur, enums.WlannFbPpduHeLtfSymbDuraion)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SYMDuration {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbPpduHeLtfSymbDuraion:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SYMDuration \n
		Selects the duration of the HE long training field (LTF) .The symbol duration value does not include the guard interval. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: he_ltf_sym_dur: SD32| SD64| SD128"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SYMDuration?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPpduHeLtfSymbDuraion)
