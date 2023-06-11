import { ReactElement, useEffect, useState } from "react";

import type { NextPageWithLayout } from "./_app";
import Container from "@/components/containers/index";
import Layout from "@/components/templates/Layout";
import EdinetHeadline from "@/components/molecules/EdinetHeadline";
import EdinetDetail from "@/components/molecules/EdinetDetail";


import { GetServerSideProps } from "next";
import prisma from "@/lib/prisma";




const HeadlineHome: NextPageWithLayout = ({ headlines }) => {
  console.log("headline->index")

  const [details, setDetails] = useState("");
  const [display, setDisplayDetail] = useState("hidden");
  const handleDetailChange = (newValue) => {
    setDetails(newValue);
    setDisplayDetail("")
  };

  return (
    <Container>
      {/* <div className="h-24 min-h-0 md:min-h-full py-0 px-2 flex flex-col justify-center items-center">
        <h1 className="text-4xl text-purple-600">Headline</h1>
      </div> */}
      <div>{renderHeadline(headlines, handleDetailChange)}</div>
      <div className={`${display}`}>{renderDetail(details)}</div>
    </Container>
  );
};

HeadlineHome.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};


const renderHeadline = (headlines, handleDetailChange) => {
  console.log("headline->render")
  return (
    <>
      <EdinetHeadline headlines={headlines} handleDetailChange={handleDetailChange} />
    </>
  );
};

const renderDetail = (details) => {
  console.log("detail->render")
  console.log(details)
  return (
    <>
      <EdinetDetail details={details} />
    </>
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
