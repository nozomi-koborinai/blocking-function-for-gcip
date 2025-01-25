# blocking-function-sample

## Identity Platform

```bash
npm init -y

npm install typescript @types/node --save-dev

npx tsc --init

npm install gcip-cloud functions

gcloud functions deploy before-create \
--region=asia-northeast1 \
--runtime nodejs20 \
---no-gen2 \
--trigger-http \
--allow-unauthenticated \
--entry-point=beforeCreate \
--set-env-vars GCP_PROJECT=$project_id
```

## References

- [Customizing the authentication flow using blocking functions](https://cloud.google.com/identity-platform/docs/blocking-functions)
- [Blocking functions reference](https://cloud.google.com/identity-platform/docs/reference/gcip-cloud-functions)
- [Google Cloud Identity Platform Blocking Functions](https://www.npmjs.com/package/gcip-cloud-functions)
