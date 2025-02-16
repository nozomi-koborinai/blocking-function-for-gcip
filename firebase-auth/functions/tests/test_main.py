import unittest
from firebase_auth.functions.main import evaluate_user, CheckResult

class TestEvaluateUser(unittest.TestCase):
    def test_skip_for_non_entraid_provider(self):
        # プロバイダが oidc.entra-id 以外の場合は SKIP となる
        result = evaluate_user("oidc.okta", True, "user@example.com")
        self.assertEqual(result, CheckResult.SKIP)

    def test_blocked_user_if_not_allowed(self):
        # プロバイダが oidc.entra-id で、かつユーザーが承認されていない場合は BLOCKED_USER
        result = evaluate_user("oidc.entra-id", False, "user@example.com")
        self.assertEqual(result, CheckResult.BLOCKED_USER)

    def test_blocked_domain_if_invalid_email(self):
        # プロバイダが oidc.entra-id で、ユーザーが承認されているが、email のドメインが不正な場合は BLOCKED_DOMAIN
        result = evaluate_user("oidc.entra-id", True, "user@invalid.com")
        self.assertEqual(result, CheckResult.BLOCKED_DOMAIN)

    def test_allowed_when_all_conditions_met(self):
        # プロバイダが oidc.entra-id で、ユーザーが承認済み、かつ email のドメインが正しい場合は ALLOWED
        result = evaluate_user("oidc.entra-id", True, "user@example.com")
        self.assertEqual(result, CheckResult.ALLOWED)

if __name__ == '__main__':
    unittest.main()