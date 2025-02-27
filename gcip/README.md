# blocking-function-sample

<img width="1453" alt="Google Chrome 2025-01-25 14 29 05" src="https://github.com/user-attachments/assets/a3dd2e83-175a-4643-a11f-133eaa9ca08c" />
<img width="809" alt="Google Chrome 2025-01-25 14 29 26" src="https://github.com/user-attachments/assets/533117cf-ac69-4954-ab8b-707b7af5ca74" />

## Identity Platform

```bash
npm init -y

npm install typescript @types/node --save-dev

npx tsc --init

npm install gcip-cloud functions

gcloud functions deploy before-create \
--region=asia-northeast1 \
--runtime nodejs20 \
--no-gen2 \
--trigger-http \
--allow-unauthenticated \
--entry-point=beforeCreate \
--set-env-vars GCP_PROJECT=$project_id
```

## References

- [Customizing the authentication flow using blocking functions](https://cloud.google.com/identity-platform/docs/blocking-functions)
- [Blocking functions reference](https://cloud.google.com/identity-platform/docs/reference/gcip-cloud-functions)
- [Google Cloud Identity Platform Blocking Functions](https://www.npmjs.com/package/gcip-cloud-functions)
