from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta
import hashlib

class VoteType(Enum):
    YES = 'yes'
    NO = 'no'
    ABSTAIN = 'abstain'

@dataclass
class Vote:
    voter: str
    vote_type: VoteType
    timestamp: datetime
    weight: float = 1.0

@dataclass 
class Proposal:
    id: str
    title: str
    description: str
    creator: str
    created_at: datetime
    expires_at: datetime
    execution_payload: Dict
    votes: List[Vote]
    executed: bool = False
    min_threshold: float = 0.66

    @property
    def total_votes(self) -> Dict[VoteType, float]:
        results = {t: 0.0 for t in VoteType}
        for vote in self.votes:
            results[vote.vote_type] += vote.weight
        return results

    @property
    def is_passed(self) -> bool:
        totals = self.total_votes
        total_weight = sum(totals.values())
        if total_weight == 0:
            return False
        return totals[VoteType.YES] / total_weight >= self.min_threshold

class GovernanceSystem:
    def __init__(self):
        self.proposals: Dict[str, Proposal] = {}
        self.vote_weights: Dict[str, float] = {}

    def create_proposal(
        self,
        title: str,
        description: str,
        creator: str,
        execution_payload: Dict,
        duration_days: int = 7
    ) -> Proposal:
        proposal_id = hashlib.sha256(
            f"{title}{description}{creator}{datetime.now()}".encode()
        ).hexdigest()[:12]

        proposal = Proposal(
            id=proposal_id,
            title=title,
            description=description,
            creator=creator,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=duration_days),
            execution_payload=execution_payload,
            votes=[]
        )
        
        self.proposals[proposal_id] = proposal
        return proposal

    def cast_vote(
        self,
        proposal_id: str,
        voter: str,
        vote_type: VoteType
    ) -> bool:
        if proposal_id not in self.proposals:
            raise ValueError("Invalid proposal ID")

        proposal = self.proposals[proposal_id]
        
        if datetime.now() > proposal.expires_at:
            raise ValueError("Proposal voting period has ended")

        # Remove any existing votes by this voter
        proposal.votes = [v for v in proposal.votes if v.voter != voter]
        
        # Add new vote
        vote = Vote(
            voter=voter,
            vote_type=vote_type,
            timestamp=datetime.now(),
            weight=self.vote_weights.get(voter, 1.0)
        )
        proposal.votes.append(vote)
        return True

    def execute_proposal(self, proposal_id: str) -> bool:
        if proposal_id not in self.proposals:
            raise ValueError("Invalid proposal ID")

        proposal = self.proposals[proposal_id]
        
        if proposal.executed:
            raise ValueError("Proposal already executed")

        if datetime.now() < proposal.expires_at:
            raise ValueError("Voting period not yet complete")

        if not proposal.is_passed:
            raise ValueError("Proposal did not meet required threshold")

        # Execute the proposal's payload
        try:
            # Implementation would vary based on execution_payload format
            # and allowed operations
            print(f"Executing proposal {proposal_id}")
            print(f"Payload: {proposal.execution_payload}")
            proposal.executed = True
            return True
        except Exception as e:
            print(f"Failed to execute proposal: {str(e)}")
            return False

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        return self.proposals.get(proposal_id)

    def get_active_proposals(self) -> List[Proposal]:
        now = datetime.now()
        return [
            p for p in self.proposals.values()
            if p.expires_at > now and not p.executed
        ]
