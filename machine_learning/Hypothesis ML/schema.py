#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:36:57 2022

@author: claremcmullen
"""
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class SexEnum(str, Enum):
    female = "female"
    male = "male"
    
class PclassEnum(str,Enum):
    one = "1"
    two = "2"
    three = "3"
    
    
class EmbarkedEnum(str,Enum):
    C = "C"
    Q = "Q"
    S = "S"

class TitanicModelInput(BaseModel):
    """Schema for input of the model's predict method."""

    Age: Optional[int] = Field(None, title="Age", ge=1, le=100, description="The age of the passenger.")
    
    Sex: SexEnum = Field(..., title="Sex", description="The gender of the passenger.")
    
    Pclass: PclassEnum = Field(..., title='Pclass',description='The class of the passenger, 1,2 or 3.')
    
    Sibsp: Optional[int] = Field(None, title="SibSp", ge=0, le=5, description='The number of siblings that the passenger has travelling with them.')
    
    Parch: Optional[int] = Field(None, title="Parch", ge=0, le=2, description="The number of parents the passenger has travelling with them.")

    Fare: Optional[float] = Field(None, title="Fare", ge=0.0, le=100.0, description="The age of the passenger.")

    Embarked: EmbarkedEnum = Field(..., title="Embarked", description="Where the passenger got on.")

class TitanicModelOutput(BaseModel):
    """Schema for output of the model's predict method."""
    Survived: bool = Field(..., title="Survived", description="Whether the passenger survived.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    