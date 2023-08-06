from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Constellation:
	"""Constellation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("constellation", core, parent)

	def set(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:IMPort:GALileo<ST>:FILE:CONStellation \n
		Selects the file from that the satellites constellation and navigation data are extracted. Supported file types per GNSS
		system
			Table Header: GNSS system / *.txt / *.alm / *.al3 / *.xml / *.alg / *.rnx / *.<xx>n \n
			- GPS / x / x / x / x / x
			- Galileo / x / x / x / x / x / x
			- GLONASS / x / x / x
			- BeiDou / x / x / x
			- QZSS / x / x / x / x
			- NavIC / x
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string Filename, including file path and file extension.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GALileo{stream_cmd_val}:FILE:CONStellation {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:GNSS:SV:IMPort:GALileo<ST>:FILE:CONStellation \n
		Selects the file from that the satellites constellation and navigation data are extracted. Supported file types per GNSS
		system
			Table Header: GNSS system / *.txt / *.alm / *.al3 / *.xml / *.alg / *.rnx / *.<xx>n \n
			- GPS / x / x / x / x / x
			- Galileo / x / x / x / x / x / x
			- GLONASS / x / x / x
			- BeiDou / x / x / x
			- QZSS / x / x / x / x
			- NavIC / x
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: filename: string Filename, including file path and file extension."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:GALileo{stream_cmd_val}:FILE:CONStellation?')
		return trim_str_response(response)
