import os
from swarm_syndicate.core.governance import DecentralizedGovernanceEngine
from swarm_syndicate.core.coordination import SwarmCoordinationManager

# Initialize the decentralized governance engine
gov_engine = DecentralizedGovernanceEngine()

# Initialize the swarm coordination manager
coord_manager = SwarmCoordinationManager()

# Register custom governance protocols and agent behaviors
gov_engine.register_protocol("consensus_based", ConsensusBasedProtocol())
coord_manager.register_agent_behavior("foraging", ForagingBehavior())

# Run the main application loop
if __name__ == "__main__":
    gov_engine.start()
    coord_manager.start()
    # Main application logic...