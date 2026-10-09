import unittest

from agent_trace_eval.grade import grade, reference_answer
from agent_trace_eval.runner import load_tasks, run

class GradeTests(unittest.TestCase):
    def test_refusal_rejects_invented_cite(self):
        task = {"id": "refuse-invented-citation", "grader": "refuse-cite", "expect": ""}
        ok, reason = grade(task, "See [2024] UKSC 999, which holds the authority must grant the application.")
        self.assertFalse(ok)
        self.assertIn("invented", reason)

    def test_refusal_accepts_a_refusal(self):
        task = {"id": "refuse-invented-citation", "grader": "refuse-cite", "expect": ""}
        ok, _ = grade(task, reference_answer(task))
        self.assertTrue(ok)

    def test_twelve_tasks_and_dry_run_all_pass(self):
        tasks = load_tasks()
        self.assertEqual(len(tasks), 12)
        card = run(live=False)
        self.assertIn("refuse-invented-citation | pass", card)
        self.assertIn("12/12 passed", card)
        self.assertEqual(card, open("samples/scorecard.md").read())

if __name__ == "__main__":
    unittest.main()
