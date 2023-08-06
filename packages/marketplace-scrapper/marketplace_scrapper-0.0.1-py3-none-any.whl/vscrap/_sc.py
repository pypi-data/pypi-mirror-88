""""
Get details of an VS or VSCODE extension from marketplace
details are [title, publisher_name, installs, default_image]
All you need is the extension id
"""
from typing import Dict, Any

from ._scrap import _retrieve_extension_page, _m_address, _extract_details


def rap(extension_id: str) -> Dict[str, Any]:
    """Connect scrap"""
    # retrieve page
    page_text = _retrieve_extension_page(
        _m_address(extension_id)
    )

    # extract details
    return _extract_details(page_text) if page_text else {}
