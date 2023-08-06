from mapz.methods.traverse import (
    ismapping,
    traverse,
    issequence,
)

from typing import Any, Hashable, Iterable, Mapping, List, Optional, Tuple


RowType = Iterable[str]
HeaderType = RowType
TableType = Tuple[HeaderType, List[RowType]]


def to_table(
    mapping: Mapping[Hashable, Any],
    headers: Iterable[str] = ["Key", "Value"],
    indentation: str = "  ",
    limit: int = 0,
) -> TableType:
    """Transform mapping into a table structure.

    Returns tuple of headers and rows.
    Returned structure is suitable for printing by Cleo library.
    """

    def builder(k: Any, v: Any, **kwargs: Any) -> Optional[Tuple[Any, Any]]:

        rows = kwargs["rows"]
        limit = kwargs["limit"]
        depth = kwargs["_depth"]
        index = kwargs["_index"]
        ancestors = kwargs["_ancestors"]

        # Render keys by default as:
        table_key = indentation * (depth - 1) + str(k)

        if (
            len(ancestors) > 1
            and ismapping(ancestors[-1])
            and issequence(ancestors[-2])
        ):
            # If node has two or more ancestors, then check if it's a
            # mapping within a list. Because in that case it must be
            # rendered as in YAML:
            # my_list
            #   - key1      value1
            #     key2      value2
            if index:
                table_key = indentation * (depth - 1) + str(k)
            else:
                table_key = indentation * (depth - 2) + "- " + str(k)

        elif ancestors and issequence(ancestors[-1]):
            # Render child items of lists as just a dash with proper indent
            table_key = indentation * (depth - 1) + "-"

        if not limit or limit and len(rows) < limit:

            value = ""
            if not (ismapping(v) or issequence(v)):
                s = " ".join(
                    str(v).replace("\n", " ").replace("\t", " ").split()
                )
                value = s if len(s) < 80 else f"{s[:76]}..."

            # Ignore empty lines with no key and no value.
            # Example: List of Mappings will result in such row.
            if not k and not value:
                return None

            rows.append([table_key, value])

        return None

    rows: List[RowType] = []
    traverse(
        mapping,
        visitor=builder,
        key_order=lambda keys: sorted(keys),
        rows=rows,
        limit=limit,
    )

    if limit and len(rows) >= limit:
        rows.append(["...", "..."])

    return (headers, rows)
