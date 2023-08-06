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
from typing import Optional
from attr import dataclass

from mautrix.types import SerializableAttrs

from .login import LoginResponseUser


@dataclass
class ChallengeStateData(SerializableAttrs['ChallengeStateData']):
    # Only for reset step
    choice: Optional[str] = None
    fb_access_token: Optional[str] = None
    big_blue_token: Optional[str] = None
    google_oauth_token: Optional[str] = None
    email: Optional[str] = None

    # Only for verify email step
    security_code: Optional[str] = None
    resend_delay: Optional[int] = None
    contact_point: Optional[str] = None
    form_type: Optional[str] = None


@dataclass(kw_only=True)
class ChallengeStateResponse(SerializableAttrs['ChallengeStateResponse']):
    # TODO enum?
    step_name: str
    step_data: ChallengeStateData
    logged_in_user: Optional[LoginResponseUser] = None
    user_id: int
    nonce_code: str
    # TODO enum?
    action: Optional[str] = None
    status: str

    # flow_render_type: int
    # bloks_action: str
    # challenge_context: str
    # challenge_type_enum_str: str
