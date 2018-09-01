from flask import render_template, redirect, session, flash
from services import auth_services, assistant_services, user_services
from models import Callback, User, Company, Question
from utilties import helpers
from typing import List



def questionsBuilder(questions: List[Question]):
    json = {}



