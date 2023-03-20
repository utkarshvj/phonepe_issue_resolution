from issue_resolution_adts import *

class IssueResolution(object):
    """docstring for Issue"""
    def __init__(self):
        self.issues = ISSUES
        self.agents = SERVICE_AGENTS


    def __get_min_issue_agent(self, issue_type):

        agent_ids = list(SERVICE_AGENTS.keys())
        min_issues_pending = None
        min_issues_agent = None
        
        for agent_id in agent_ids:
            agent_details = SERVICE_AGENTS[agent_id]


            if issue_type in agent_details['expertise']:
                if min_issues_pending is None:
                    min_issues_pending = agent_details['issues_pending']
                    min_issues_agent = agent_id
                elif min_issues_pending > agent_details['issues_pending']:
                    min_issues_pending = agent_details['issues_pending']
                    min_issues_agent = agent_id


        return min_issues_pending, min_issues_agent


    def create_issue(self, transaction_id, issue_type, subject, description, email):

        issue_id_key = ''
        issue_id = len(ISSUES.keys()) + 1

        ISSUES[issue_id] = {'transaction_id': transaction_id, 'customer_id': email, 'type': issue_type, 'description': description, 'status': 'Pending', 'resolution': 'Pending', 'assigned_to': None}
        
        if email not in CUSTOMER_ISSUES:
            CUSTOMER_ISSUES[email] = [issue_id]
        else:
            CUSTOMER_ISSUES[email].append(issue_id)
        

        return f'Issue I{issue_id} created against transaction {transaction_id}'


    def add_agent(self, agent_email, agent_name, issue_types):

        agent_id = len(SERVICE_AGENTS.keys()) + 1
        SERVICE_AGENTS[agent_id] = {'name': agent_name, 'email': agent_email, 'expertise': issue_types, 'issues_pending': 0}

        for issue_type in SERVICE_AGENTS[agent_id]['expertise']:
            SERVICE_AGENTS[agent_id][f'{issue_type} Issues'] = []

        return f'Agent A{agent_id} created'


    def assign_issue(self, issue_id):

        db_issue_id = int(issue_id.replace('I', ''))
        issue_details = ISSUES.get(db_issue_id)

        if not issue_details:
            return f'Issue {issue_id} not created yet'

        issue_type = issue_details['type']
        issues_pending, agent_id = self.__get_min_issue_agent(issue_type)
        ISSUES[db_issue_id]['assigned_to'] = agent_id
        ISSUES[db_issue_id]['status'] = 'Assigned'

        if agent_id is None:
            return f'Issue {issue_id} could not be assigned as no expert available'

        SERVICE_AGENTS[agent_id][f'{issue_type} Issues'].append(db_issue_id)
        SERVICE_AGENTS[agent_id]['issues_pending'] += 1

        if issues_pending:
            return f'Issue {issue_id} added to waitlist of A{agent_id}'
        return f'Issue {issue_id} assigned to A{agent_id}'


    def get_issues(self, filter):

        customer_email = filter.get('email')
        agent_id = filter.get('agent_id')
        issue_type = filter.get('type')

        issue_list = []
        if customer_email:
            cust_issues = CUSTOMER_ISSUES.get(customer_email) or []

            for issue_id in cust_issues:

                if issue_type:
                    if ISSUES[issue_id]['type'] == issue_type:
                        print(f'I{issue_id} {ISSUES[issue_id]}')
                else:
                    print(f'I{issue_id} {ISSUES[issue_id]}')
        elif agent_id:
            db_agent_id = int(agent_id.replace('A', ''))
            agent_details = SERVICE_AGENTS.get(db_agent_id)

            if agent_details is None:
                return f'Agent {agent_id} not created yet'

            if issue_type:
                for issue_id in agent_details[f'{issue_type} Issues']:
                    print(f'I{issue_id} {ISSUES[issue_id]}')
            else:
                for issue_type in agent_details['expertise']:
                    for issue_id in agent_details[f'{issue_type} Issues']:
                        print(f'I{issue_id} {ISSUES[issue_id]}')
        elif issue_type:

            all_issues = list(ISSUES.keys())

            for issue_id in all_issues:
                if issue_type == ISSUES[issue_id]['type']:
                    print(f'I{issue_id} {ISSUES[issue_id]}')
        else:
            print(f'Filter {filter} is not available yet')


    def update_issue(self, issue_id, status, resolution):

        db_issue_id = int(issue_id.replace('I', ''))
        issue_details = ISSUES[db_issue_id]
        issue_details['status'] = status
        issue_details['resolution'] = resolution

        if status == 'Done':
            db_agent_id = issue_details['assigned_to']

            SERVICE_AGENTS[db_agent_id]['issues_pending'] -= 1

        return f'{issue_id} status updated to {status}'


    def resolve_issue(self, issue_id, resolution):

        db_issue_id = int(issue_id.replace('I', ''))
        issue_details = ISSUES[db_issue_id]
        issue_details['status'] = 'Done'
        issue_details['resolution'] = resolution
        db_agent_id = issue_details['assigned_to']
        SERVICE_AGENTS[db_agent_id]['issues_pending'] -= 1

        return f'Issue {issue_id} marked as resolved'


    def view_agents_work_history(self):

        agent_ids = list(SERVICE_AGENTS.keys())
        for agent_id in agent_ids:

            agent_details = SERVICE_AGENTS[agent_id]
            agent_issues = []

            for issue_type in agent_details['expertise']:
                agent_issues += agent_details[f'{issue_type} Issues']

            agent_issues = sorted(agent_issues)
            ui_agent_issues = [f'I{issue_id}' for issue_id in agent_issues]
            print(f'A{agent_id} -> {ui_agent_issues}')
        