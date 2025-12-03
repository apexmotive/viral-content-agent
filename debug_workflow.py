
import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

import config
from workflow.graph import run_workflow

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_workflow():
    print("🚀 Testing Workflow Logic")
    
    # Mock settings
    config.MAX_ITERATIONS = 3
    config.VIRALITY_THRESHOLD = 99 # High threshold to force loops
    
    topic = "Test Topic"
    platform = "twitter"
    
    print(f"Config: Max Iterations={config.MAX_ITERATIONS}, Threshold={config.VIRALITY_THRESHOLD}")
    
    # Run workflow
    final_state = run_workflow(topic, platform)
    
    print("\n✅ Workflow Complete")
    print(f"Final Status: {final_state.get('status')}")
    print(f"Iteration Count: {final_state.get('iteration_count')}")
    print(f"Scores: {final_state.get('scores')}")
    print(f"Drafts count: {len(final_state.get('drafts'))}")

if __name__ == "__main__":
    test_workflow()
