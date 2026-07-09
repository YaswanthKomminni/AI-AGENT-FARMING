import sys, os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.farming_agent import process_farming_query

tests = [
    # On-topic questions
    ("What crop should I grow in black soil?", True),
    ("Will it rain tomorrow in Pune?", True),
    ("Tomato mandi prices in Maharashtra?", True),
    ("PM Kisan Yojana subsidy eligibility?", True),
    ("How to treat yellow spots on rice leaves?", True),
    
    # Greetings & Meta questions (should be allowed)
    ("Hello!", True),
    ("Who are you?", True),
    ("What can you do?", True),
    
    # Off-topic questions (should be blocked)
    ("Who is the president of USA?", False),
    ("What is 10 + 20?", False),
    ("Write a Python script to reverse a string.", False),
    ("Tell me a joke about cats.", False),
    ("What is the capital of France?", False),
    
    # Advanced off-topic questions (using generic keywords - should be blocked)
    ("What is the price of gold?", False),
    ("What is the temperature of the sun?", False),
    ("How much water should I drink daily?", False),
    ("Which government is in power in the UK?", False),
    
    # Advanced off-topic questions (sneaking farming terms into blacklist words - should be blocked)
    ("Tell me a joke about farming.", False),
    ("Write a python script to calculate crop yield.", False),
]

async def run_tests():
    print("FarmWise AI — Guardrails & Topic Restriction Test (v2)")
    print("=" * 65)
    all_ok = True
    for query, expected_allowed in tests:
        res = await process_farming_query(query)
        ans = res["answer"]
        is_blocked = "I can only help with questions related to farming" in ans
        allowed = not is_blocked
        
        status = "OK  " if allowed == expected_allowed else "FAIL"
        if allowed != expected_allowed:
            all_ok = False
        print(f"  {status}  [expected={expected_allowed}, got={allowed}] '{query}'")
        
    print("=" * 65)
    print("Guardrails check: " + ("ALL PASSED" if all_ok else "SOME FAILED"))
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    asyncio.run(run_tests())
