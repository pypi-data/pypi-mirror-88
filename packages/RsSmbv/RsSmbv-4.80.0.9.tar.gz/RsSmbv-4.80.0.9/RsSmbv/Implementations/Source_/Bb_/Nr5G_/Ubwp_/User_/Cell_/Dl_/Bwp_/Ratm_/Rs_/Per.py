from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Per:
	"""Per commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("per", core, parent)

	def set(self, rate_match_period: enums.RateMatchPeriodictyAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, rateSetting=repcap.RateSetting.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:RATM:RS<GR>:PER \n
		Sets the time-domain pattern. \n
			:param rate_match_period: 1| 2| 5| 4| 8| 10| 20| 40
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSetting: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')"""
		param = Conversions.enum_scalar_to_str(rate_match_period, enums.RateMatchPeriodictyAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		rateSetting_cmd_val = self._base.get_repcap_cmd_value(rateSetting, repcap.RateSetting)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:RATM:RS{rateSetting_cmd_val}:PER {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, rateSetting=repcap.RateSetting.Default) -> enums.RateMatchPeriodictyAll:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:DL:BWP<DIR>:RATM:RS<GR>:PER \n
		Sets the time-domain pattern. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param rateSetting: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Rs')
			:return: rate_match_period: 1| 2| 5| 4| 8| 10| 20| 40"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		rateSetting_cmd_val = self._base.get_repcap_cmd_value(rateSetting, repcap.RateSetting)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:DL:BWP{numSuffix_cmd_val}:RATM:RS{rateSetting_cmd_val}:PER?')
		return Conversions.str_to_scalar_enum(response, enums.RateMatchPeriodictyAll)
