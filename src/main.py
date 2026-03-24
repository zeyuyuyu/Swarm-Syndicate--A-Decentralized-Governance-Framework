import time
import random
from typing import List

class Voter:
    def __init__(self, id: str):
        self.id = id
        self.votes = []

    def cast_vote(self, proposal_id: str):
        self.votes.append(proposal_id)

class Proposal:
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description
        self.votes = []

    def add_vote(self, voter: Voter):
        self.votes.append(voter.id)

class DecentralizedVotingSystem:
    def __init__(self):
        self.voters: List[Voter] = []
        self.proposals: List[Proposal] = []

    def register_voter(self, voter: Voter):
        self.voters.append(voter)

    def create_proposal(self, proposal: Proposal):
        self.proposals.append(proposal)

    def vote(self, voter: Voter, proposal_id: str):
        voter.cast_vote(proposal_id)
        for proposal in self.proposals:
            if proposal.id == proposal_id:
                proposal.add_vote(voter)
                break

    def tally_votes(self) -> List[Proposal]:
        return sorted(self.proposals, key=lambda p: len(p.votes), reverse=True)

# Example usage
voting_system = DecentralizedVotingSystem()

# Register voters
voter1 = Voter('voter1')
voter2 = Voter('voter2')
voter3 = Voter('voter3')
voting_system.register_voter(voter1)
voting_system.register_voter(voter2)
voting_system.register_voter(voter3)

# Create proposals
proposal1 = Proposal('proposal1', 'Implement decentralized voting')
proposal2 = Proposal('proposal2', 'Add support for multiple currencies')
proposal3 = Proposal('proposal3', 'Improve user interface')
voting_system.create_proposal(proposal1)
voting_system.create_proposal(proposal2)
voting_system.create_proposal(proposal3)

# Cast votes
voting_system.vote(voter1, 'proposal1')
voting_system.vote(voter1, 'proposal2')
voting_system.vote(voter2, 'proposal1')
voting_system.vote(voter2, 'proposal3')
voting_system.vote(voter3, 'proposal1')
voting_system.vote(voter3, 'proposal2')
voting_system.vote(voter3, 'proposal3')

# Tally votes
ranked_proposals = voting_system.tally_votes()
for proposal in ranked_proposals:
    print(f'Proposal: {proposal.description}, Votes: {len(proposal.votes)}')
