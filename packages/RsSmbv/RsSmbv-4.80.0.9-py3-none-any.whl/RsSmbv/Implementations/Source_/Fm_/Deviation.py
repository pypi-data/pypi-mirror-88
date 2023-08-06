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
		"""[SOURce<HW>]:FM:DEViation:MODE \n
		Selects the coupling mode. The coupling mode parameter also determines the mode for fixing the total deviation. \n
			:return: fm_dev_mode: UNCoupled| TOTal| RATio UNCoupled Does not couple the LF signals. The deviation values of both paths are independent. TOTal Couples the deviation of both paths. RATio Couples the deviation ratio of both paths
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FM:DEViation:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationDevMode)

	def set_mode(self, fm_dev_mode: enums.ModulationDevMode) -> None:
		"""[SOURce<HW>]:FM:DEViation:MODE \n
		Selects the coupling mode. The coupling mode parameter also determines the mode for fixing the total deviation. \n
			:param fm_dev_mode: UNCoupled| TOTal| RATio UNCoupled Does not couple the LF signals. The deviation values of both paths are independent. TOTal Couples the deviation of both paths. RATio Couples the deviation ratio of both paths
		"""
		param = Conversions.enum_scalar_to_str(fm_dev_mode, enums.ModulationDevMode)
		self._core.io.write(f'SOURce<HwInstance>:FM:DEViation:MODE {param}')

	def get_sum(self) -> float:
		"""[SOURce<HW>]:FM:DEViation:SUM \n
		Sets the total deviation of the LF signal when using combined signal sources in frequency modulation. \n
			:return: fm_dev_sum: float Range: 0 to 40E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FM:DEViation:SUM?')
		return Conversions.str_to_float(response)

	def set_sum(self, fm_dev_sum: float) -> None:
		"""[SOURce<HW>]:FM:DEViation:SUM \n
		Sets the total deviation of the LF signal when using combined signal sources in frequency modulation. \n
			:param fm_dev_sum: float Range: 0 to 40E6
		"""
		param = Conversions.decimal_value_to_str(fm_dev_sum)
		self._core.io.write(f'SOURce<HwInstance>:FM:DEViation:SUM {param}')

	def set(self, deviation: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:FM<CH>:[DEViation] \n
		Sets the modulation deviation of the frequency modulation in Hz. \n
			:param deviation: float The maximum deviation depends on the RF frequency and the selected modulation mode (see data sheet) . Range: 0 to max
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fm')"""
		param = Conversions.decimal_value_to_str(deviation)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:FM{channel_cmd_val}:DEViation {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:FM<CH>:[DEViation] \n
		Sets the modulation deviation of the frequency modulation in Hz. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fm')
			:return: deviation: float The maximum deviation depends on the RF frequency and the selected modulation mode (see data sheet) . Range: 0 to max"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:FM{channel_cmd_val}:DEViation?')
		return Conversions.str_to_float(response)
