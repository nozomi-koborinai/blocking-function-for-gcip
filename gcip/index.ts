// https://www.npmjs.com/package/gcip-cloud-functions

import * as gcipCloudFunctions from 'gcip-cloud-functions';

const auth = new gcipCloudFunctions.Auth();

export const beforeCreate = auth.functions().beforeCreateHandler((user, context) => {
  // Write to the log
  console.log('AdditionalUserInfo:', {
      providerId: context.additionalUserInfo?.providerId,
      profile: context.additionalUserInfo?.profile,
      username: context.additionalUserInfo?.username,
      isNewUser: context.additionalUserInfo?.isNewUser
    });
    console.log('AuthCredential:', {
      claims: context.credential?.claims,
      idToken: context.credential?.idToken,
      accessToken: context.credential?.accessToken,
      refreshToken: context.credential?.refreshToken,
      expirationTime: context.credential?.expirationTime,
      providerId: context.credential?.providerId
    });
    console.log('User:', {
      email: user.email,
      uid: user.uid,
      displayName: user.displayName,
      photoURL: user.photoURL,
    });

  // Example of allowing only specific domains
  if (!user.email?.endsWith('@example.com')) {
    throw new gcipCloudFunctions.https.HttpsError(
      'invalid-argument',
      'You are not allowed to register this domain'
    );
  }
  return {};
});
