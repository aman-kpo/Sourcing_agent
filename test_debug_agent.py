from smart_sourcing_agent import SmartSourcingAgent

agent = SmartSourcingAgent()
job_desc = "DevOps Engineer for Information Technology startup in San Francisco"
candidates = agent.find_top_candidates(job_desc, 3)
print(f"\n🎉 FINAL RESULT: {len(candidates)} candidates found")

for i, candidate in enumerate(candidates):
    print(f"\nCandidate {i+1}:")
    print(f"  Overall Fit: {candidate['score'].get('overall_fit', 0)}")
    print(f"  Title: {candidate['profile']['title']}")
    print(f"  URL: {candidate['profile']['url']}") 