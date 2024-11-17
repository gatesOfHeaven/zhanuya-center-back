from fastapi import APIRouter, status, HTTPException, Path, Query, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils import connect_db
from utils.facades import auth
from entities.user import User
from entities.workday import WorkdayQuery
from entities.slot import SlotQuery
from entities.medical_record import MedicalRecordQuery


router = APIRouter()


