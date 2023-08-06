# mautrix-instagram - A Matrix-Instagram puppeting bridge.
# Copyright (C) 2020 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import List, Any, Optional

from attr import dataclass
from mautrix.types import SerializableAttrs

from .thread import Thread, ThreadUser


@dataclass
class DMInboxCursor(SerializableAttrs['DMInboxCursor']):
    cursor_timestamp_seconds: int
    cursor_thread_v2_id: int


@dataclass
class DMInbox(SerializableAttrs['DMInbox']):
    threads: List[Thread]
    has_older: bool
    unseen_count: int
    unseen_count_ts: int
    prev_cursor: DMInboxCursor
    next_cursor: DMInboxCursor
    blended_inbox_enabled: bool
    newest_cursor: Optional[str] = None
    oldest_cursor: Optional[str] = None


@dataclass
class DMInboxResponse(SerializableAttrs['DMInboxResponse']):
    status: str
    seq_id: int
    snapshot_at_ms: int
    pending_requests_total: int
    has_pending_top_requests: bool
    viewer: ThreadUser
    inbox: DMInbox
    # TODO type
    most_recent_inviter: Any = None


@dataclass
class DMThreadResponse(SerializableAttrs['DMThreadResponse']):
    thread: Thread
    status: str
