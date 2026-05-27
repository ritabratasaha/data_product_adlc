import json
import subprocess
import sys

def run_all_evals(json_path):
    try:
        # 1. Load the evals JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Could not read or parse {json_path}: {e}")
        return

    skill_name = data.get("skill_name", "Unknown Skill")
    eval_cases = data.get("evals", [])
    
    print("=" * 60)
    print(f"🎯 Target Skill: {skill_name}")
    print(f"📋 Found {len(eval_cases)} evaluation tests to run.")
    print("=" * 60 + "\n")

    # 2. Iterate through each eval block in the JSON file
    for case in eval_cases:
        eval_id = case.get("id")
        name = case.get("name")
        prompt_list = case.get("prompt", [])
        
        # 3. Combine the prompt array into a clean block of multi-line text
        compiled_prompt = "\n".join(prompt_list)
        
        print(f"🔄 Running Test [{eval_id}]: {name}")
        print("🤖 Claude is scanning your workspace files...")
        print("-" * 60)
        
        try:
            # 4. Fire the prompt to the Claude CLI
            result = subprocess.run(
                ["claude", "-p", compiled_prompt],
                capture_output=True,
                text=True,
                timeout=90  # Keeps the execution safe for large scans
            )
            
            # 5. Output whatever Claude returns right onto the screen
            print(result.stdout)
            
            if result.stderr:
                print(f"⚠️ System Messages/Stderr:\n{result.stderr}")

        except subprocess.TimeoutExpired:
            print("⏳ Execution stopped: Test exceeded the 90-second limit.")
        except Exception as e:
            print(f"💥 Failed to execute this test: {e}")
            
        print("=" * 60 + "\n")

if __name__ == "__main__":
    # Uses 'evals.json' by default, or you can pass a path: python run_all_evals.py alternative.json
    target_file = sys.argv[1] if len(sys.argv) > 1 else ".claude/skills/data-product-engineering/evals/evals.json"
    run_all_evals(target_file)