"""AI Outreach Crew - Recruitment automation using CrewAI"""

from .crew import RecruitmentCrew
from .elite_evaluator import evaluate_candidate_gpt, generate_outreach_message_gpt

all = ['RecruitmentCrew', 'evaluate_candidate_gpt', 'generate_outreach_message_gpt']


ai_outreach_crew/tools/init.py
"""Custom tools for the AI Outreach Crew"""

from .tools.custom_tools import search_candidates, evaluate_candidate

all = ['search_candidates', 'evaluate_candidate']
﻿
