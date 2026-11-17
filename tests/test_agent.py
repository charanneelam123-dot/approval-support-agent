import unittest
from unittest.mock import patch
from agent import SupportAgent

class AgentTests(unittest.TestCase):
    def test_eligible_refund_requires_approval(self):
        result = SupportAgent().run('Refund A100')
        self.assertEqual(result['pending_approvals'][0]['status'], 'pending_human_approval')
    def test_expired_order_denied(self):
        self.assertEqual(SupportAgent().tool('request_refund', {'order_id':'A200'})['status'], 'denied')
    def test_in_transit_denied(self):
        self.assertEqual(SupportAgent().tool('request_refund', {'order_id':'A300'})['status'], 'denied')
    def test_unknown_tool_denied(self):
        self.assertIn('error', SupportAgent().tool('execute_payment', {}))
    def test_bad_arguments(self):
        self.assertIn('error', SupportAgent().tool('lookup_order', {'order_id':[], 'extra':1}))
    def test_duplicate_request_idempotent(self):
        agent = SupportAgent()
        for _ in range(2):
            agent.tool('request_refund', {'order_id':'A100'})
        self.assertEqual(len(agent.pending), 1)
    @patch('agent.complete', return_value=({'role':'assistant','tool_calls':[{'id':'1','type':'function','function':{'name':'read_policy','arguments':'{}'}}]}, {}))
    def test_step_budget(self, mock):
        result = SupportAgent().run('loop', True, max_steps=2)
        self.assertIn('budget exhausted', result['reply'])
        self.assertEqual(mock.call_count, 2)

if __name__ == '__main__':
    unittest.main()
