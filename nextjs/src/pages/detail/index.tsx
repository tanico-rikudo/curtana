import { ReactElement } from "react";

import type { NextPageWithLayout } from "./_app";
import Container from "@/components/containers/index";
import Layout from "@/components/templates/Layout";
import EdinetDetail from "@/components/molecules/EdinetDetail";

import { GetServerSideProps } from "next";
import prisma from "@/lib/prisma";


const DetailHome: NextPageWithLayout = ({ details }) => {
  console.log("detail->index")
  // console.log(details)
  return (
    <Container>
      <div className="h-24 min-h-0 md:min-h-full py-0 px-2 flex flex-col justify-center items-center">
        <h1 className="text-4xl text-purple-600">Detail</h1>
      </div>
      <div>{renderDetail(details)}</div>
    </Container>
  );
};

DetailHome.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};


const renderDetail = (details) => {
  return (
    <EdinetDetail details={details} />
  );
};


export const getServerSideProps: GetServerSideProps = async () => {
  const details = await prisma.buyback_detail.findMany({
    take: 10
  });
  return {
    props: { details },
  };
};

export default DetailHome;
