Feature: Apple Search and Cart

  Scenario: Open Apple homepage
    Given I am on the Apple homepage

  Scenario: Search for the product
    When I search for the product

  Scenario: Add the product to the bag
    When I add the first product result to the bag
    Then I should be able to proceed to the review bag
    Then a screenshot of the reviewed product should be taken

  Scenario: Delete product or item from the bag
    Then the product should be removed or deleted from the bag

  Scenario: Close the browser
    Then I close the browser
