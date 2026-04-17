"""Serialize matplotlib figures to base64-encoded PNG strings."""

from __future__ import annotations

import base64
import io

from matplotlib.figure import Figure


def figure_to_base64(fig: Figure, dpi: int = 150) -> str:
    """Render a matplotlib Figure to a base64-encoded PNG string.

    The caller is responsible for closing the figure after this function
    returns.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    buf.close()
    return encoded
