from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Create:
	"""Create commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("create", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CREate \n
		Creates a multi-carrier waveform using the current settings of the carrier table. Use the command method RsSmbv.Source.Bb.
		Arbitrary.Mcarrier.ofile to define the multi-carrier waveform file name. The file extension is *.wv. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CREate')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CREate \n
		Creates a multi-carrier waveform using the current settings of the carrier table. Use the command method RsSmbv.Source.Bb.
		Arbitrary.Mcarrier.ofile to define the multi-carrier waveform file name. The file extension is *.wv. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CREate')
