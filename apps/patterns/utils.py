import arrow
import re
from typing import Tuple, Optional, List

def epoch_to_date_string(epoch: int) -> str:
    return arrow.get(epoch).format('YYYY-MM-DD')


def epoch_to_datetime_string(epoch: int) -> str:
    return arrow.get(epoch).format('YYYY-MM-DD HH:mm:SS')


def module_matches_any_pattern_and_match(
    node_module: str,
    full_model_import_regex: str,
    app_import_regex: str,
    local_import_regex: str,
    app_name_regex: str,
    elements_imported: List[str],
) -> Tuple[bool, Optional[str]]:

    # Covers "from apps.app1.models"
    match_for_full_model_import = re.match(full_model_import_regex, node_module)
    if bool(match_for_full_model_import):
        return True, match_for_full_model_import.group("app")

    # Covers from "apps.app1 import models"
    match_for_app_import = re.match(app_import_regex, node_module)
    if bool(match_for_app_import) and "models" in elements_imported:
        return True, match_for_app_import.group("app")

    # Covers "from ..app1.models"
    match_for_local_import = re.match(local_import_regex, node_module)
    if not node_module.startswith("apps.") and bool(match_for_local_import):
        return True, match_for_local_import.group("app")

    # Covers "from ..app1 import models"
    match_for_app_name = re.match(app_name_regex, node_module)
    if bool(match_for_app_name) and "models" in elements_imported:
        return True, match_for_app_name.group("app")

    return False, None
