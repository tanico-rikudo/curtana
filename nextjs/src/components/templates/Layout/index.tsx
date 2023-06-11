import Header from "@/components/orgnisms/NavBar";
import Sidebar from "@/components/orgnisms/SideBar";
import NavBar from "@/components/orgnisms/NavBar";
import Footer from "@/components/orgnisms/Footer";
import Separator from "@/components/atoms/Separator";
import Box from "@/components/layouts/Box";
import Flex from "@/components/layouts/Flex";


interface LayoutProps {
    children: React.ReactNode
}

const Layout = ({ children }: LayoutProps) => {
    return (
        <>
            <NavBar />
            <div className="flex">
                <Flex class_names="flex-none w-64">
                    <Sidebar />
                </Flex>
                <Flex class_names="grow">
                    <main>{children}</main>
                </Flex>
            </div>
            {/* <Separator /> */}
            {/* <Box>
                <Footer />
            </Box> */}
        </>
    )
}

export default Layout
