import "@/styles/globals.css";
import { AppProps } from "next/app";
// import { ThemeProvider } from 'styled-components'
import { ThemeProvider } from "next-themes";
import { NextPage } from "next";
import { ReactElement, ReactNode } from "react";
import Header from "@/components/layouts/Header";

import { SessionProvider, signIn, useSession } from "next-auth/react";
import type { Session } from "next-auth/react";

export type NextPageWithLayout<P = {}, IP = P> = NextPage<P, IP> & {
  getLayout?: (page: ReactElement) => ReactNode;
};

type AppPropsWithLayout<P> = AppProps<P> & {
  Component: NextPageWithLayout<P>;
};

// Theme provider
// https://zenn.dev/nawomat/articles/3c7222ae01235f
// https://github.com/chakra-ui/chakra-ui/issues/4689

// Session provider
// https://stackoverflow.com/questions/73942758/how-to-use-next-auth-with-per-page-layouts-in-next-js-with-typescript
export default function MyApp({
  Component,
  pageProps,
}: AppPropsWithLayout<{ session: Session }>) {
  const getLayout =
    Component.getLayout ||
    ((page) => {
      return page;
    });
  // console.log("app.tsx");
  // console.log(pageProps);
  return (
    <>
      <SessionProvider session={pageProps.session}>
        <Header />
        <ThemeProvider attribute="class" defaultTheme="dark">
          {getLayout(<Component {...pageProps} />)}
        </ThemeProvider>
      </SessionProvider>
    </>
  );
};
