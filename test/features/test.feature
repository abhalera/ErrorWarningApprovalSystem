Feature: Getting Started With Aruba
  Scenario: First Run of Command
    Given I successfully run `~/github/ErrorWarningApprovalSystem/bin/ErrorWarningApproval.py`
    Then the output should contain:
    """
    Hello, Aruba!
    """
