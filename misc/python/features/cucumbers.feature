Feature: eating cucumbers

  Scenario Outline: eating
    Given there are <start> cucumbers
    When I eat <eat> cucumbers
    Then I should have <left> cucumbers left

    * In general, I should have fewer cucumbers than I start with

    Examples:
      | start | eat | left |
      |    12 |   5 |    7 |

  Scenario: buying
    Given there are 15 cucumbers
    When I buy 5 cucumbers
    Then I should have 20 cucumbers

    * In general, I should have more cucumbers than I start with