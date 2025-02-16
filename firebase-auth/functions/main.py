import firebase_admin
from firebase_admin import firestore
from firebase_functions import identity_fn, https_fn
from enum import Enum

firebase_admin.initialize_app()

class CheckResult(Enum):
    SKIP = 0           # プロバイダが oidc.entra-id 以外の場合
    ALLOWED = 1        # チェックに成功し、アクセスが許可される場合
    BLOCKED_USER = 2   # 承認済みユーザーに登録されていない場合
    BLOCKED_DOMAIN = 3 # ドメインが example.com でない場合

def evaluate_user(provider_id: str, is_user_allowed: bool, email: str) -> CheckResult:
    """
    プロバイダ ID、承認済みユーザーかどうか、ユーザーの email から
    チェック結果を返します。
    
    要件:
      1. プロバイダが "oidc.entra-id" 以外の場合はチェックをスキップ（SKIP）
      2. プロバイダが "oidc.entra-id" の場合、
         - 許可済みユーザー (is_user_allowed=True) でなければ BLOCKED_USER
         - email のドメインが "@example.com" でなければ BLOCKED_DOMAIN
         - それ以外は ALLOWED
    """
    if provider_id != "oidc.entra-id":
        return CheckResult.SKIP
    if not is_user_allowed:
        return CheckResult.BLOCKED_USER
    if not email.endswith('@example.com'):
        return CheckResult.BLOCKED_DOMAIN
    return CheckResult.ALLOWED

@identity_fn.before_user_created(region="asia-northeast1")
def before_create(event: identity_fn.AuthBlockingEvent) -> identity_fn.BeforeCreateResponse | None:
    # event から必要なパラメータを取得
    user = event.data
    credential = event.credential

    # Firestore から allowedUsers コレクションを参照してユーザーが登録されているかチェック
    db = firestore.client()
    allowed_docs = db.collection('allowedUsers').where('email', '==', user.email).limit(1).get()
    is_user_allowed = bool(allowed_docs)

    result = evaluate_user(credential.provider_id, is_user_allowed, user.email)
    if result == CheckResult.SKIP:
        # oidc.entra-id 以外の場合はチェックをスキップしてそのまま返す
        return
    elif result == CheckResult.BLOCKED_USER:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.NOT_FOUND,
            message="承認済みユーザーのみ、アプリケーションにアクセスすることが可能です。"
        )
    elif result == CheckResult.BLOCKED_DOMAIN:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.NOT_FOUND,
            message="ドメインが異なる場合はアプリケーションにアクセスできません。"
        )

    # ALLOWED の場合は何もせずにそのままアクセスを許可する
    return