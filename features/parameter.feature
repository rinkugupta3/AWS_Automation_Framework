Feature: Apple Search and Cart

  Scenario: Open Apple homepage
    Given I am on the Apple homepage

  Scenario Outline: Search for a product
    When I search for "<product>"
    When I add the first "<product>" result to the bag
    Then I should be able to proceed to the review bag
    And a screenshot of the reviewed "<product>" should be taken
    Then the "<product>" should be removed or deleted from the bag
    Then I return to the Apple homepage

  Examples:
    | product         |
    | iPhone 16 Pro   |
    | MacBook Pro     |

  # Scenario: Delete product or item from the bag
    # Then the "<product>" should be removed or deleted from the bag
    # Then the product should be removed or deleted from the bag

  Scenario: Close the browser
    Then I close the browser