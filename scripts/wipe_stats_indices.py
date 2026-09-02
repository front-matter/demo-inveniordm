"""Delete the invenio-stats indices.

`invenio index destroy` only removes registered indices; the stats indices are
created on the fly from templates, so historical statistics survive a wipe
unless they are deleted by name.

Run with: invenio shell wipe_stats_indices.py
"""

from invenio_search.proxies import current_search_client
from invenio_search.utils import prefix_index

patterns = ",".join(prefix_index(p) for p in ("events-stats-*", "stats-*"))
# Wildcards are resolved here because `indices.delete` rejects them when the
# cluster has `action.destructive_requires_name` enabled.
names = sorted(
    current_search_client.indices.get(
        index=patterns,
        ignore_unavailable=True,
        allow_no_indices=True,
        expand_wildcards="all",
    )
)
if names:
    current_search_client.indices.delete(index=",".join(names))
print(f"Stats indices deleted ({patterns}): {len(names)}")
