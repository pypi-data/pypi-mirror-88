from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Speriod:
	"""Speriod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("speriod", core, parent)

	def set(self, sched_period: enums.EutraMchSchedPer, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:SPERiod \n
		Defines the MCH scheduling period, i.e. the periodicity used for providing MCH scheduling information at lower layers
		(MAC) applicable for an MCH. \n
			:param sched_period: SPM| SPRF8| SPRF16| SPRF32| SPRF64| SPRF128| SPRF256| SPRF512| SPRF1024
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')"""
		param = Conversions.enum_scalar_to_str(sched_period, enums.EutraMchSchedPer)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:SPERiod {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraMchSchedPer:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:SPERiod \n
		Defines the MCH scheduling period, i.e. the periodicity used for providing MCH scheduling information at lower layers
		(MAC) applicable for an MCH. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')
			:return: sched_period: SPM| SPRF8| SPRF16| SPRF32| SPRF64| SPRF128| SPRF256| SPRF512| SPRF1024"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:SPERiod?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMchSchedPer)
