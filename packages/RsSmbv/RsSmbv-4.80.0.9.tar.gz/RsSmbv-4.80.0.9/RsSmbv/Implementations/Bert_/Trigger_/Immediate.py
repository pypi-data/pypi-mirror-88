from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	def set(self) -> None:
		"""BERT:TRIGger:[IMMediate] \n
		For method RsSmbv.Bert.Trigger.mode|method RsSmbv.Bler.Trigger.mode SING, triggers a single bit error rate or block error
		rate measurement. \n
		"""
		self._core.io.write(f'BERT:TRIGger:IMMediate')

	def set_with_opc(self) -> None:
		"""BERT:TRIGger:[IMMediate] \n
		For method RsSmbv.Bert.Trigger.mode|method RsSmbv.Bler.Trigger.mode SING, triggers a single bit error rate or block error
		rate measurement. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'BERT:TRIGger:IMMediate')
