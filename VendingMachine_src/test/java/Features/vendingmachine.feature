Feature: Vending Machine

  Background:
    Given the cost of a drink is $200

  Scenario: Buying a toonie drink
    Given I inserted a toonie
    When I select a $200 drink
    Then I should have a drink
    And no change to return

  Scenario Outline: Change
    When I insert a $<initial> coin
    And I press the return change button
    Then I should have $<initial> in change

    Examples:
      | initial |
      |     200 |
      |      25 |
      |      75 |