from src.agents.agent_router import route_query

agent, recommendation = route_query(input(
    "default: 'What is the current best movie released lately on netflix' -->  "
    ) or "What is the current best movie released lately on netflix"
    )

print(f"agent: {agent}")
print(f"recommendation: {recommendation}")
