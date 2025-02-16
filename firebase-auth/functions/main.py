import firebase_admin
from firebase_admin import auth, firestore
from firebase_functions import identity_fn, https_fn
from firebase_functions.firestore_fn import on_document_deleted, Event, DocumentSnapshot

firebase_admin.initialize_app()

@identity_fn.before_user_created(region="asia-northeast1")
def before_create(event: identity_fn.AuthBlockingEvent) -> identity_fn.BeforeCreateResponse | None:
    # パラメータを取得
    user = event.data
    additional_info = event.additional_user_info
    credential = event.credential

    # ログ出力
    print(user)
    print(additional_info)
    print(credential)
    print(credential.provider_id)

    # 事前承認済みユーザーかどうかチェック
    db = firestore.client()
    ref = db.collection('allowedUsers')
    doc = ref.where('email', '==', user.email).limit(1).get()
    if not doc:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.NOT_FOUND,
            message="アプリケーションにアクセスできません。"
        )

    # IdP チェック
    if credential.provider_id != "oidc.entra-id":
        return
    
    # ドメインチェック
    if not user.email.endswith('@example.com'):
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.NOT_FOUND,
            message="アプリケーションにアクセスできません。"
        )

    # ここまできたらアプリケーションへのアクセス許可
    return