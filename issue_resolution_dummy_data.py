
# ISSUES

{
  "1": {
    "transaction_id": "T1",
    "customer_id": "testUser1@test.com",
    "type": "Payment Related",
    "description": "My payment failed but money is debited",
    "status": "Done",
    "resolution": "Payment reversed on NPCI end",
    "assigned_to": 1
  },
  "2": {
    "transaction_id": "T2",
    "customer_id": "testUser2@test.com",
    "type": "Mutual Fund Related",
    "description": "Unable to purchase Mutual Fund",
    "status": "Assigned",
    "resolution": "Pending",
    "assigned_to": null
  },
  "3": {
    "transaction_id": "T3",
    "customer_id": "testUser2@test.com",
    "type": "Payment Related",
    "description": "My payment failed but money is debited",
    "status": "Assigned",
    "resolution": "Pending",
    "assigned_to": 2
  }
}

'''


'''

CUSTOMER_ISSUES

{
  "testUser1@test.com": [1],
  "testUser2@test.com": [
    2,
    3
  ]
}

'''


'''

SERVICE_AGENTS

{
  "1": {
    "name": "Agent 1",
    "email": "agent1@test.com",
    "expertise": [
      "Payment Related",
      "Gold Related"
    ],
    "issues_pending": 0,
    "Payment Related Issues": [
      1
    ],
    "Gold Related Issues": []
  },
  "2": {
    "name": "Agent 2",
    "email": "agent2@test.com",
    "expertise": [
      "Payment Related"
    ],
    "issues_pending": 1,
    "Payment Related Issues": [
      3
    ]
  }
}

'''

