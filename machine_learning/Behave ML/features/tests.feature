
Feature: Testing the incrementor

  Scenario: Test if removing a dependant variable changes anything
    Given a model created by dropping these features PassengerId,Name,Ticket,Cabin,Survived
    When we create a model dropping one more dependent feature PassengerId,Name,Ticket,Cabin,Survived,Fare
    Then their testing accuracies should be very similar


