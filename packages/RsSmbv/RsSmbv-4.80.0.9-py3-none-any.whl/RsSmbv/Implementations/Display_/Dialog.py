from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dialog:
	"""Dialog commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dialog", core, parent)

	def close(self, dialog_id: str) -> None:
		"""DISPlay:DIALog:CLOSe \n
		Closes the specified dialog. \n
			:param dialog_id: string To find out the dialog identifier, use the query method RsSmbv.Display.Dialog.id. The DialogName part of the query result is sufficient.
		"""
		param = Conversions.value_to_quoted_str(dialog_id)
		self._core.io.write(f'DISPlay:DIALog:CLOSe {param}')

	def close_all(self) -> None:
		"""DISPlay:DIALog:CLOSe:ALL \n
		Closes all open dialogs. \n
		"""
		self._core.io.write(f'DISPlay:DIALog:CLOSe:ALL')

	def close_all_with_opc(self) -> None:
		"""DISPlay:DIALog:CLOSe:ALL \n
		Closes all open dialogs. \n
		Same as close_all, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'DISPlay:DIALog:CLOSe:ALL')

	def get_id(self) -> str:
		"""DISPlay:DIALog:ID \n
		Returns the dialog identifiers of the open dialogs in a string separated by blanks. \n
			:return: dialog_id_list: DialogID#1 DialogID#2 ... DialogID#n Dialog identifiers are string without blanks. Blanks are represented as $$. Dialog identifiers DialogID are composed of two main parts: DialogName[OptionalParts] DialogName Meaningful information, mandatory input parameter for the commands: method RsSmbv.Display.Dialog.open method RsSmbv.Display.Dialog.close Optional parts String of $X values, where X is a character, interpreted as follows: $qDialogQualifier: optional dialog qualifier, usually the letter A or B, as displayed in the dialog title. $iInstances: comma-separated list of instance indexes, given in the order h,c,s,d,g,u,0. Default is zero; the terminating ',0' can be omitted. $tTabIds: comma-separated indexes or tab names; required, if a dialog is composed of several tabs. $xLeft$yTop$hLeft$wTop: position and size; superfluous information.
		"""
		response = self._core.io.query_str('DISPlay:DIALog:ID?')
		return trim_str_response(response)

	def open(self, dialog_id: str) -> None:
		"""DISPlay:DIALog:OPEN \n
		Opens the specified dialog. \n
			:param dialog_id: string To find out the dialog identifier, use the query method RsSmbv.Display.Dialog.id. The DialogName part of the query result is mandatory.
		"""
		param = Conversions.value_to_quoted_str(dialog_id)
		self._core.io.write(f'DISPlay:DIALog:OPEN {param}')
