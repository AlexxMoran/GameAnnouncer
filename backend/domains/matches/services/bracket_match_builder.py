import math

from domains.matches.model import Match
from domains.matches.repository import MatchRepository
from domains.participants.model import AnnouncementParticipant
from enums import MatchStatus


class BracketMatchBuilder:
    """
    Callable service that builds and wires all Match records for a single-elimination bracket.

    Handles creating Match objects for all rounds, persisting them,
    linking them via next_match_winner_id, and propagating BYE winners.
    Does not handle seeding logic — seeding_slots and assigned seeds are
    provided by the caller.

    Third-place match design note:
        The third-place match is created with no participants. Its participant slots
        (participant1_id / participant2_id) must be populated by the match result
        recording service when both semifinal matches are completed — the losers
        of those matches become the third-place participants. The Match model does
        not have a next_match_loser_id field, so this linking is deferred to result
        recording logic.

    Usage:
        builder = BracketMatchBuilder(announcement_id=1, third_place_match=True)
        await builder.call(eligible, bracket_size, seeding_slots, match_repo)
        await session.flush()
    """

    def __init__(self, announcement_id: int, third_place_match: bool) -> None:
        self._announcement_id = announcement_id
        self._third_place_match = third_place_match

    async def call(
        self,
        eligible: list[AnnouncementParticipant],
        bracket_size: int,
        seeding_slots: list[int],
        match_repo: MatchRepository,
    ) -> None:
        """
        Build all Match records, persist them, link rounds, and propagate BYEs.

        Must be followed by session.flush() from the caller to finalise changes.
        """
        matches_by_round = self._build_matches(eligible, bracket_size, seeding_slots)

        all_matches = []
        for round_matches in matches_by_round.values():
            all_matches.extend(round_matches)
        await match_repo.save_many(all_matches)

        self._link_next_matches(matches_by_round)
        self._propagate_byes(matches_by_round)

    def _build_matches(
        self,
        eligible: list[AnnouncementParticipant],
        bracket_size: int,
        seeding_slots: list[int],
    ) -> dict[int, list[Match]]:
        """
        Create all Match objects for every round without persisting.

        Round 1 is built from seeding_slots — a slot with no matching participant
        produces a BYE match where the present participant advances automatically.
        Rounds 2..num_rounds are empty PENDING matches.
        A third-place match is added at the semifinal round when enabled.
        """
        num_rounds = int(math.log2(bracket_size))
        matches_by_round: dict[int, list[Match]] = {}

        matches_by_round[1] = self._build_first_round(
            eligible, seeding_slots, bracket_size
        )

        for round_number in range(2, num_rounds + 1):
            previous_non_third = [
                m for m in matches_by_round[round_number - 1] if not m.is_third_place
            ]
            match_count = len(previous_non_third) // 2
            matches_by_round[round_number] = [
                Match(
                    announcement_id=self._announcement_id,
                    round_number=round_number,
                    match_number=match_number,
                    status=MatchStatus.PENDING,
                )
                for match_number in range(1, match_count + 1)
            ]

        if num_rounds >= 2 and self._third_place_match:
            semifinal_round = num_rounds - 1
            matches_by_round[semifinal_round].append(
                Match(
                    announcement_id=self._announcement_id,
                    round_number=semifinal_round,
                    match_number=3,
                    status=MatchStatus.PENDING,
                    is_third_place=True,
                )
            )

        return matches_by_round

    def _build_first_round(
        self,
        eligible: list[AnnouncementParticipant],
        seeding_slots: list[int],
        bracket_size: int,
    ) -> list[Match]:
        """
        Build round 1 matches by pairing participants from seeding_slots.

        Each pair of consecutive slots forms one match.
        A slot with no participant produces a BYE match — the other participant
        is immediately set as the winner.
        """
        participant_by_seed = {p.seed: p for p in eligible}
        matches = []

        for match_number in range(1, bracket_size // 2 + 1):
            top = participant_by_seed.get(seeding_slots[(match_number - 1) * 2])
            bottom = participant_by_seed.get(seeding_slots[(match_number - 1) * 2 + 1])

            if top is None or bottom is None:
                advancing = top or bottom
                matches.append(
                    Match(
                        announcement_id=self._announcement_id,
                        round_number=1,
                        match_number=match_number,
                        participant1_id=top.id if top else None,
                        participant2_id=bottom.id if bottom else None,
                        winner_id=advancing.id if advancing else None,
                        status=MatchStatus.BYE,
                        is_bye=True,
                    )
                )
            else:
                matches.append(
                    Match(
                        announcement_id=self._announcement_id,
                        round_number=1,
                        match_number=match_number,
                        participant1_id=top.id,
                        participant2_id=bottom.id,
                        status=MatchStatus.PENDING,
                    )
                )

        return matches

    def _link_next_matches(self, matches_by_round: dict[int, list[Match]]) -> None:
        """
        Set next_match_winner_id on each match to link the bracket progression.

        Round R match M advances to Round R+1 match ceil(M/2).
        Odd-numbered match fills participant1 slot; even fills participant2 slot.
        Third-place matches are not linked forward.

        Requires matches to be already persisted so that IDs are assigned.
        """
        num_rounds = max(matches_by_round.keys())
        for round_number in range(1, num_rounds):
            next_round_matches = matches_by_round.get(round_number + 1, [])
            next_match_by_number = {
                m.match_number: m for m in next_round_matches if not m.is_third_place
            }
            for match in matches_by_round[round_number]:
                if match.is_third_place:
                    continue
                next_match_number = math.ceil(match.match_number / 2)
                next_match = next_match_by_number.get(next_match_number)
                if next_match:
                    match.next_match_winner_id = next_match.id

    def _propagate_byes(self, matches_by_round: dict[int, list[Match]]) -> None:
        """
        Propagate BYE winners from round 1 into their round 2 participant slots.

        Odd-numbered BYE → fills participant1_id of the next match.
        Even-numbered BYE → fills participant2_id of the next match.
        If both slots are filled after propagation, the match status becomes READY.
        """
        second_round_matches = {
            m.match_number: m
            for m in matches_by_round.get(2, [])
            if not m.is_third_place
        }
        for bye_match in matches_by_round.get(1, []):
            if not bye_match.is_bye or bye_match.winner_id is None:
                continue
            next_match_number = math.ceil(bye_match.match_number / 2)
            next_match = second_round_matches.get(next_match_number)
            if next_match is None:
                continue
            if bye_match.match_number % 2 == 1:
                next_match.participant1_id = bye_match.winner_id
            else:
                next_match.participant2_id = bye_match.winner_id
            if next_match.participant1_id and next_match.participant2_id:
                next_match.status = MatchStatus.READY
