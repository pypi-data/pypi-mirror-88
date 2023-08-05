"""Defines the Parser class."""

from typing import Optional, Tuple, TYPE_CHECKING

from .context import RootParseContext
from ..config import FluffConfig

if TYPE_CHECKING:
    from .segments import BaseSegment


class Parser:
    """Instantiates parsed queries from a sequence of lexed raw segments."""

    def __init__(
        self, config: Optional[FluffConfig] = None, dialect: Optional[str] = None
    ):
        # Allow optional config and dialect
        self.config = FluffConfig.from_kwargs(config=config, dialect=dialect)
        self.RootSegment = self.config.get("dialect_obj").get_root_segment()

    def parse(self, segments: Tuple["BaseSegment", ...], recurse=True) -> "BaseSegment":
        """Parse a series of lexed tokens using the current dialect."""
        if not segments:
            raise ValueError("Cannot parse an empty iterable of segments.")
        # Instantiate the root segment
        root_segment = self.RootSegment(segments=segments)
        # Call .parse() on that segment
        with RootParseContext.from_config(config=self.config, recurse=recurse) as ctx:
            parsed = root_segment.parse(parse_context=ctx)
        return parsed
