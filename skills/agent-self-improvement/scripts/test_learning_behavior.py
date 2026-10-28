"""Fixture grader negative controls, not live agent evaluation."""
import copy
import tempfile
import unittest
from pathlib import Path

from learning_behavior import grade
from learning_cycle import read_json, write_json


class BehaviorGraderTests(unittest.TestCase):
    def test_windows_utf8_signature_does_not_hide_incorrect_state(self):
        case = read_json(Path(__file__).parent.parent / "assets/behavior-cases.json")["cases"][0]
        import json
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            state = copy.deepcopy(case['initial'])
            (root / 'rule.txt').write_text(case['initial_rule'], encoding='utf-8')
            (root / 'memory.json').write_text(json.dumps(state), encoding='utf-8-sig')
            self.assertEqual(grade(root, case), [])
            state['apply_count'] += 1
            (root / 'memory.json').write_text(json.dumps(state), encoding='utf-8-sig')
            self.assertIn('duplicate or missing application', grade(root, case))

    def test_six_and_twenty_four_trial_plans_cannot_shrink_coverage(self):
        from learning_behavior import trial_plan
        from learning_workflow import verification_plan
        for changes, count in (([], 24), ([{'find': 'same', 'replace': 'same'}], 6)):
            plan = verification_plan([], changes)
            cases = [{'id': name} for name in plan['scenarios']]
            self.assertEqual(trial_plan(cases, plan)[1], count)
            with self.assertRaises(ValueError):
                trial_plan(cases[:-1], plan)
            with self.assertRaises(ValueError):
                trial_plan(cases, dict(plan, repetitions=0))

    def test_expected_states_and_wrong_result_negative_controls(self):
        cases = read_json(Path(__file__).parent.parent / "assets/behavior-cases.json")["cases"]
        for case in cases:
            with self.subTest(case=case["id"]), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                state = copy.deepcopy(case["initial"])
                expected = case["expected"]
                for identifier, outcome in expected["records"].items():
                    state["records"][identifier].update(outcome=outcome, reason="Fixture expected justification")
                state.update(apply_count=expected["apply_count"], behavioral_passed=expected["behavioral_passed"])
                write_json(root / "memory.json", state)
                (root / "rule.txt").write_text(expected["rule"], encoding="utf-8")
                self.assertEqual(grade(root, case), [])
                state["apply_count"] += 1
                write_json(root / "memory.json", state)
                self.assertIn("duplicate or missing application", grade(root, case))

    def test_textual_success_cannot_replace_environment_result(self):
        case = read_json(Path(__file__).parent.parent / "assets/behavior-cases.json")["cases"][-1]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            state = copy.deepcopy(case["initial"])
            state["behavioral_passed"] = True
            write_json(root / "memory.json", state)
            (root / "rule.txt").write_text(case["initial_rule"], encoding="utf-8")
            (root / "answer.txt").write_text("Everything is verified successfully", encoding="utf-8")
            self.assertIn("incorrect behavioral certification", grade(root, case))


if __name__ == "__main__":
    unittest.main()
