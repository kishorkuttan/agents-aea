# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the abstract class defining an agent's strategy for the TAC."""

import copy
import random
from enum import Enum
from typing import Dict, List, Optional, Tuple, cast

from aea.decision_maker.default import OwnershipState, Preferences
from aea.helpers.search.generic import (
    AGENT_LOCATION_MODEL,
    AGENT_REMOVE_SERVICE_MODEL,
    AGENT_SET_SERVICE_MODEL,
)
from aea.helpers.search.models import (
    Constraint,
    ConstraintType,
    Description,
    Location,
    Query,
)
from aea.protocols.signing.message import SigningMessage
from aea.skills.base import Model

from packages.fetchai.skills.tac_negotiation.dialogues import FipaDialogue
from packages.fetchai.skills.tac_negotiation.helpers import (
    build_goods_description,
    build_goods_query,
)
from packages.fetchai.skills.tac_negotiation.transactions import Transactions


ROUNDING_ADJUSTMENT = 1
DEFAULT_LOCATION = {"longitude": 51.5194, "latitude": 0.1270}
DEFAULT_SERVICE_KEY = "tac_service"
DEFAULT_SEARCH_QUERY = {
    "search_key": "tac_service",
    "search_value": "generic_service",
    "constraint_type": "==",
}
DEFAULT_SEARCH_RADIUS = 5.0


