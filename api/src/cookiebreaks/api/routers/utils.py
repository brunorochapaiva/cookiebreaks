from datetime import datetime
from typing import Optional

from arrow import Arrow
from cookiebreaks.core.database import get_break_objects
from cookiebreaks.core.structs import (
    BreakFilters,
    User,
    Break as BreakInternal,
    Claim as ClaimInternal,
)
from dataclasses import dataclass


@dataclass
class BreakExternal:
    id: int
    break_time: datetime
    location: str
    holiday: bool
    host: Optional[str]
    break_announced: Optional[datetime]
    cost: Optional[float]
    host_reimbursed: Optional[datetime]
    admin_claimed: Optional[datetime]
    admin_reimbursed: Optional[datetime]


def arrow_to_datetime(original: Arrow | None) -> datetime | None:
    if original:
        return original.datetime
    else:
        return None


def break_internal_to_external(
    internal: BreakInternal, current_user: Optional[User]
) -> BreakExternal:
    if current_user and current_user.admin:
        break_announced = arrow_to_datetime(internal.break_announced)
        cost = internal.cost
        host_reimbursed = arrow_to_datetime(internal.host_reimbursed)
        admin_claimed = arrow_to_datetime(internal.admin_claimed)
        admin_reimbursed = arrow_to_datetime(internal.admin_reimbursed)
    else:
        break_announced = None
        cost = None
        host_reimbursed = None
        admin_claimed = None
        admin_reimbursed = None
    return BreakExternal(
        internal.id,
        internal.break_time.datetime,
        internal.location,
        internal.holiday,
        internal.host,
        break_announced,
        cost,
        host_reimbursed,
        admin_claimed,
        admin_reimbursed,
    )


@dataclass
class ClaimExternal:
    id: int
    claim_date: datetime
    breaks_claimed: list[BreakExternal]
    claim_amount: float
    claim_reimbursed: Optional[datetime]


def claim_internal_to_external(
    internal: ClaimInternal, current_user: Optional[User]
) -> ClaimExternal:
    return ClaimExternal(
        internal.id,
        internal.claim_date.datetime,
        list(
            map(
                lambda b: break_internal_to_external(b, current_user),
                internal.breaks_claimed,
            )
        ),
        internal.claim_amount,
        arrow_to_datetime(internal.claim_reimbursed),
    )


def get_breaks(
    filters: BreakFilters = BreakFilters(), current_user: Optional[User] = None
):
    breaks = get_break_objects(filters)
    return list(map(lambda b: break_internal_to_external(b, current_user), breaks))
