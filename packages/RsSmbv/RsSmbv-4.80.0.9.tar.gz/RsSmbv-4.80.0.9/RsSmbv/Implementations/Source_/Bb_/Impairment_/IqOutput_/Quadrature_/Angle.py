from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Angle:
	"""Angle commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("angle", core, parent)

	def set(self, angle: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:BB:IMPairment:IQOutput<CH>:QUADrature:[ANGLe] \n
		Sets a quadrature offset (phase angle) between the I and Q vectors deviating from the ideal 90 degrees.
		A positive quadrature offset results in a phase angle greater than 90 degrees. Value range
			Table Header: Impairments / Min [dB] / Max [dB] / Resolution \n
			- Digital / 30 / 30 / 0.01
			- Analog / 10 / 10 / 0.01 \n
			:param angle: float Range: -30 to 30, Unit: DEG
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')"""
		param = Conversions.decimal_value_to_str(angle)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:IQOutput{channel_cmd_val}:QUADrature:ANGLe {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce]:BB:IMPairment:IQOutput<CH>:QUADrature:[ANGLe] \n
		Sets a quadrature offset (phase angle) between the I and Q vectors deviating from the ideal 90 degrees.
		A positive quadrature offset results in a phase angle greater than 90 degrees. Value range
			Table Header: Impairments / Min [dB] / Max [dB] / Resolution \n
			- Digital / 30 / 30 / 0.01
			- Analog / 10 / 10 / 0.01 \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'IqOutput')
			:return: angle: float Range: -30 to 30, Unit: DEG"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:IQOutput{channel_cmd_val}:QUADrature:ANGLe?')
		return Conversions.str_to_float(response)