class Strategy(Model):
    """This class defines an abstract strategy for the agent."""

    class RegisterAs(Enum):
        """This class defines the service registration options."""

        SELLER = "seller"
        BUYER = "buyer"
        BOTH = "both"

    class SearchFor(Enum):
        """This class defines the service search options."""

        SELLERS = "sellers"
        BUYERS = "buyers"
        BOTH = "both"

    def __init__(self, **kwargs) -> None:
        """
        Initialize the strategy of the agent.

        :param register_as: determines whether the agent registers as seller, buyer or both
        :param search_for: determines whether the agent searches for sellers, buyers or both

        :return: None
        """
        self._register_as = Strategy.RegisterAs(kwargs.pop("register_as", "both"))
        self._search_for = Strategy.SearchFor(kwargs.pop("search_for", "both"))
        self._is_contract_tx = kwargs.pop("is_contract_tx", False)
        self._ledger_id = kwargs.pop("ledger_id", "ethereum")

        location = kwargs.pop("location", DEFAULT_LOCATION)
        self._agent_location = {
            "location": Location(location["longitude"], location["latitude"])
        }
        service_key = kwargs.pop("service_key", DEFAULT_SERVICE_KEY)
        self._set_service_data = {"key": service_key, "value": self._register_as.value}
        self._remove_service_data = {"key": service_key}
        self._simple_service_data = {service_key: self._register_as.value}
        self._search_query = {
            "search_key": service_key,
            "search_value": self._search_for.value,
            "constraint_type": "==",
        }
        self._radius = kwargs.pop("search_radius", DEFAULT_SEARCH_RADIUS)

        super().__init__(**kwargs)

    @property
    def registering_as(self) -> str:
        """Get what the agent is registering as."""
        return (
            self._register_as.value
            if self._register_as != self.RegisterAs.BOTH
            else "buyer and seller"
        )

    @property
    def searching_for(self) -> str:
        """Get what the agent is searching for."""
        return (
            self._search_for.value
            if self._search_for != self.SearchFor.BOTH
            else "buyer and seller"
        )

    @property
    def searching_for_types(self) -> List[Tuple[bool, str]]:
        result = []  # type: List[Tuple[bool, str]]
        if self._search_for in [self.SearchFor.SELLERS, self.SearchFor.BOTH]:
            result.append((True, "sellers"))
        if self._search_for in [self.SearchFor.BUYERS, self.SearchFor.BOTH]:
            result.append((False, "buyers"))
        return result

    # @property
    # def is_registering_as_seller(self) -> bool:
    #     """Check if the agent registers as a seller on the OEF service directory."""
    #     return (
    #         self._register_as == Strategy.RegisterAs.SELLER
    #         or self._register_as == Strategy.RegisterAs.BUYER
    #     )

    # @property
    # def is_searching_for_sellers(self) -> bool:
    #     """Check if the agent searches for sellers on the OEF service directory."""
    #     return (
    #         self._search_for == Strategy.SearchFor.SELLERS
    #         or self._search_for == Strategy.SearchFor.BOTH
    #     )

    # @property
    # def is_registering_as_buyer(self) -> bool:
    #     """Check if the agent registers as a buyer on the OEF service directory."""
    #     return (
    #         self._register_as == Strategy.RegisterAs.BUYER
    #         or self._register_as == Strategy.RegisterAs.BOTH
    #     )

    # @property
    # def is_searching_for_buyers(self) -> bool:
    #     """Check if the agent searches for buyers on the OEF service directory."""
    #     return (
    #         self._search_for == Strategy.SearchFor.BUYERS
    #         or self._search_for == Strategy.SearchFor.BOTH
    #     )

    @property
    def is_contract_tx(self) -> bool:
        """Check if tx are made against the ERC1155 or not."""
        return self._is_contract_tx

    @property
    def ledger_id(self) -> str:
        """Get the ledger id."""
        return self._ledger_id

    def get_location_description(self) -> Description:
        """
        Get the location description.

        :return: a description of the agent's location
        """
        description = Description(
            self._agent_location, data_model=AGENT_LOCATION_MODEL,
        )
        return description

    def get_register_service_description(self) -> Description:
        """
        Get the register service description.

        :return: a description of the offered services
        """
        description = Description(
            self._set_service_data, data_model=AGENT_SET_SERVICE_MODEL,
        )
        return description

    def get_unregister_service_description(self) -> Description:
        """
        Get the unregister service description.

        :return: a description of the to be removed service
        """
        description = Description(
            self._remove_service_data, data_model=AGENT_REMOVE_SERVICE_MODEL,
        )
        return description

    def get_location_and_service_query(self) -> Query:
        """
        Get the location and service query of the agent.

        :return: the query
        """
        close_to_my_service = Constraint(
            "location",
            ConstraintType(
                "distance", (self._agent_location["location"], self._radius)
            ),
        )
        service_key_filter = Constraint(
            self._search_query["search_key"],
            ConstraintType(
                self._search_query["constraint_type"],
                self._search_query["search_value"],
            ),
        )
        query = Query([close_to_my_service, service_key_filter],)
        return query

    def get_own_service_description(self, is_supply: bool) -> Description:
        """
        Get the description of the supplied goods (as a seller), or the demanded goods (as a buyer).
        :param is_supply: Boolean indicating whether it is supply or demand.
        :return: the description (to advertise on the Service Directory).
        """
        transactions = cast(Transactions, self.context.transactions)
        ownership_state_after_locks = transactions.ownership_state_after_locks(
            is_seller=is_supply
        )
        quantities_by_good_id = (
            self._supplied_goods(ownership_state_after_locks.quantities_by_good_id)
            if is_supply
            else self._demanded_goods(ownership_state_after_locks.quantities_by_good_id)
        )
        currency_id = next(
            iter(ownership_state_after_locks.amount_by_currency_id.keys())
        )
        desc = build_goods_description(
            quantities_by_good_id=quantities_by_good_id,
            currency_id=currency_id,
            ledger_id=self.ledger_id,
            is_supply=is_supply,
        )
        return desc

    @staticmethod
    def _supplied_goods(good_holdings: Dict[str, int]) -> Dict[str, int]:
        """
        Generate a dictionary of quantities which are supplied.

        :param good_holdings: a dictionary of current good holdings
        :return: a dictionary of quantities supplied
        """
        supply = {}  # type: Dict[str, int]
        for good_id, quantity in good_holdings.items():
            supply[good_id] = quantity - 1 if quantity > 1 else 0
        return supply

    @staticmethod
    def _demanded_goods(good_holdings: Dict[str, int]) -> Dict[str, int]:
        """
        Generate a dictionary of quantities which are demanded.

        :param good_holdings: a dictionary of current good holdings
        :return: a dictionary of quantities supplied
        """
        demand = {}  # type: Dict[str, int]
        for good_id in good_holdings.keys():
            demand[good_id] = 1
        return demand

    def get_own_services_query(self, is_searching_for_sellers: bool,) -> Query:
        """
        Build a query.

        In particular, build the query to look for agents
            - which supply the agent's demanded goods (i.e. sellers), or
            - which demand the agent's supplied goods (i.e. buyers).

        :param is_searching_for_sellers: Boolean indicating whether the search is for sellers or buyers.

        :return: the Query, or None.
        """
        transactions = cast(Transactions, self.context.transactions)
        ownership_state_after_locks = transactions.ownership_state_after_locks(
            is_seller=not is_searching_for_sellers
        )
        good_id_to_quantities = (
            self._demanded_goods(ownership_state_after_locks.quantities_by_good_id)
            if is_searching_for_sellers
            else self._supplied_goods(ownership_state_after_locks.quantities_by_good_id)
        )
        currency_id = next(
            iter(ownership_state_after_locks.amount_by_currency_id.keys())
        )
        query = build_goods_query(
            good_ids=list(good_id_to_quantities.keys()),
            currency_id=currency_id,
            ledger_id=self.ledger_id,
            is_searching_for_sellers=is_searching_for_sellers,
        )
        return query

    def _get_proposal_for_query(
        self, query: Query, is_seller: bool
    ) -> Optional[Description]:
        """
        Generate proposal (in the form of a description) which matches the query.

        :param query: the query for which to build the proposal
        :is_seller: whether the agent making the proposal is a seller or not

        :return: a description
        """
        candidate_proposals = self._generate_candidate_proposals(is_seller)
        proposals = []
        for proposal in candidate_proposals:
            if not query.check(proposal):
                continue
            proposals.append(proposal)
        if not proposals:
            return None
        else:
            return random.choice(proposals)  # nosec

    def get_proposal_for_query(
        self, query: Query, role: FipaDialogue.Role
    ) -> Optional[Description]:
        """
        Generate proposal (in the form of a description) which matches the query.

        :param query: the query for which to build the proposal
        :param role: the role of the agent making the proposal (seller or buyer)

        :return: a description
        """
        is_seller = role == FipaDialogue.Role.SELLER

        own_service_description = self.get_own_service_description(is_supply=is_seller,)
        if not query.check(own_service_description):
            self.context.logger.debug("current holdings do not satisfy CFP query.")
            return None
        else:
            proposal_description = self._get_proposal_for_query(
                query, is_seller=is_seller
            )
            if proposal_description is None:
                self.context.logger.debug(
                    "current strategy does not generate proposal that satisfies CFP query."
                )
            return proposal_description

    def _generate_candidate_proposals(self, is_seller: bool):
        """
        Generate proposals from the agent in the role of seller/buyer.

        :param is_seller: the bool indicating whether the agent is a seller.

        :return: a list of proposals in Description form
        """
        transactions = cast(Transactions, self.context.transactions)
        ownership_state_after_locks = transactions.ownership_state_after_locks(
            is_seller=is_seller
        )
        good_id_to_quantities = (
            self._supplied_goods(ownership_state_after_locks.quantities_by_good_id)
            if is_seller
            else self._demanded_goods(ownership_state_after_locks.quantities_by_good_id)
        )
        nil_proposal_dict = {
            good_id: 0 for good_id in good_id_to_quantities.keys()
        }  # type: Dict[str, int]
        proposals = []
        fee_by_currency_id = self.context.shared_state.get("tx_fee", {"FET": 0})
        buyer_tx_fee = next(iter(fee_by_currency_id.values()))
        ownership_state = cast(
            OwnershipState, self.context.decision_maker_handler_context.ownership_state
        )
        currency_id = list(ownership_state.amount_by_currency_id.keys())[0]
        preferences = cast(
            Preferences, self.context.decision_maker_handler_context.preferences
        )
        for good_id, quantity in good_id_to_quantities.items():
            if is_seller and quantity == 0:
                continue
            proposal_dict = copy.copy(nil_proposal_dict)
            proposal_dict[good_id] = 1
            proposal = build_goods_description(
                quantities_by_good_id=proposal_dict,
                currency_id=currency_id,
                ledger_id=self.ledger_id,
                is_supply=is_seller,
            )
            if is_seller:
                delta_quantities_by_good_id = {
                    good_id: quantity * -1
                    for good_id, quantity in proposal_dict.items()
                }  # type: Dict[str, int]
            else:
                delta_quantities_by_good_id = proposal_dict
            marginal_utility_from_delta_good_holdings = preferences.marginal_utility(
                ownership_state=ownership_state_after_locks,
                delta_quantities_by_good_id=delta_quantities_by_good_id,
            )
            switch = -1 if is_seller else 1
            breakeven_price_rounded = (
                round(marginal_utility_from_delta_good_holdings) * switch
            )
            if is_seller:
                proposal.values["price"] = breakeven_price_rounded + ROUNDING_ADJUSTMENT
            else:
                proposal.values["price"] = (
                    breakeven_price_rounded - buyer_tx_fee - ROUNDING_ADJUSTMENT
                )
            proposal.values["fee"] = buyer_tx_fee
            if not proposal.values["price"] > 0:
                continue
            nonce = transactions.get_next_nonce()
            proposal.values["nonce"] = nonce
            proposals.append(proposal)
        return proposals

    def is_profitable_transaction(
        self, signing_msg: SigningMessage, role: FipaDialogue.Role
    ) -> bool:
        """
        Check if a transaction is profitable.

        Is it a profitable transaction?
        - apply all the locks for role.
        - check if the transaction is consistent with the locks (enough money/holdings)
        - check that we gain score.

        :param signing_msg: the signing_msg
        :param role: the role of the agent (seller or buyer)

        :return: True if the transaction is good (as stated above), False otherwise.
        """
        is_seller = role == FipaDialogue.Role.SELLER

        transactions = cast(Transactions, self.context.transactions)
        ownership_state_after_locks = transactions.ownership_state_after_locks(
            is_seller
        )
        if not ownership_state_after_locks.is_affordable_transaction(signing_msg.terms):
            return False
        preferences = cast(
            Preferences, self.context.decision_maker_handler_context.preferences
        )
        proposal_delta_score = preferences.utility_diff_from_transaction(
            ownership_state_after_locks, signing_msg.terms
        )
        if proposal_delta_score >= 0:
            return True
        else:
            return False
