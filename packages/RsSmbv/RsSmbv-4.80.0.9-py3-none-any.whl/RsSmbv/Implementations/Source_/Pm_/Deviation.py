from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("deviation", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ModulationDevMode:
		"""[SOURce<HW>]:PM:DEViation:MODE \n
		Selects the coupling mode. The coupling mode parameter also determines the mode for fixing the total deviation. \n
			:return: pm_dev_mode: UNCoupled| TOTal| RATio UNCoupled Does not couple the LF signals. The deviation values of both paths are independent. TOTal Couples the deviation of both paths. RATio Couples the deviation ratio of both paths
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PM:DEViation:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationDevMode)

	def set_mode(self, pm_dev_mode: enums.ModulationDevMode) -> None:
		"""[SOURce<HW>]:PM:DEViation:MODE \n
		Selects the coupling mode. The coupling mode parameter also determines the mode for fixing the total deviation. \n
			:param pm_dev_mode: UNCoupled| TOTal| RATio UNCoupled Does not couple the LF signals. The deviation values of both paths are independent. TOTal Couples the deviation of both paths. RATio Couples the deviation ratio of both paths
		"""
		param = Conversions.enum_scalar_to_str(pm_dev_mode, enums.ModulationDevMode)
		self._core.io.write(f'SOURce<HwInstance>:PM:DEViation:MODE {param}')

	def get_sum(self) -> float:
		"""[SOURce<HW>]:PM:DEViation:SUM \n
		Sets the total deviation of the LF signal when using combined signal sources in phase modulation. \n
			:return: pm_dev_sum: float Range: 0 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PM:DEViation:SUM?')
		return Conversions.str_to_float(response)

	def set_sum(self, pm_dev_sum: float) -> None:
		"""[SOURce<HW>]:PM:DEViation:SUM \n
		Sets the total deviation of the LF signal when using combined signal sources in phase modulation. \n
			:param pm_dev_sum: float Range: 0 to 20
		"""
		param = Conversions.decimal_value_to_str(pm_dev_sum)
		self._core.io.write(f'SOURce<HwInstance>:PM:DEViation:SUM {param}')

	def set(self, deviation: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:PM<CH>:[DEViation] \n
		Sets the modulation deviation of the phase modulation in RAD. \n
			:param deviation: float The maximal deviation depends on the RF frequency and the selected modulation mode (see data sheet) . Range: 0 to max, Unit: RAD
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pm')"""
		param = Conversions.decimal_value_to_str(deviation)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:PM{channel_cmd_val}:DEViation {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce]:PM<CH>:[DEViation] \n
		Sets the modulation deviation of the phase modulation in RAD. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pm')
			:return: deviation: float The maximal deviation depends on the RF frequency and the selected modulation mode (see data sheet) . Range: 0 to max, Unit: RAD"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:PM{channel_cmd_val}:DEViation?')
		return Conversions.str_to_float(response)
