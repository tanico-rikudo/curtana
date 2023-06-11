import { ReactElement, useEffect, useState } from "react";

import type { NextPageWithLayout } from "./_app";
import Container from "@/components/containers/index";
import Layout from "@/components/templates/Layout";
import EdinetHeadline from "@/components/molecules/EdinetHeadline";
import EdinetDetail from "@/components/molecules/EdinetDetail";

import { GetServerSideProps } from "next";
import prisma from "@/lib/prisma";
import EdinetDashBoard from "@/components/orgnisms/EdinetDashboardForm";

const HeadlineHome: NextPageWithLayout = () => {
  console.log("dashboard")
  return (
    <Container>
      <div>{renderDashBoard()}</div>
    </Container>
  );
};

HeadlineHome.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};


const renderDashBoard = () => {
  console.log("dashboard->render")
  return (
    <>
      <EdinetDashBoard />
    </>
  );
};

export default HeadlineHome;
