import { useState, useEffect, useCallback, useRef } from 'react';
import { ReactElement } from "react";
import { useRouter } from 'next/router';
import Container from "@/components/containers/index";
import Layout from "@/components/templates/Layout";
import { getSession, signIn, signOut, useSession } from "next-auth/react";
import { Session } from "next-auth";
import { NextPageWithLayout } from './_app';
import Link from 'next/link';


const Index: NextPageWithLayout = () => {

  return (
    <Container>
      {/* <div className="h-24 min-h-0 md:min-h-full py-0 px-2 flex flex-col justify-center items-center">
        <h1 className="text-left text-4xl text-purple-600">Edinet Contoroler</h1>
      </div> */}
      {/* <div>{renderSesssion(session)}</div> */}
    </Container>
  );
};

Index.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};

// const renderSesssion = (session) => {

//   // if (loading) {
//   //   return <div>Loading...</div>;
//   // }
//   // console.log(session);
//   return (
//     <div>
//       {session && (
//         <>
//           Signed in as {session.user.name} <br />
//           <button onClick={signOut}>Sign out</button>
//         </>
//       )}
//       {!session && (
//         <>
//           Not signed in <br />
//           <button onClick={signIn}>Sign in</button>
//         </>
//       )}
//     </div>
//   );
// };

export default Index;




