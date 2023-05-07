import { NextApiRequest, NextApiResponse } from "next";
import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

const findUserByCredentials = credentials => {

  // simple exmaple. match or not
  if (
    credentials.email === process.env.TEST_USER_EMAIL &&
    credentials.password === process.env.TEST_USER_PASSWORD
  ) {
    // OK
    return { id: 1, name: "test user" };
  } else {
    //NG
    return null;
  }
};

// NextAuth に渡すオプション
const options = {
  // 認証プロバイダー
  providers: [
    CredentialsProvider({
      name: "Email",
      //  Provide challenge method by myself
      credentials: {
        email: {
          label: "Email",
          type: "email",
          placeholder: "email@example.com",
        },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials, req) {
        const user = await findUserByCredentials(credentials);
        // console.log(user);
        if (user) {
          // 返されたオブジェクトはすべてJWTの`user`プロパティに保存される
          console.log(user);
          return user; //Promise.resolve(user);
        } else {
          // nullまたはfalseを返すと、認証を拒否する
          return null; // Promise.resolve(null);

          // ErrorオブジェクトやリダイレクトURLを指定してコールバックをリジェクトすることもできます。
          // return Promise.reject(new Error('error message')) // エラーページにリダイレクト
          // return Promise.reject('/path/to/redirect')        // URL にリダイレクト
        }
      },
      // callbacks: {
      //   async jwt(token, user, account, profile, isNewUser) {
      //     if (account?.accessToken) {
      //       token.accessToken = account.accessToken;
      //     }
      //     return token;
      //   },
      //   async session(session, token) {
      //     session.accessToken = (token as GenericObject).accessToken;
      //     return session;
      //   },
      // },
    }),
  ],
};

export default (req: NextApiRequest, res: NextApiResponse) => NextAuth(req, res, options);
