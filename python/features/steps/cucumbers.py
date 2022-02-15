from behave import *
from behave.log_capture import capture
from hypothesis import given as hypothesis_given
from hypothesis.strategies import integers

runs = {}
def run_once(func):
    def wrapper():
        if id(func) not in runs:
            func()
    return wrapper

def eat_cucumbers(start, amount):
    return start - amount

def buy_cucumbers(start, amount):
    return start + amount

@given('there are {start} cucumbers')
def step_impl(context, start):
    context.start_num = int(start)

@when('I eat {eat} cucumbers')
def step_impl(context, eat):
    context.eat_num = int(eat)

@then('I should have {left} cucumbers left')
def step_impl(context, left):
    assert eat_cucumbers(context.start_num, context.eat_num) == int(left)

@step('In general, I should have fewer cucumbers than I start with')
def step_impl(context):
    test_eating_cucumbers()

@when("I buy 5 cucumbers")
def step_impl(context):
    context.eat_num = 5

@then('I should have 20 cucumbers')
def step_impl(context):
    assert buy_cucumbers(context.start_num, context.eat_num) == 20

@step('In general, I should have more cucumbers than I start with')
def step_impl(context):
    test_buying_cucumbers()

@hypothesis_given(integers(min_value=0), integers(min_value=0))
def test_eating_cucumbers(start, amount):
    assert eat_cucumbers(start, amount) <= start

@hypothesis_given(integers(), integers())
def test_buying_cucumbers(start, amount):
    assert buy_cucumbers(start, amount) >= start