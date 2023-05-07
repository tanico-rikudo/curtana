import { ReactElement } from "react";

import type { NextPageWithLayout } from "./_app";
import Container from "@/components/containers/index";
import Layout from "@/components/templates/Layout";
import EdinetHeadline from "@/components/molecules/EdinetHeadline";

import { GetServerSideProps } from "next";
import prisma from "@/lib/prisma";


const HeadlineHome: NextPageWithLayout = ({ headlines }) => {
  console.log("headline->index")
  // console.log(headlines)
  return (
    <Container>
      <div className="h-24 min-h-0 md:min-h-full py-0 px-2 flex flex-col justify-center items-center">
        <h1 className="text-4xl text-purple-600">Headline</h1>
      </div>
      <div>{renderHeadline(headlines)}</div>
    </Container>
  );
};

HeadlineHome.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};


const renderHeadline = (headlines) => {
  // console.log("headline->index")
  // console.log(headlines)

  return (
    // <div>teeeee</div>
    <EdinetHeadline headlines={headlines} />
  );
};


export const getServerSideProps: GetServerSideProps = async () => {
  const headlines = await prisma.buyback_headline.findMany({
    take: 10
  });
  return {
    props: { headlines },
  };
};

export default HeadlineHome;
