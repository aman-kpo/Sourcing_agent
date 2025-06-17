import os
from dotenv import load_dotenv
from ai_outreach_crew.crew import RecruitmentCrew
from datetime import date
from ai_outreach_crew.tools.elite_evaluator import evaluate_candidate_gpt, generate_outreach_message_gpt, send_smartlead_email
import json
import asyncio
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Example: List of jobs to process (in practice, load from a file or database)
jobs = [
    {
        "organization": "Rimot.io.",
        "website": "https://bluegrid.energy/",
        "role": "DevOps Developer",
        "description": "Rimot io  is looking for a DevOps developer. Work will be on Tyscript and Python codebases. CICD, piepline development and deployment.",
        "location": "Halifax, Nova Scotia",
        "start_date": "June 30, 2024",
        "category": "Full-Time",
        "current_date": date.today().strftime("%Y-%m-%d"),
    },
    # Add more job dicts here for batch processing
]

FIT_SCORE_THRESHOLD = 7.0  # Only keep candidates above this score

async def process_job(job):
    logging.info(f"Processing job: {job['role']} at {job['organization']}")
    candidate_profiles_path = "./documents/candidate_profiles.json"
    try:
        RecruitmentCrew().recruitment_crew().kickoff(inputs=job)
        with open(candidate_profiles_path, "r") as f:
            candidates = json.load(f)
    except Exception as e:
        logging.error(f"Error sourcing candidates for {job['role']}: {e}")
        return
    top_candidates = []
    for candidate in candidates:
        try:
            logging.info(f"Evaluating candidate: {candidate.get('name', '')}")
            eval_result = evaluate_candidate_gpt(candidate, job)
            logging.info(f"Evaluation result: {eval_result}")
            # Enhanced fit score parsing
            fit_score = 0.0
            for line in eval_result.splitlines():
                if "Final Fit Score" in line:
                    try:
                        fit_score = float(line.split(":")[-1].split("/")[0].strip())
                        break
                    except Exception:
                        continue
            if fit_score >= FIT_SCORE_THRESHOLD:
                candidate["fit_score"] = fit_score
                candidate["evaluation"] = eval_result
                outreach_msg = generate_outreach_message_gpt(candidate, job)
                candidate["outreach_message"] = outreach_msg
                # Send email via Smartlead
                email_result = send_smartlead_email(candidate, outreach_msg, job)
                candidate["email_result"] = email_result
                # Placeholder for LinkedIn automation
                # send_linkedin_connection_request(candidate, outreach_msg, job)
                top_candidates.append(candidate)
        except Exception as e:
            logging.error(f"Error processing candidate {candidate.get('name', '')}: {e}")
    output_path = f"./documents/top_candidates_{job['role'].replace(' ', '_')}.json"
    try:
        with open(output_path, "w") as f:
            json.dump(top_candidates, f, indent=2)
        logging.info(f"Saved top candidates for {job['role']} to {output_path}")
    except Exception as e:
        logging.error(f"Error saving top candidates for {job['role']}: {e}")

async def main():
    await asyncio.gather(*(process_job(job) for job in jobs))

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
