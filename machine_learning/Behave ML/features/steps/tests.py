from behave import Given, When, Then

from make_model import get_testing_set
from make_model import model_creator

#drop_features1 = ['PassengerId', 'Name','Ticket','Cabin','Survived']
#drop_features2 = ['PassengerId', 'Name','Ticket','Cabin','Survived','Fare']
#model1 = model_creator(drop_features1)
#model2 = model_creator(drop_features2)


@Given("a model created by dropping these features {drop_features1}")
def given_incrementor(context, drop_features1: str):
    context.drop_features1 = drop_features1.split(",")
    context.model1 = model_creator(context.drop_features1)


@When("we create a model dropping one more dependent feature {drop_features2}")
def when_incrementor(context, drop_features2: str):
    context.drop_features2 = drop_features2.split(",")
    context.model2 = model_creator(context.drop_features2)


@Then("their testing accuracies should be {result}")
def then_results(context, result: str):
    assert(result == check(context.drop_features1,context.drop_features2,context.model1,context.model2))


def check(drop_features1, drop_features2, model1, model2):
    X_test1, y_test1 = get_testing_set(drop_features1)
    X_test2, y_test2 = get_testing_set(drop_features2)

    score1 = model1.score(X_test1, y_test1)
    score2 = model2.score(X_test2, y_test2)

    print(score1)
    print(score2)

    diff = score1-score2
    if diff<0.1:
        print('very similar')
        return 'very similar'
    else:
        print('not similar')
        return 'not similar'


#print(check(drop_features1,drop_features2,model1,model2))
