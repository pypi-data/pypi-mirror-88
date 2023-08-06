from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zero:
	"""Zero commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zero", core, parent)

	def set(self, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:[POWer]:ZERO \n
		Performs zeroing of the sensor. Zeroing is required after warm-up, i.e. after connecting the sensor. Note: Switch off or
		disconnect the RF power source from the sensor before zeroing.
			INTRO_CMD_HELP: We recommend that you zero in regular intervals (at least once a day) , if: \n
			- The temperature has varied more than about 5 °C.
			- The sensor has been replaced.
			- You want to measure very low power. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:ZERO')

	def set_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""SENSe<CH>:[POWer]:ZERO \n
		Performs zeroing of the sensor. Zeroing is required after warm-up, i.e. after connecting the sensor. Note: Switch off or
		disconnect the RF power source from the sensor before zeroing.
			INTRO_CMD_HELP: We recommend that you zero in regular intervals (at least once a day) , if: \n
			- The temperature has varied more than about 5 °C.
			- The sensor has been replaced.
			- You want to measure very low power. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		self._core.io.write_with_opc(f'SENSe{channel_cmd_val}:POWer:ZERO')
